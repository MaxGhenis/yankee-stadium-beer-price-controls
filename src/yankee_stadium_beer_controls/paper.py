"""Package-native Quarto artifact generation for the paper."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections.abc import Callable
from datetime import date
from importlib import resources
from pathlib import Path
from typing import Any

import numpy as np

from yankee_stadium_beer_controls.config_loader import load_full_config
from yankee_stadium_beer_controls.model import ConsumerType, StadiumEconomicModel
from yankee_stadium_beer_controls.price_ceiling_analysis import (
    create_charts,
    simulate_price_ceilings,
)

PAPER_TITLE = "Beer Price Ceilings and Joint Pricing in Sports Venues: A Yankee Stadium Application"
PAPER_KEYWORDS = [
    "price controls",
    "sports economics",
    "alcohol policy",
    "monopoly pricing",
    "complementary goods",
    "selection effects",
]
PAPER_JEL_CODES = ["D42", "L12", "L83"]
AUTHOR_NAME = "Max Ghenis"
AUTHOR_EMAIL = "max@policyengine.org"
AUTHOR_AFFILIATION = "PolicyEngine"
PACKAGED_PAPER_PROJECT_DIR = "paper_project"
PACKAGED_PAPER_FILES = ("_quarto.yml", "index.qmd", "references.bib")


def _pct_change(new: float, old: float) -> float:
    return (new / old - 1) * 100


def _scenario(model: StadiumEconomicModel, ceiling: float | None) -> dict[str, Any]:
    if ceiling is None:
        ticket_price, beer_price, result = model.optimal_pricing()
        label = "baseline"
    else:
        ticket_price, beer_price, result = model.optimal_pricing(
            beer_price_control=ceiling,
            ceiling_mode=True,
        )
        label = f"ceiling_{ceiling:g}"
    welfare = model.social_welfare(ticket_price, beer_price)
    drinker_attendance = result["breakdown_by_type"]["Drinker"]["attendance"]
    result_bundle = {
        "label": label,
        "ticket_price": ticket_price,
        "beer_price": beer_price,
        "attendance": result["attendance"],
        "drinker_share_attendance": drinker_attendance / result["attendance"],
        "beers_per_fan": result["beers_per_fan"],
        "total_beers": result["total_beers"],
        "profit": result["profit"],
        "consumer_surplus": welfare["consumer_surplus"],
        "tax_revenue": welfare["tax_revenue"],
        "externality_cost": welfare["externality_cost"],
        "social_welfare": welfare["social_welfare"],
        "breakdown_by_type": result["breakdown_by_type"],
    }
    return result_bundle


def _decomposition(base: dict[str, Any], ceiling: dict[str, Any]) -> dict[str, float]:
    base_attendance = base["attendance"]
    ceiling_attendance = ceiling["attendance"]
    base_beers = base["beers_per_fan"]
    ceiling_beers = ceiling["beers_per_fan"]

    intensive_1 = ceiling_attendance * (ceiling_beers - base_beers)
    extensive_1 = (ceiling_attendance - base_attendance) * base_beers
    intensive_2 = base_attendance * (ceiling_beers - base_beers)
    extensive_2 = (ceiling_attendance - base_attendance) * ceiling_beers

    intensive = (intensive_1 + intensive_2) / 2
    extensive = (extensive_1 + extensive_2) / 2
    baseline_total = base["total_beers"]

    return {
        "intensive_pct_of_baseline": intensive / baseline_total * 100,
        "extensive_pct_of_baseline": extensive / baseline_total * 100,
    }


def _ticket_foc_decomposition(
    model: StadiumEconomicModel,
    scenario: dict[str, Any],
) -> dict[str, float]:
    """Decompose the ticket FOC into standalone and concession/cost terms."""
    beer_price = scenario["beer_price"]
    pre_tax_beer_price = beer_price / (1 + model.beer_sales_tax_rate)
    stadium_beer_margin = pre_tax_beer_price - model.beer_excise_tax - model.beer_cost
    marginal_internal_cost = (
        2 * model.experience_degradation_cost * scenario["total_beers"] / 1_000_000
    )
    effective_beer_margin = stadium_beer_margin - marginal_internal_cost
    concession_cost_adjustment = -effective_beer_margin * scenario["beers_per_fan"]

    return {
        "ticket_price": scenario["ticket_price"],
        "ticket_margin": scenario["ticket_price"] - model.ticket_cost,
        "standalone_ticket_markup": 1 / model.ticket_price_sensitivity,
        "stadium_beer_margin": stadium_beer_margin,
        "marginal_internal_cost": marginal_internal_cost,
        "effective_beer_margin": effective_beer_margin,
        "marginal_attendee_beer_intensity": scenario["beers_per_fan"],
        "concession_cost_adjustment": concession_cost_adjustment,
        "foc_implied_ticket_margin": (1 / model.ticket_price_sensitivity)
        + concession_cost_adjustment,
    }


def _run_one_way_sensitivity() -> list[dict[str, Any]]:
    """Run targeted one-way sensitivity checks around the calibrated model."""

    def linspace_values(start: float, stop: float) -> list[float]:
        return [float(value) for value in np.linspace(start, stop, 5)]

    def outcome(model: StadiumEconomicModel) -> tuple[float, float, float]:
        base = _scenario(model, None)
        ceiling = _scenario(model, 6.0)
        return (
            _pct_change(ceiling["ticket_price"], base["ticket_price"]),
            _pct_change(ceiling["attendance"], base["attendance"]),
            _pct_change(ceiling["total_beers"], base["total_beers"]),
        )

    checks: list[tuple[str, str, list[float], Callable[[float], StadiumEconomicModel]]] = [
        (
            "Drinker share",
            "30% to 50%",
            linspace_values(0.30, 0.50),
            lambda value: StadiumEconomicModel(
                consumer_types=[
                    ConsumerType(name="Non-Drinker", share=1 - float(value), alpha_beer=0.0),
                    ConsumerType(name="Drinker", share=float(value), alpha_beer=43.75),
                ]
            ),
        ),
        (
            "Drinker consumption target",
            "2.0 to 3.5 beers",
            linspace_values(2.0, 3.5),
            lambda value: StadiumEconomicModel(
                consumer_types=[
                    ConsumerType(name="Non-Drinker", share=0.60, alpha_beer=0.0),
                    ConsumerType(
                        name="Drinker",
                        share=0.40,
                        alpha_beer=12.50 * (float(value) + 1),
                    ),
                ]
            ),
        ),
        (
            "Ticket-price sensitivity",
            "0.010 to 0.016",
            linspace_values(0.010, 0.016),
            lambda value: StadiumEconomicModel(ticket_price_sensitivity=float(value)),
        ),
        (
            "Internal crowd cost",
            "0 to 160",
            linspace_values(0.0, 160.0),
            lambda value: StadiumEconomicModel(experience_degradation_cost=float(value)),
        ),
        (
            "Beer cap",
            "5 to 10 beers",
            linspace_values(5.0, 10.0),
            lambda value: StadiumEconomicModel(beer_max_per_person=float(value)),
        ),
        (
            "Beer marginal cost",
            "$1.50 to $2.50",
            linspace_values(1.50, 2.50),
            lambda value: StadiumEconomicModel(beer_cost=float(value)),
        ),
    ]

    summaries = []
    for parameter, range_label, values, model_factory in checks:
        outcomes = np.asarray([outcome(model_factory(value)) for value in values])
        summaries.append(
            {
                "parameter": parameter,
                "range": range_label,
                "ticket_change_min": float(outcomes[:, 0].min()),
                "ticket_change_max": float(outcomes[:, 0].max()),
                "attendance_change_min": float(outcomes[:, 1].min()),
                "attendance_change_max": float(outcomes[:, 1].max()),
                "beer_change_min": float(outcomes[:, 2].min()),
                "beer_change_max": float(outcomes[:, 2].max()),
            }
        )
    return summaries


def _ticket_friction_sensitivity(model: StadiumEconomicModel) -> list[dict[str, float | str]]:
    """Evaluate the $6 ceiling when ticket repricing is mechanically constrained."""
    baseline = _scenario(model, None)
    full_ticket = _scenario(model, 6.0)["ticket_price"]

    cases = [
        ("No ticket increase", 1.00),
        ("10% ticket cap", 1.10),
        ("25% ticket cap", 1.25),
        ("Full repricing", full_ticket / baseline["ticket_price"]),
    ]

    rows: list[dict[str, float | str]] = []
    for label, ticket_multiplier in cases:
        ticket_price = min(full_ticket, baseline["ticket_price"] * ticket_multiplier)
        result = model.stadium_revenue(ticket_price, 6.0)
        rows.append(
            {
                "case": label,
                "ticket_price": ticket_price,
                "ticket_change": _pct_change(ticket_price, baseline["ticket_price"]),
                "attendance_change": _pct_change(result["attendance"], baseline["attendance"]),
                "beer_change": _pct_change(result["total_beers"], baseline["total_beers"]),
                "profit_change": _pct_change(result["profit"], baseline["profit"]),
            }
        )
    return rows


def run_monte_carlo(draws: int = 1000, seed: int = 42) -> dict[str, float]:
    """Vary key assumptions and return sign-robustness shares."""
    rng = np.random.default_rng(seed)
    outcomes: list[dict[str, float | bool]] = []

    for _ in range(draws):
        drinker_share = float(rng.uniform(0.30, 0.50))
        drinker_consumption = float(rng.uniform(2.0, 3.5))
        drinker_alpha = 12.50 * (drinker_consumption + 1)
        model = StadiumEconomicModel(
            consumer_types=[
                ConsumerType(name="Non-Drinker", share=1.0 - drinker_share, alpha_beer=0.0),
                ConsumerType(name="Drinker", share=drinker_share, alpha_beer=drinker_alpha),
            ],
            beer_max_per_person=float(rng.uniform(5.0, 10.0)),
            ticket_cost=float(rng.uniform(3.0, 4.0)),
            beer_cost=float(rng.uniform(1.5, 2.5)),
            experience_degradation_cost=float(rng.uniform(0.0, 160.0)),
            ticket_price_sensitivity=float(rng.uniform(0.010, 0.016)),
        )
        model.external_costs["crime"] = float(rng.uniform(1.5, 3.5))
        model.external_costs["health"] = float(rng.uniform(1.0, 2.0))

        base = _scenario(model, None)
        ceiling = _scenario(model, 6.0)
        ticket_pct = _pct_change(ceiling["ticket_price"], base["ticket_price"])
        beer_pct = _pct_change(ceiling["total_beers"], base["total_beers"])
        welfare_pct = _pct_change(ceiling["social_welfare"], base["social_welfare"])
        outcomes.append(
            {
                "ticket_up": ceiling["ticket_price"] > base["ticket_price"],
                "profit_down": ceiling["profit"] < base["profit"],
                "beers_up": ceiling["total_beers"] > base["total_beers"],
                "welfare_down": ceiling["social_welfare"] < base["social_welfare"],
                "ticket_pct": ticket_pct,
                "beer_pct": beer_pct,
                "welfare_pct": welfare_pct,
            }
        )

    def share(key: str) -> float:
        return float(np.mean([outcome[key] for outcome in outcomes]) * 100)

    def percentile(key: str, percentile_value: float) -> float:
        return float(np.percentile([outcome[key] for outcome in outcomes], percentile_value))

    return {
        "draws": draws,
        "ticket_up_share": share("ticket_up"),
        "profit_down_share": share("profit_down"),
        "beers_up_share": share("beers_up"),
        "welfare_down_share": share("welfare_down"),
        "ticket_pct_p10": percentile("ticket_pct", 10),
        "ticket_pct_p50": percentile("ticket_pct", 50),
        "ticket_pct_p90": percentile("ticket_pct", 90),
        "beer_pct_p10": percentile("beer_pct", 10),
        "beer_pct_p50": percentile("beer_pct", 50),
        "beer_pct_p90": percentile("beer_pct", 90),
        "welfare_pct_p10": percentile("welfare_pct", 10),
        "welfare_pct_p50": percentile("welfare_pct", 50),
        "welfare_pct_p90": percentile("welfare_pct", 90),
    }


def compute_report_context(
    model: StadiumEconomicModel | None = None, draws: int = 1000
) -> dict[str, Any]:
    """Compute all dynamic outputs used by the Quarto paper."""
    model = model or StadiumEconomicModel()
    full_config = load_full_config()
    calibration_config = full_config.get("calibration", {})
    baseline = _scenario(model, None)
    ceiling_10 = _scenario(model, 10.0)
    ceiling_8 = _scenario(model, 8.0)
    ceiling_6 = _scenario(model, 6.0)
    ceiling_5 = _scenario(model, 5.0)
    decomposition = _decomposition(baseline, ceiling_6)
    mechanism = {
        "baseline": _ticket_foc_decomposition(model, baseline),
        "ceiling_6": _ticket_foc_decomposition(model, ceiling_6),
    }
    one_way_sensitivity = _run_one_way_sensitivity()
    ticket_friction = _ticket_friction_sensitivity(model)
    monte_carlo = run_monte_carlo(draws=draws)

    ceilings = {
        "10": ceiling_10,
        "8": ceiling_8,
        "6": ceiling_6,
        "5": ceiling_5,
    }

    ceiling_summary = {
        key: {
            "ticket_pct_change": _pct_change(value["ticket_price"], baseline["ticket_price"]),
            "attendance_pct_change": _pct_change(value["attendance"], baseline["attendance"]),
            "beers_pct_change": _pct_change(value["total_beers"], baseline["total_beers"]),
        }
        for key, value in ceilings.items()
    }

    return {
        "baseline": baseline,
        "ceiling_6": ceiling_6,
        "ceiling_8": ceiling_8,
        "ceiling_10": ceiling_10,
        "ceiling_5": ceiling_5,
        "decomposition": decomposition,
        "mechanism": mechanism,
        "one_way_sensitivity": one_way_sensitivity,
        "ticket_friction": ticket_friction,
        "ceiling_summary": ceiling_summary,
        "monte_carlo": monte_carlo,
        "calibration": {
            "target_ticket_price": model.base_ticket_price,
            "target_beer_price": calibration_config.get(
                "target_optimal_beer", model.base_beer_price
            ),
            "target_attendance_share": model.base_attendance / model.capacity,
            "target_beers_per_fan": calibration_config.get(
                "aggregate_consumption_at_baseline", 1.0
            ),
            "target_drinker_beers": calibration_config.get("drinker_consumption_at_baseline", 2.5),
            "experience_degradation_cost": model.experience_degradation_cost,
            "ticket_price_sensitivity": model.ticket_price_sensitivity,
            "ticket_elasticity_at_80": -model.ticket_price_sensitivity * 80,
        },
        "credibility": {
            "baseline_attendance_share": baseline["attendance"] / model.capacity,
            "baseline_drinker_beers": baseline["breakdown_by_type"]["Drinker"]["beers_per_fan"],
            "baseline_drinker_share": baseline["drinker_share_attendance"],
            "ceiling_6_drinker_share": ceiling_6["drinker_share_attendance"],
        },
    }


def _format_currency(value: float, decimals: int = 2) -> str:
    return f"${value:,.{decimals}f}"


def _format_pct(value: float, decimals: int = 1) -> str:
    return f"{value:+,.{decimals}f}%"


def _format_pct_range(low: float, high: float, decimals: int = 1) -> str:
    return f"{_format_pct(low, decimals)} to {_format_pct(high, decimals)}"


def _format_percent_level(value: float, decimals: int = 1) -> str:
    return f"{value * 100:,.{decimals}f}%"


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    lines = ["| " + " | ".join(headers) + " |", separator]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def _format_letter_date(current_date: date | None = None) -> str:
    current_date = current_date or date.today()
    return f"{current_date.strftime('%B')} {current_date.day}, {current_date.year}"


def _packaged_paper_project_root():
    packaged_root = resources.files("yankee_stadium_beer_controls").joinpath(
        PACKAGED_PAPER_PROJECT_DIR
    )
    if packaged_root.is_dir():
        return packaged_root
    return Path(__file__).resolve().parents[2] / "paper"


def _ensure_paper_project(project_dir: str | Path) -> Path:
    project_path = Path(project_dir)
    project_path.mkdir(parents=True, exist_ok=True)

    resource_root = _packaged_paper_project_root()
    for filename in PACKAGED_PAPER_FILES:
        target = project_path / filename
        if target.exists():
            continue
        source = resource_root.joinpath(filename)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    return project_path


def write_markdown_artifacts(context: dict[str, Any], output_dir: Path) -> None:
    """Emit markdown fragments consumed by Quarto includes."""
    baseline = context["baseline"]
    ceiling_6 = context["ceiling_6"]
    ceiling_8 = context["ceiling_8"]
    ceiling_10 = context["ceiling_10"]
    ceiling_5 = context["ceiling_5"]
    calibration = context["calibration"]
    ceiling_summary = context["ceiling_summary"]
    monte_carlo = context["monte_carlo"]
    decomposition = context["decomposition"]
    mechanism = context["mechanism"]
    one_way_sensitivity = context["one_way_sensitivity"]
    ticket_friction = context["ticket_friction"]
    credibility = context["credibility"]

    abstract = "\n".join(
        [
            "Sports venues jointly price tickets and concessions. This paper asks how a profit-maximizing venue responds when regulators cap beer prices but leave tickets unconstrained. I build a calibrated partial-equilibrium model of Yankee Stadium with drinkers and non-drinkers, utility-consistent beer demand, and attendance that responds to beer consumer surplus.",
            "",
            f"The benchmark matches an {_format_currency(baseline['ticket_price'], 0)} ticket, a {_format_currency(baseline['beer_price'])} beer, {_format_percent_level(credibility['baseline_attendance_share'])} capacity use, and {baseline['beers_per_fan']:.2f} beers per attendee. Under a binding $6 ceiling, the stadium raises tickets to {_format_currency(ceiling_6['ticket_price'], 0)}, attendance falls to {ceiling_6['attendance']:,.0f}, and beer sales rise {_format_pct(_pct_change(ceiling_6['total_beers'], baseline['total_beers']))}.",
            "",
            "The mechanism is joint pricing: cheaper beer changes both intensive drinking and attendee composition. The exercise is not causal, but it suggests that concession price ceilings may be poorly targeted when alcohol harms are the policy concern.",
        ]
    )
    (output_dir / "abstract.md").write_text(abstract + "\n")

    mechanism_rows = [
        [
            "Ticket price",
            _format_currency(mechanism["baseline"]["ticket_price"]),
            _format_currency(mechanism["ceiling_6"]["ticket_price"]),
        ],
        [
            "Ticket margin",
            _format_currency(mechanism["baseline"]["ticket_margin"]),
            _format_currency(mechanism["ceiling_6"]["ticket_margin"]),
        ],
        [
            "Standalone ticket markup",
            _format_currency(mechanism["baseline"]["standalone_ticket_markup"]),
            _format_currency(mechanism["ceiling_6"]["standalone_ticket_markup"]),
        ],
        [
            "Stadium beer margin before crowd costs",
            _format_currency(mechanism["baseline"]["stadium_beer_margin"]),
            _format_currency(mechanism["ceiling_6"]["stadium_beer_margin"]),
        ],
        [
            "Marginal internal crowd cost per beer",
            _format_currency(mechanism["baseline"]["marginal_internal_cost"]),
            _format_currency(mechanism["ceiling_6"]["marginal_internal_cost"]),
        ],
        [
            "Effective beer margin net of crowd cost",
            _format_currency(mechanism["baseline"]["effective_beer_margin"]),
            _format_currency(mechanism["ceiling_6"]["effective_beer_margin"]),
        ],
        [
            "Marginal attendee beer intensity",
            f"{mechanism['baseline']['marginal_attendee_beer_intensity']:.2f}",
            f"{mechanism['ceiling_6']['marginal_attendee_beer_intensity']:.2f}",
        ],
        [
            "Concession/crowd-cost ticket adjustment",
            _format_currency(mechanism["baseline"]["concession_cost_adjustment"]),
            _format_currency(mechanism["ceiling_6"]["concession_cost_adjustment"]),
        ],
    ]
    mechanism_text = "\n".join(
        [
            "The ticket first-order condition separates the ordinary ticket markup from the concession and crowd-cost value of a marginal attendee:",
            "",
            r"$$P_T - c_T = -\frac{A}{A_T} - \left[m_B(P_B) - C'(Q)\right]\frac{Q_T}{A_T}.$$",
            "",
            "The first term is the standalone ticket markup. The second term is the joint-pricing adjustment: if a marginal attendee buys profitable beer, the venue is willing to lower the ticket markup; if the marginal attendee generates beer-related crowd costs above beer margins, the adjustment raises the ticket markup. In the calibrated benchmark, the $6 ceiling both lowers the stadium's beer margin and makes attendees more beer-intensive, so the crowd-cost adjustment becomes much larger. This mechanism is conditional on the private crowd-cost calibration rather than an independently estimated stadium cost.",
            "",
            r"The private crowd-cost coefficient has units of dollars per squared thousand beers because $C(Q)=k(Q/1000)^2$. The marginal internal cost rows below report $C'(Q)=2kQ/1{,}000{,}000$ dollars per beer.",
            "",
            _markdown_table(["FOC component", "Baseline", "$6 ceiling"], mechanism_rows),
        ]
    )
    (output_dir / "mechanism.md").write_text(mechanism_text + "\n")

    results_rows = [
        [
            "Ticket price",
            _format_currency(baseline["ticket_price"]),
            _format_currency(ceiling_6["ticket_price"]),
            _format_pct(_pct_change(ceiling_6["ticket_price"], baseline["ticket_price"])),
        ],
        [
            "Beer price",
            _format_currency(baseline["beer_price"]),
            _format_currency(ceiling_6["beer_price"]),
            _format_pct(_pct_change(ceiling_6["beer_price"], baseline["beer_price"])),
        ],
        [
            "Attendance",
            f"{baseline['attendance']:,.0f}",
            f"{ceiling_6['attendance']:,.0f}",
            _format_pct(_pct_change(ceiling_6["attendance"], baseline["attendance"])),
        ],
        [
            "Drinker share of attendance",
            f"{baseline['drinker_share_attendance'] * 100:.1f}%",
            f"{ceiling_6['drinker_share_attendance'] * 100:.1f}%",
            f"{(ceiling_6['drinker_share_attendance'] - baseline['drinker_share_attendance']) * 100:+.1f} pp",
        ],
        [
            "Beers per fan",
            f"{baseline['beers_per_fan']:.2f}",
            f"{ceiling_6['beers_per_fan']:.2f}",
            _format_pct(_pct_change(ceiling_6["beers_per_fan"], baseline["beers_per_fan"])),
        ],
        [
            "Total beers",
            f"{baseline['total_beers']:,.0f}",
            f"{ceiling_6['total_beers']:,.0f}",
            _format_pct(_pct_change(ceiling_6["total_beers"], baseline["total_beers"])),
        ],
        [
            "Stadium profit",
            _format_currency(baseline["profit"], 0),
            _format_currency(ceiling_6["profit"], 0),
            _format_pct(_pct_change(ceiling_6["profit"], baseline["profit"])),
        ],
        [
            "Consumer surplus",
            _format_currency(baseline["consumer_surplus"], 0),
            _format_currency(ceiling_6["consumer_surplus"], 0),
            _format_pct(_pct_change(ceiling_6["consumer_surplus"], baseline["consumer_surplus"])),
        ],
        [
            "Tax revenue",
            _format_currency(baseline["tax_revenue"], 0),
            _format_currency(ceiling_6["tax_revenue"], 0),
            _format_pct(_pct_change(ceiling_6["tax_revenue"], baseline["tax_revenue"])),
        ],
        [
            "External alcohol costs",
            _format_currency(baseline["externality_cost"], 0),
            _format_currency(ceiling_6["externality_cost"], 0),
            _format_pct(_pct_change(ceiling_6["externality_cost"], baseline["externality_cost"])),
        ],
        [
            "Social welfare",
            _format_currency(baseline["social_welfare"], 0),
            _format_currency(ceiling_6["social_welfare"], 0),
            _format_pct(_pct_change(ceiling_6["social_welfare"], baseline["social_welfare"])),
        ],
    ]
    (output_dir / "baseline_vs_6.md").write_text(
        "Social welfare is computed as consumer surplus plus stadium profit plus tax revenue minus external alcohol costs.\n\n"
        + _markdown_table(["Outcome", "Baseline", "$6 Ceiling", "Change"], results_rows)
        + "\n"
    )

    ceiling_lines = [
        "The comparative statics are monotonic: tighter ceilings produce larger ticket increases, larger attendance declines, and larger increases in total beer consumption.",
        "",
        f"Even a relatively mild $10 ceiling, still below the {_format_currency(baseline['beer_price'])} benchmark beer price, raises tickets {_format_pct(ceiling_summary['10']['ticket_pct_change'])} and total beer consumption {_format_pct(ceiling_summary['10']['beers_pct_change'])}.",
        "",
    ]
    ceiling_lines.extend(
        f"- At **${label}**, tickets change {_format_pct(stats['ticket_pct_change'])}, attendance changes {_format_pct(stats['attendance_pct_change'])}, and total beer consumption changes {_format_pct(stats['beers_pct_change'])}."
        for label, stats in ceiling_summary.items()
    )
    (output_dir / "ceiling_stringency.md").write_text("\n".join(ceiling_lines) + "\n")

    one_way_rows = [
        [
            row["parameter"],
            row["range"],
            _format_pct_range(row["ticket_change_min"], row["ticket_change_max"]),
            _format_pct_range(row["attendance_change_min"], row["attendance_change_max"]),
            _format_pct_range(row["beer_change_min"], row["beer_change_max"]),
        ]
        for row in one_way_sensitivity
    ]
    ticket_friction_rows = [
        [
            str(row["case"]),
            _format_currency(float(row["ticket_price"])),
            _format_pct(float(row["attendance_change"])),
            _format_pct(float(row["beer_change"])),
            _format_pct(float(row["profit_change"])),
        ]
        for row in ticket_friction
    ]
    robustness = "\n".join(
        [
            "The qualitative results are informative, but not unconditional.",
            "",
            "The first check varies one parameter at a time without recalibrating the other moments. This is not a probability model over parameters; it is a transparent stress test around the benchmark, including low internal crowd-cost cases where the ticket response is mechanically weaker.",
            "",
            _markdown_table(
                [
                    "Parameter",
                    "Range",
                    "Ticket",
                    "Attendance",
                    "Beers",
                ],
                one_way_rows,
            ),
            "",
            "The next check constrains ticket repricing under the $6 ceiling. Beer consumption still rises when ticket repricing is limited, but the profit effect becomes much larger because the venue cannot fully move to the unconstrained ticket margin.",
            "",
            _markdown_table(
                ["Ticket case", "Ticket", "Attendance", "Beers", "Profit"],
                ticket_friction_rows,
            ),
            "",
            "Each Monte Carlo draw independently varies the drinker share from 30% to 50%, drinker beer demand from 2.0 to 3.5 beers at the benchmark price, the beer cap from 5 to 10 beers, ticket cost from $3.00 to $4.00, beer cost from $1.50 to $2.50, the internal crowd cost from 0 to 160, ticket-price sensitivity from 0.010 to 0.016, the crime externality from $1.50 to $3.50 per beer, and the health externality from $1.00 to $2.00 per beer.",
            "",
            f"Across {monte_carlo['draws']:,} draws, ticket prices rise in {monte_carlo['ticket_up_share']:.0f}% of draws and total beer consumption rises in {monte_carlo['beers_up_share']:.0f}% of draws. Profit falls in {monte_carlo['profit_down_share']:.0f}% of draws, which is mostly a feasibility check because the ceiling constrains the venue's choice set. Social welfare falls in {monte_carlo['welfare_down_share']:.0f}% of draws.",
            "",
            f"- Intensive margin: {decomposition['intensive_pct_of_baseline']:+.1f}% of baseline beer consumption.",
            f"- Extensive margin: {decomposition['extensive_pct_of_baseline']:+.1f}% of baseline beer consumption.",
            f"- Monte Carlo ticket-price change p10/p50/p90: {_format_pct(monte_carlo['ticket_pct_p10'])}, {_format_pct(monte_carlo['ticket_pct_p50'])}, {_format_pct(monte_carlo['ticket_pct_p90'])}.",
            f"- Monte Carlo beer-consumption change p10/p50/p90: {_format_pct(monte_carlo['beer_pct_p10'])}, {_format_pct(monte_carlo['beer_pct_p50'])}, {_format_pct(monte_carlo['beer_pct_p90'])}.",
            f"- Monte Carlo welfare change p10/p50/p90: {_format_pct(monte_carlo['welfare_pct_p10'])}, {_format_pct(monte_carlo['welfare_pct_p50'])}, {_format_pct(monte_carlo['welfare_pct_p90'])}.",
        ]
    )
    (output_dir / "robustness.md").write_text(robustness + "\n")

    credibility_lines = "\n".join(
        [
            f"- Baseline attendance is {credibility['baseline_attendance_share'] * 100:.1f}% of capacity.",
            f"- Drinkers consume {credibility['baseline_drinker_beers']:.2f} beers at the benchmark price.",
            f"- Drinker share rises from {credibility['baseline_drinker_share'] * 100:.1f}% to {credibility['ceiling_6_drinker_share'] * 100:.1f}% under the $6 ceiling.",
            "- These are calibration checks rather than independent validation moments. They document the benchmark region of the parameter space used for the mechanism exercise.",
        ]
    )
    (output_dir / "credibility.md").write_text(credibility_lines + "\n")

    calibration_sources = "\n".join(
        [
            "The calibration uses public or literature-based moments rather than transaction-level Yankees data. The moments are deliberately rounded because the point of the exercise is the joint-pricing mechanism, not a claim to estimate exact Yankees demand.",
            "",
            _markdown_table(
                ["Input", "Benchmark value", "Rationale"],
                [
                    [
                        "Beer price",
                        _format_currency(calibration["target_beer_price"]),
                        "Public concession-price reporting and the policy debate motivating the exercise [@semafor2025khan].",
                    ],
                    [
                        "Ticket price",
                        _format_currency(calibration["target_ticket_price"]),
                        "Round benchmark for the effective ticket price faced by a marginal attendee; treated as a calibration target rather than a microdata estimate.",
                    ],
                    [
                        "Capacity utilization",
                        _format_percent_level(calibration["target_attendance_share"]),
                        "High-demand regular-season benchmark; the exact attendance level matters less than the implied local ticket elasticity.",
                    ],
                    [
                        "Drinker share",
                        f"{credibility['baseline_drinker_share'] * 100:.0f}%",
                        "Anchored to stadium alcohol-use evidence showing substantial but far from universal drinking among MLB spectators [@wolfe1998baseball].",
                    ],
                    [
                        "Beers per attendee",
                        f"{calibration['target_beers_per_fan']:.2f}",
                        "Chosen so the aggregate benchmark combines the drinker share with 2.5 beers per drinker.",
                    ],
                    [
                        "Beer cap",
                        "6.5 beers",
                        "Upper bound on per-person beer demand used consistently in the demand and beer-surplus formulas.",
                    ],
                    [
                        "Internal crowd cost",
                        f"{_format_currency(calibration['experience_degradation_cost'])} per squared thousand beers",
                        "Coefficient in C(Q)=k(Q/1000)^2. The main ticket-response mechanism is conditional on this private crowd-management and experience-degradation value and is stress-tested below.",
                    ],
                    [
                        "Alcohol external costs",
                        "$4.00 per beer",
                        "Imported from broader alcohol-policy evidence; used for welfare accounting, not for the private-pricing mechanism [@manning1991costs; @carpenter2015mlda].",
                    ],
                ],
            ),
            "",
            "The two calibrated structural parameters are the semi-log ticket sensitivity and the internalized experience-degradation cost. They are chosen jointly so that the unconstrained venue optimum reproduces the benchmark ticket and beer prices.",
        ]
    )
    (output_dir / "calibration_sources.md").write_text(calibration_sources + "\n")

    limitations = "\n".join(
        [
            "- The paper is a calibrated mechanism exercise using public price and attendance targets rather than proprietary transaction-level Yankees data.",
            "- The demand side uses two consumer types, which captures composition effects but not the full distribution of fan preferences or outside options.",
            "- The model is static and partial-equilibrium, so it abstracts from pregame drinking, nearby bars, repeat attendance, and long-run reputation effects.",
            "- The policy experiments assume perfect enforcement and do not model evasive responses such as flask-smuggling, bootlegging, or accelerated pregame drinking in response to the ceiling.",
            "- The benchmark ticket increase depends materially on calibrated private crowd-management and experience-degradation costs; low-cost variants are reported as stress tests rather than ruled out by direct Yankees data.",
            "- The ticket price is assumed to be freely re-optimized for the representative game; the model abstracts from season tickets, resale markets, dynamic pricing frictions, and fan backlash from sudden repricing.",
            "- Attendance is capped at stadium capacity, but the main ceiling counterfactuals only move attendance downward, so the paper is not informative about policies that would push demand back against the capacity constraint.",
            "- External costs are imported from the alcohol-policy literature rather than estimated around Yankee Stadium itself.",
        ]
    )
    (output_dir / "limitations.md").write_text(limitations + "\n")

    calibration_rows = [
        [
            "Ticket price",
            _format_currency(calibration["target_ticket_price"]),
            _format_currency(baseline["ticket_price"]),
            "Direct benchmark target",
        ],
        [
            "Beer price",
            _format_currency(calibration["target_beer_price"]),
            _format_currency(baseline["beer_price"]),
            "Direct benchmark target",
        ],
        [
            "Attendance share",
            _format_percent_level(calibration["target_attendance_share"]),
            _format_percent_level(credibility["baseline_attendance_share"]),
            "Capacity utilization target",
        ],
        [
            "Beers per attendee",
            f"{calibration['target_beers_per_fan']:.2f}",
            f"{baseline['beers_per_fan']:.2f}",
            "Aggregate consumption target",
        ],
        [
            "Beers per drinker",
            f"{calibration['target_drinker_beers']:.2f}",
            f"{credibility['baseline_drinker_beers']:.2f}",
            "Type-specific consumption target",
        ],
        [
            "Ticket elasticity at $80",
            "n/a",
            f"{calibration['ticket_elasticity_at_80']:.2f}",
            "Implied by calibrated attendance sensitivity",
        ],
    ]
    (output_dir / "calibration_table.md").write_text(
        _markdown_table(["Moment", "Target", "Model", "Notes"], calibration_rows) + "\n"
    )

    policy_rows = [
        [
            "Baseline",
            _format_currency(baseline["ticket_price"]),
            _format_currency(baseline["beer_price"]),
            f"{baseline['attendance']:,.0f}",
            f"{baseline['drinker_share_attendance'] * 100:.1f}%",
            f"{baseline['total_beers']:,.0f}",
        ],
        [
            "$10 ceiling",
            _format_currency(ceiling_10["ticket_price"]),
            _format_currency(ceiling_10["beer_price"]),
            f"{ceiling_10['attendance']:,.0f}",
            f"{ceiling_10['drinker_share_attendance'] * 100:.1f}%",
            f"{ceiling_10['total_beers']:,.0f}",
        ],
        [
            "$8 ceiling",
            _format_currency(ceiling_8["ticket_price"]),
            _format_currency(ceiling_8["beer_price"]),
            f"{ceiling_8['attendance']:,.0f}",
            f"{ceiling_8['drinker_share_attendance'] * 100:.1f}%",
            f"{ceiling_8['total_beers']:,.0f}",
        ],
        [
            "$6 ceiling",
            _format_currency(ceiling_6["ticket_price"]),
            _format_currency(ceiling_6["beer_price"]),
            f"{ceiling_6['attendance']:,.0f}",
            f"{ceiling_6['drinker_share_attendance'] * 100:.1f}%",
            f"{ceiling_6['total_beers']:,.0f}",
        ],
        [
            "$5 ceiling",
            _format_currency(ceiling_5["ticket_price"]),
            _format_currency(ceiling_5["beer_price"]),
            f"{ceiling_5['attendance']:,.0f}",
            f"{ceiling_5['drinker_share_attendance'] * 100:.1f}%",
            f"{ceiling_5['total_beers']:,.0f}",
        ],
    ]
    (output_dir / "policy_cases_table.md").write_text(
        _markdown_table(
            [
                "Case",
                "Ticket",
                "Beer",
                "Attendance",
                "Drinker Share",
                "Total Beers",
            ],
            policy_rows,
        )
        + "\n"
    )


def write_submission_materials(context: dict[str, Any], output_dir: Path) -> None:
    """Write copy-ready SSRN and journal submission materials."""
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline = context["baseline"]
    ceiling_6 = context["ceiling_6"]
    credibility = context["credibility"]

    abstract = " ".join(
        [
            "Sports venues jointly price tickets and concessions.",
            "This paper asks how a profit-maximizing venue responds when regulators cap beer prices but leave tickets unconstrained.",
            "I build a calibrated partial-equilibrium model of Yankee Stadium with drinkers and non-drinkers, utility-consistent beer demand, and attendance that responds to beer consumer surplus.",
            f"The benchmark matches an {_format_currency(baseline['ticket_price'], 0)} ticket, a {_format_currency(baseline['beer_price'])} beer, {_format_percent_level(credibility['baseline_attendance_share'])} capacity use, and {baseline['beers_per_fan']:.2f} beers per attendee.",
            f"Under a binding $6 ceiling, the stadium raises tickets to {_format_currency(ceiling_6['ticket_price'], 0)}, attendance falls to {ceiling_6['attendance']:,.0f}, and beer sales rise {_format_pct(_pct_change(ceiling_6['total_beers'], baseline['total_beers']))}.",
            "The mechanism is joint pricing: cheaper beer changes both intensive drinking and attendee composition.",
            "The exercise is not causal, but it suggests that concession price ceilings may be poorly targeted when alcohol harms are the policy concern.",
        ]
    )

    ssrn_metadata = "\n".join(
        [
            "# SSRN Metadata",
            "",
            f"**Title:** {PAPER_TITLE}",
            "",
            f"**Author:** {AUTHOR_NAME}",
            "",
            f"**Affiliation:** {AUTHOR_AFFILIATION}",
            "",
            f"**Email:** {AUTHOR_EMAIL}",
            "",
            f"**Keywords:** {', '.join(PAPER_KEYWORDS)}",
            "",
            f"**JEL Codes:** {', '.join(PAPER_JEL_CODES)}",
            "",
            "**Abstract:**",
            "",
            abstract,
            "",
            "**Suggested One-Line Summary:**",
            "",
            "A calibrated Yankee Stadium model suggests that beer price ceilings can backfire once the venue re-optimizes ticket prices.",
        ]
    )
    (output_dir / "ssrn_metadata.md").write_text(ssrn_metadata + "\n")

    letter_date = _format_letter_date()
    jse_letter = [
        letter_date,
        "",
        "Dear Editor,",
        "",
        f'I am pleased to submit "{PAPER_TITLE}" for your consideration.',
        "",
        "The paper studies how a profit-maximizing sports venue responds when regulation caps concession prices but leaves ticket prices unconstrained. It adds a simple ticket-markup condition showing how concession margins and beer-related crowd costs enter optimal ticket pricing, then applies that mechanism in a calibrated Yankee Stadium model.",
        "",
        "The manuscript is explicit about its scope. It is a calibrated mechanism paper rather than a reduced-form causal estimate. Its contribution is to illustrate how partial price regulation can backfire in a joint-pricing setting and to deliver that argument with transparent calibration, targeted sensitivity checks, and fully reproducible outputs.",
        "",
        "I believe the paper fits Journal of Sports Economics because it combines a sports-venue application with a clear pricing and regulation mechanism. The manuscript is original, is not under consideration elsewhere, and the accompanying code reproduces the reported tables and figures.",
        "",
        "Thank you for your consideration.",
        "",
        AUTHOR_NAME,
        AUTHOR_EMAIL,
    ]
    (output_dir / "cover_letter_journal_of_sports_economics.md").write_text(
        "\n".join(jse_letter) + "\n"
    )

    ijsf_letter = [
        letter_date,
        "",
        "Dear Editor,",
        "",
        f'I am pleased to submit "{PAPER_TITLE}" for your consideration.',
        "",
        "The paper studies how a profit-maximizing sports venue responds when regulation caps concession prices but leaves ticket prices unconstrained. It adds a simple ticket-markup condition showing how concession margins and beer-related crowd costs enter optimal ticket pricing, then applies that mechanism in a calibrated Yankee Stadium model.",
        "",
        "The manuscript is explicit about its scope. It is a calibrated mechanism paper rather than a reduced-form causal estimate. Its contribution is to illustrate how partial price regulation can backfire in a joint-pricing setting and to deliver that argument with transparent calibration, targeted sensitivity checks, and fully reproducible outputs.",
        "",
        "I believe the paper fits International Journal of Sport Finance because it focuses directly on venue pricing, concession policy, and the revenue trade-offs facing a sports franchise. The manuscript is original, is not under consideration elsewhere, and the accompanying code reproduces the reported tables and figures.",
        "",
        "Thank you for your consideration.",
        "",
        AUTHOR_NAME,
        AUTHOR_EMAIL,
    ]
    (output_dir / "cover_letter_international_journal_of_sport_finance.md").write_text(
        "\n".join(ijsf_letter) + "\n"
    )

    readme_lines = [
        "# Submission Bundle",
        "",
        "- `ssrn_metadata.md`: copy-ready SSRN title, abstract, keywords, and JEL codes.",
        "- `cover_letter_journal_of_sports_economics.md`: default first-pass journal cover letter.",
        "- `cover_letter_international_journal_of_sport_finance.md`: fallback niche-journal cover letter.",
        "",
        "Recommended order:",
        "",
        "1. Post the PDF on SSRN.",
        "2. Submit the same manuscript to Journal of Sports Economics.",
        "3. If needed, make a light revision and send it to International Journal of Sport Finance.",
        "",
        "Before sending, replace the greeting line with the journal's actual editor name if available.",
    ]
    (output_dir / "README.md").write_text("\n".join(readme_lines) + "\n")


def build_paper_artifacts(output_dir: str | Path, draws: int = 1000) -> dict[str, Any]:
    """Generate markdown fragments, context, and figures for Quarto."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    context = compute_report_context(draws=draws)
    (output_path / "context.json").write_text(json.dumps(context, indent=2))
    write_markdown_artifacts(context, output_path)

    chart_model = StadiumEconomicModel()
    chart_df = simulate_price_ceilings(np.linspace(5.0, 13.0, 17), chart_model)
    create_charts(chart_df, output_dir=output_path / "charts", model=chart_model)

    return context


