import type { ReactNode } from "react";

import { loadDashboardContext, type DashboardContext, type ScenarioSummary } from "@/lib/model-context";

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

const wholeCurrency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

const wholeNumber = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 0,
});

const oneDecimal = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

function formatPercent(value: number, suffix = "%"): string {
  const formatter = new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
    signDisplay: "exceptZero",
  });

  return `${formatter.format(value)}${suffix}`;
}

function Badge({ children }: { children: ReactNode }) {
  return (
    <span className="rounded-full border border-[color:var(--line)] bg-white/60 px-3 py-1 text-[0.72rem] font-semibold uppercase tracking-[0.22em] text-[color:var(--muted)]">
      {children}
    </span>
  );
}

function StatCard({
  label,
  value,
  detail,
}: {
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <article className="card-shadow rounded-[1.5rem] border border-[color:var(--line)] bg-[color:var(--panel)] p-5 reveal">
      <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[color:var(--muted)]">
        {label}
      </p>
      <p className="mt-4 font-display text-3xl text-[color:var(--ink)] md:text-4xl">{value}</p>
      <p className="mt-3 text-sm leading-6 text-[color:var(--muted)]">{detail}</p>
    </article>
  );
}

function MetricRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 border-t border-[color:var(--line)] py-3 first:border-t-0 first:pt-0 last:pb-0">
      <dt className="text-sm text-[color:var(--muted)]">{label}</dt>
      <dd className="text-right text-sm font-semibold text-[color:var(--ink)]">{value}</dd>
    </div>
  );
}

function ScenarioCard({
  eyebrow,
  title,
  accentClass,
  scenario,
}: {
  eyebrow: string;
  title: string;
  accentClass: string;
  scenario: ScenarioSummary;
}) {
  const drinkerAttendance = scenario.breakdown_by_type["Drinker"]?.attendance ?? 0;
  const nonDrinkerAttendance = scenario.breakdown_by_type["Non-Drinker"]?.attendance ?? 0;

  return (
    <article className="card-shadow rounded-[1.75rem] border border-[color:var(--line)] bg-[color:var(--panel)] p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[color:var(--muted)]">
            {eyebrow}
          </p>
          <h2 className="mt-3 font-display text-3xl text-[color:var(--ink)]">{title}</h2>
        </div>
        <div className={`h-14 w-3 rounded-full ${accentClass}`} />
      </div>

      <dl className="mt-8 space-y-1">
        <MetricRow label="Ticket price" value={currency.format(scenario.ticket_price)} />
        <MetricRow label="Beer price" value={currency.format(scenario.beer_price)} />
        <MetricRow label="Attendance" value={wholeNumber.format(scenario.attendance)} />
        <MetricRow label="Beers per fan" value={oneDecimal.format(scenario.beers_per_fan)} />
        <MetricRow label="Total beers" value={wholeNumber.format(scenario.total_beers)} />
        <MetricRow label="Profit" value={wholeCurrency.format(scenario.profit)} />
        <MetricRow label="Social welfare" value={wholeCurrency.format(scenario.social_welfare)} />
      </dl>

      <div className="mt-8 grid gap-3 sm:grid-cols-2">
        <div className="rounded-2xl bg-white/60 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[color:var(--muted)]">
            Drinker attendance
          </p>
          <p className="mt-3 font-display text-2xl text-[color:var(--ink)]">
            {wholeNumber.format(drinkerAttendance)}
          </p>
        </div>
        <div className="rounded-2xl bg-white/60 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[color:var(--muted)]">
            Non-drinker attendance
          </p>
          <p className="mt-3 font-display text-2xl text-[color:var(--ink)]">
            {wholeNumber.format(nonDrinkerAttendance)}
          </p>
        </div>
      </div>
    </article>
  );
}