def build_submission_bundle(output_dir: str | Path, draws: int = 1000) -> dict[str, Any]:
    """Generate copy-ready materials for SSRN and journal submission."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    context = compute_report_context(draws=draws)
    write_submission_materials(context, output_path)
    return context


def render_quarto_project(project_dir: str | Path = "paper", draws: int = 1000) -> None:
    """Build paper artifacts and render the Quarto project."""
    quarto_binary = shutil.which("quarto")
    if quarto_binary is None:
        raise RuntimeError(
            "Quarto CLI is required to render the paper. Install Quarto and ensure "
            "`quarto` is on PATH, or run `yankee-beer-paper build` to generate "
            "the markdown artifacts without rendering."
        )

    project_path = _ensure_paper_project(project_dir)
    build_paper_artifacts(project_path / "_generated", draws=draws)
    subprocess.run([quarto_binary, "render", str(project_path)], check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Quarto-ready paper artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Write markdown fragments and charts.")
    build_parser.add_argument("--output-dir", default="paper/_generated")
    build_parser.add_argument("--draws", type=int, default=1000)

    render_parser = subparsers.add_parser("render", help="Build artifacts and render Quarto.")
    render_parser.add_argument("--project-dir", default="paper")
    render_parser.add_argument("--draws", type=int, default=1000)

    submission_parser = subparsers.add_parser(
        "submission",
        help="Write SSRN metadata and journal cover letters.",
    )
    submission_parser.add_argument("--output-dir", default="submissions")
    submission_parser.add_argument("--draws", type=int, default=1000)

    args = parser.parse_args(argv)

    if args.command == "build":
        build_paper_artifacts(args.output_dir, draws=args.draws)
        return 0

    if args.command == "render":
        render_quarto_project(args.project_dir, draws=args.draws)
        return 0

    if args.command == "submission":
        build_submission_bundle(args.output_dir, draws=args.draws)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