function StringencyRow({
  label,
  ticketShift,
  beerShift,
  ticketWidth,
  beerWidth,
}: {
  label: string;
  ticketShift: number;
  beerShift: number;
  ticketWidth: number;
  beerWidth: number;
}) {
  return (
    <div className="rounded-[1.4rem] border border-[color:var(--line)] bg-white/60 p-4">
      <div className="flex items-center justify-between gap-4">
        <h3 className="font-display text-2xl text-[color:var(--ink)]">{label}</h3>
        <p className="text-sm text-[color:var(--muted)]">Binding ceiling</p>
      </div>

      <div className="mt-5 space-y-4">
        <div>
          <div className="mb-2 flex items-center justify-between gap-4 text-sm">
            <span className="text-[color:var(--muted)]">Ticket price</span>
            <span className="font-semibold text-[color:var(--ink)]">{formatPercent(ticketShift)}</span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-[color:var(--line)]">
            <div
              className="h-full rounded-full bg-[color:var(--navy)]"
              style={{ width: `${ticketWidth}%` }}
            />
          </div>
        </div>

        <div>
          <div className="mb-2 flex items-center justify-between gap-4 text-sm">
            <span className="text-[color:var(--muted)]">Total beer consumption</span>
            <span className="font-semibold text-[color:var(--ink)]">{formatPercent(beerShift)}</span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-[color:var(--line)]">
            <div
              className="h-full rounded-full bg-[color:var(--amber)]"
              style={{ width: `${beerWidth}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function CredibilityPanel({ context }: { context: DashboardContext }) {
  return (
    <section className="card-shadow rounded-[1.9rem] border border-[color:var(--line)] bg-[color:var(--panel)] p-6">
      <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[color:var(--muted)]">
        Credibility
      </p>
      <h2 className="mt-3 font-display text-4xl text-[color:var(--ink)]">Why the mechanism is at least disciplined</h2>

      <div className="mt-8 space-y-4">
        <div className="rounded-2xl bg-white/60 p-4">
          <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-[color:var(--muted)]">
            Calibration targets
          </h3>
          <p className="mt-3 text-sm leading-6 text-[color:var(--ink)]">
            The benchmark reproduces an {currency.format(context.baseline.ticket_price)} ticket, a{" "}
            {currency.format(context.baseline.beer_price)} beer, and{" "}
            {formatPercent(context.credibility.baseline_attendance_share * 100, "% of capacity")} attendance.
          </p>
        </div>

        <div className="rounded-2xl bg-white/60 p-4">
          <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-[color:var(--muted)]">
            Utility-consistent demand
          </h3>
          <p className="mt-3 text-sm leading-6 text-[color:var(--ink)]">
            Drinkers buy about {oneDecimal.format(context.credibility.baseline_drinker_beers)} beers at the
            benchmark price, and beer affects attendance through consumer surplus rather than an ad hoc
            cross-price elasticity.
          </p>
        </div>

        <div className="rounded-2xl bg-white/60 p-4">
          <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-[color:var(--muted)]">
            Sign robustness
          </h3>
          <p className="mt-3 text-sm leading-6 text-[color:var(--ink)]">
            Across {wholeNumber.format(context.monte_carlo.draws)} Monte Carlo draws, ticket prices rise in{" "}
            {formatPercent(context.monte_carlo.ticket_up_share)}, profit falls in{" "}
            {formatPercent(context.monte_carlo.profit_down_share)}, and total beer consumption rises in{" "}
            {formatPercent(context.monte_carlo.beers_up_share)}.
          </p>
        </div>

        <div className="rounded-2xl border border-dashed border-[color:var(--line-strong)] bg-[color:var(--paper)] p-4">
          <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-[color:var(--muted)]">
            Still missing
          </h3>
          <p className="mt-3 text-sm leading-6 text-[color:var(--ink)]">
            This is still a calibrated mechanism model, not a reduced-form estimate. The biggest remaining
            gaps are transaction-level Yankees data, richer fan heterogeneity, and substitution to outside
            drinking options.
          </p>
        </div>
      </div>
    </section>
  );
}

function EmptyState() {
  return (
    <div className="card-shadow rounded-[1.9rem] border border-dashed border-[color:var(--line-strong)] bg-[color:var(--panel)] p-6">
      <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[color:var(--muted)]">
        Data missing
      </p>
      <h2 className="mt-3 font-display text-4xl text-[color:var(--ink)]">Generate the shared model payload first</h2>
      <p className="mt-4 max-w-2xl text-sm leading-7 text-[color:var(--muted)]">
        The app reads packaged model output from <code className="rounded bg-white/70 px-1 py-0.5">web/public/data/context.json</code>.
        Run <code className="rounded bg-white/70 px-1 py-0.5">uv run yankee-beer-web-data --output-dir web/public/data</code> and reload the page.
      </p>
    </div>
  );
}

export default async function Home() {
  const context = await loadDashboardContext();

  if (!context) {
    return (
      <main className="px-4 py-6 md:px-8 md:py-10">
        <div className="mx-auto max-w-6xl">
          <section className="reveal rounded-[2rem] border border-[color:var(--line)] bg-[color:var(--panel)] px-6 py-8 md:px-10 md:py-12">
            <Badge>Packaged model</Badge>
            <h1 className="mt-6 max-w-4xl font-display text-5xl leading-none text-[color:var(--ink)] md:text-7xl">
              A browser layer for the stadium model, without re-implementing the economics.
            </h1>
            <p className="mt-6 max-w-3xl text-base leading-8 text-[color:var(--muted)] md:text-lg">
              The Quarto paper and the web app now share the same generated context. The UI is just a view over
              packaged output, which keeps the analysis path single-sourced.
            </p>
          </section>

          <div className="mt-8">
            <EmptyState />
          </div>
        </div>
      </main>
    );
  }

  const ceilingLevels = ["10", "8", "6", "5"] as const;
  const maxTicketShift = Math.max(...ceilingLevels.map((level) => context.ceiling_summary[level].ticket_pct_change));
  const maxBeerShift = Math.max(...ceilingLevels.map((level) => context.ceiling_summary[level].beers_pct_change));

  return (
    <main className="px-4 py-6 md:px-8 md:py-10">
      <div className="mx-auto max-w-6xl">
        <section className="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <div className="card-shadow reveal rounded-[2rem] border border-[color:var(--line)] bg-[color:var(--panel)] px-6 py-8 md:px-10 md:py-12">
            <div className="flex flex-wrap gap-3">
              <Badge>Next.js</Badge>
              <Badge>Tailwind CSS</Badge>
              <Badge>Shared JSON pipeline</Badge>
            </div>

            <h1 className="mt-6 max-w-4xl font-display text-5xl leading-none text-[color:var(--ink)] md:text-7xl">
              Cut the beer price and this model pushes the ticket price up instead.
            </h1>

            <p className="mt-6 max-w-3xl text-base leading-8 text-[color:var(--muted)] md:text-lg">
              The stadium is modeled as a joint seller of tickets and concessions. Once beer margins are capped,
              the venue re-optimizes through the remaining instrument. In the calibrated benchmark, that means
              higher ticket prices, lower attendance, and a more drinker-heavy crowd.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <Badge>Baseline ticket {currency.format(context.baseline.ticket_price)}</Badge>
              <Badge>$6 ceiling ticket {currency.format(context.ceiling_6.ticket_price)}</Badge>
              <Badge>Total beers {formatPercent(context.ceiling_summary["6"].beers_pct_change)}</Badge>
            </div>
          </div>

          <aside className="card-shadow reveal rounded-[2rem] border border-[color:var(--line)] bg-[color:var(--panel)] p-6 lg:p-8">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[color:var(--muted)]">
              Headline shift
            </p>
            <h2 className="mt-3 font-display text-4xl text-[color:var(--ink)]">$6 beer ceiling</h2>

            <dl className="mt-8 space-y-1">
              <MetricRow
                label="Ticket price change"
                value={formatPercent(context.ceiling_summary["6"].ticket_pct_change)}
              />
              <MetricRow
                label="Attendance change"
                value={formatPercent(context.ceiling_summary["6"].attendance_pct_change)}
              />
              <MetricRow
                label="Total beer change"
                value={formatPercent(context.ceiling_summary["6"].beers_pct_change)}
              />
              <MetricRow
                label="Drinker share"
                value={`${oneDecimal.format(context.credibility.baseline_drinker_share * 100)}% → ${oneDecimal.format(context.credibility.ceiling_6_drinker_share * 100)}%`}
              />
            </dl>
          </aside>
        </section>

        <section className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard
            label="Baseline ticket"
            value={currency.format(context.baseline.ticket_price)}
            detail={`Profit-maximizing benchmark with ${wholeNumber.format(context.baseline.attendance)} fans.`}
          />
          <StatCard
            label="$6 ceiling ticket"
            value={currency.format(context.ceiling_6.ticket_price)}
            detail="The unconstrained margin shifts toward the entry price rather than concessions."
          />
          <StatCard
            label="Attendance shift"
            value={formatPercent(context.ceiling_summary["6"].attendance_pct_change)}
            detail="A smaller crowd remains once the ticket increase is allowed to clear the market."
          />
          <StatCard
            label="Beer sales shift"
            value={formatPercent(context.ceiling_summary["6"].beers_pct_change)}
            detail="Lower attendance is more than offset by heavier drinking among the remaining attendees."
          />
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-2">
          <ScenarioCard
            eyebrow="Benchmark"
            title="Baseline"
            accentClass="bg-[color:var(--navy)]"
            scenario={context.baseline}
          />
          <ScenarioCard
            eyebrow="Policy shock"
            title="$6 Ceiling"
            accentClass="bg-[color:var(--amber)]"
            scenario={context.ceiling_6}
          />
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <section className="card-shadow rounded-[1.9rem] border border-[color:var(--line)] bg-[color:var(--panel)] p-6">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[color:var(--muted)]">
              Ceiling ladder
            </p>
            <h2 className="mt-3 font-display text-4xl text-[color:var(--ink)]">Tighter ceilings push harder on both margins</h2>

            <div className="mt-8 grid gap-4">
              {ceilingLevels.map((level) => (
                <StringencyRow
                  key={level}
                  label={`$${level}`}
                  ticketShift={context.ceiling_summary[level].ticket_pct_change}
                  beerShift={context.ceiling_summary[level].beers_pct_change}
                  ticketWidth={(context.ceiling_summary[level].ticket_pct_change / maxTicketShift) * 100}
                  beerWidth={(context.ceiling_summary[level].beers_pct_change / maxBeerShift) * 100}
                />
              ))}
            </div>
          </section>

          <CredibilityPanel context={context} />
        </section>
      </div>
    </main>
  );
}
