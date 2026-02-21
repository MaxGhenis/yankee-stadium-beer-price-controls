"""
Streamlit app for beer price control simulation at Yankee Stadium.

Interactive tool to explore economic impacts of beer pricing policies
on consumer welfare, stadium revenue, attendance, and externalities.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator

st.set_page_config(
    page_title="Yankee Stadium Beer Price Controls",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-header { font-size: 2.5rem; color: #003087; text-align: center; padding: 1rem 0; }
    .sub-header { font-size: 1.2rem; color: #E4002B; text-align: center; padding-bottom: 2rem; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="main-header">🍺 Beer Price Controls at Yankee Stadium</h1>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">An Economic Analysis of Consumer Welfare, Revenue, and Externalities</p>',
    unsafe_allow_html=True,
)

# Sidebar - Model Parameters
st.sidebar.header("📊 Model Parameters")

st.sidebar.subheader("Stadium Characteristics")
capacity = st.sidebar.number_input("Stadium Capacity", min_value=10000, max_value=100000, value=46537, step=1000)

st.sidebar.subheader("Baseline Prices")
base_ticket_price = st.sidebar.slider("Base Ticket Price ($)", 20.0, 200.0, 80.0, 5.0)
base_beer_price = st.sidebar.slider("Base Beer Price ($)", 5.0, 25.0, 12.5, 0.5)

st.sidebar.subheader("Cost Parameters")
ticket_cost = st.sidebar.slider("Marginal Cost per Ticket ($)", 1.0, 20.0, 3.5, 0.5)
beer_cost = st.sidebar.slider("Marginal Cost per Beer ($)", 0.5, 10.0, 2.0, 0.5)

st.sidebar.subheader("Internalized Costs (Stadium)")
experience_degradation_cost = st.sidebar.slider(
    "Experience Degradation Cost (k)", 50.0, 500.0, 126.7, 10.0,
    help="Convex cost parameter: C = k·(Q/1000)²",
)

st.sidebar.subheader("Externality Costs (Society)")
crime_cost_per_beer = st.sidebar.slider("Crime Cost per Beer ($)", 0.0, 10.0, 2.5, 0.5)
health_cost_per_beer = st.sidebar.slider("Health Cost per Beer ($)", 0.0, 10.0, 1.5, 0.5)

# Policy Scenarios
st.header("🎯 Policy Scenarios")

col1, col2 = st.columns(2)
with col1:
    price_ceiling = st.slider("Price Ceiling (Maximum Beer Price) ($)", 5.0, 20.0, 8.0, 0.5)
with col2:
    price_floor = st.slider("Price Floor (Minimum Beer Price) ($)", 10.0, 30.0, 15.0, 0.5)


@st.cache_data
def create_model(capacity, base_ticket_price, base_beer_price, ticket_cost, beer_cost, experience_degradation_cost):
    return StadiumEconomicModel(
        capacity=capacity,
        base_ticket_price=base_ticket_price,
        base_beer_price=base_beer_price,
        ticket_cost=ticket_cost,
        beer_cost=beer_cost,
        experience_degradation_cost=experience_degradation_cost,
    )


model = create_model(capacity, base_ticket_price, base_beer_price, ticket_cost, beer_cost, experience_degradation_cost)
simulator = BeerPriceControlSimulator(model)

with st.spinner("Running simulations..."):
    results_df = simulator.run_all_scenarios(
        price_ceiling=price_ceiling,
        crime_cost_per_beer=crime_cost_per_beer,
        health_cost_per_beer=health_cost_per_beer,
    )

# Ticket Price Response
st.header("📈 Results Summary")
st.subheader("🎯 Key Finding: Ticket Price Response to Beer Ceiling")

t_ceiling, b_ceiling, r_ceiling = model.optimal_pricing(beer_price_control=price_ceiling)
t_current, b_current, r_current = model.optimal_pricing(beer_price_control=base_beer_price)

ticket_change = t_ceiling - t_current
ticket_pct = (ticket_change / t_current) * 100
multiplier = abs(ticket_change / (price_ceiling - base_beer_price)) if price_ceiling != base_beer_price else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Optimal Tickets", f"${t_current:.2f}")
with col2:
    st.metric(f"With ${price_ceiling} Beer Ceiling", f"${t_ceiling:.2f}", f"{ticket_change:+.2f} ({ticket_pct:+.1f}%)")
with col3:
    st.metric("Price Adjustment Multiplier", f"{multiplier:.1f}x")

st.info(f"""
**Economic mechanism**: When beer revenue is constrained, stadium shifts toward ticket revenue.
With endogenous cross-price effects:
- Cheaper beer raises drinker CS, partially offsetting higher tickets
- Attendance falls {((r_ceiling['attendance']/r_current['attendance'] - 1) * 100):.1f}%
- Stadium raises tickets {ticket_pct:.1f}% to compensate
- Total revenue still falls {((r_ceiling['total_revenue']/r_current['total_revenue'] - 1) * 100):.1f}%
""")

st.divider()

# Baseline Metrics
st.subheader("📊 Baseline Metrics")
baseline = results_df[results_df["scenario"] == "Current Observed Prices"].iloc[0]
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Baseline Attendance", f"{baseline['attendance']:,.0f}")
with col2:
    st.metric("Baseline Total Beers", f"{baseline['total_beers']:,.0f}")
with col3:
    st.metric("Baseline Profit", f"${baseline['profit']:,.0f}")
with col4:
    st.metric("Baseline Social Welfare", f"${baseline['social_welfare']:,.0f}")

# Results table
st.subheader("Detailed Results by Scenario")
display_df = results_df[["scenario", "ticket_price", "beer_price", "attendance", "total_beers", "total_revenue", "profit", "consumer_surplus", "externality_cost", "social_welfare"]].copy()
for col in ["ticket_price", "beer_price"]:
    display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")
for col in ["attendance", "total_beers"]:
    display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}")
for col in ["total_revenue", "profit", "consumer_surplus", "externality_cost", "social_welfare"]:
    display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
st.dataframe(display_df, use_container_width=True)

# Visualizations
st.header("📊 Visualizations")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Revenue & Welfare", "Attendance & Consumption", "Price Comparison", "Externalities", "Price Ceiling Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Bar(x=results_df["scenario"], y=results_df["profit"], name="Stadium Profit", marker_color="#003087"))
        fig_revenue.update_layout(title="Stadium Profit by Scenario", xaxis_title="Scenario", yaxis_title="Profit ($)", height=400)
        st.plotly_chart(fig_revenue, use_container_width=True)
    with col2:
        fig_welfare = go.Figure()
        fig_welfare.add_trace(go.Bar(x=results_df["scenario"], y=results_df["social_welfare"], name="Social Welfare", marker_color="#E4002B"))
        fig_welfare.update_layout(title="Social Welfare by Scenario", xaxis_title="Scenario", yaxis_title="Social Welfare ($)", height=400)
        st.plotly_chart(fig_welfare, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=results_df["scenario"], y=results_df["attendance"], marker_color="#003087"))
        fig.update_layout(title="Attendance by Scenario", height=400)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=results_df["scenario"], y=results_df["total_beers"], marker_color="#E4002B"))
        fig.update_layout(title="Total Beer Consumption by Scenario", height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=results_df["scenario"], y=results_df["ticket_price"], mode="lines+markers", name="Ticket Price", line=dict(color="#003087", width=3)))
    fig.add_trace(go.Scatter(x=results_df["scenario"], y=results_df["beer_price"], mode="lines+markers", name="Beer Price", line=dict(color="#E4002B", width=3), yaxis="y2"))
    fig.update_layout(title="Prices by Scenario", yaxis_title="Ticket Price ($)", yaxis2=dict(title="Beer Price ($)", overlaying="y", side="right"), height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=results_df["scenario"], y=results_df["externality_cost"], marker_color="darkred"))
    fig.update_layout(title="Total Externality Costs by Scenario", height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("📈 Price Ceiling Comparative Statics")
    ceiling_range = np.linspace(5, 20, 31)
    ceiling_results = []
    with st.spinner("Computing price ceiling analysis..."):
        for ceiling in ceiling_range:
            t_p, b_p, rev = model.optimal_pricing(beer_price_control=ceiling, ceiling_mode=True)
            welf = model.social_welfare(t_p, b_p)
            ceiling_results.append({
                "ceiling": ceiling, "ticket_price": t_p, "beer_price": b_p,
                "attendance": rev["attendance"], "beers_per_fan": rev["beers_per_fan"],
                "total_beers": rev["total_beers"], "profit": rev["profit"],
                "consumer_surplus": welf["consumer_surplus"],
                "externality_cost": welf["externality_cost"],
                "social_welfare": welf["social_welfare"],
            })

    ceiling_df = pd.DataFrame(ceiling_results)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ceiling_df["ceiling"], y=ceiling_df["ticket_price"], mode="lines+markers", line=dict(color="#003087", width=3)))
        fig.add_hline(y=base_ticket_price, line_dash="dash", line_color="gray")
        fig.update_layout(title="Ticket Prices Rise as Beer Ceiling Tightens", xaxis_title="Beer Price Ceiling ($)", yaxis_title="Optimal Ticket Price ($)", height=400)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ceiling_df["ceiling"], y=ceiling_df["beer_price"], mode="lines+markers", line=dict(color="#E4002B", width=3)))
        fig.add_trace(go.Scatter(x=ceiling_df["ceiling"], y=ceiling_df["ceiling"], mode="lines", name="Ceiling", line=dict(color="gray", dash="dash")))
        fig.update_layout(title="Beer Price Tracks Ceiling", xaxis_title="Beer Price Ceiling ($)", yaxis_title="Beer Price ($)", height=400)
        st.plotly_chart(fig, use_container_width=True)

# Comparative analysis
st.header("🔍 Comparative Analysis")
changes_df = simulator.calculate_comparative_statics(results_df)
st.subheader("Changes Relative to Current Prices")
comparison_cols = ["scenario", "profit_change", "social_welfare_change", "attendance_change", "total_beers_change", "externality_cost_change"]
comparison_df = changes_df[comparison_cols].copy()
for col in comparison_cols[1:]:
    comparison_df[col] = comparison_df[col].apply(lambda x: f"${x:,.0f}" if not pd.isna(x) else "—")
st.dataframe(comparison_df, use_container_width=True)

# Summary
st.header("📋 Summary Statistics")
summary = simulator.summary_statistics(results_df)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Best for Stadium")
    st.write(f"**{summary['profit_maximizing_scenario']}**")
with col2:
    st.subheader("Best for Society")
    st.write(f"**{summary['welfare_maximizing_scenario']}**")
with col3:
    st.subheader("Lowest Externalities")
    st.write(f"**{summary['lowest_externality_scenario']}**")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'><p>Built with Streamlit | For educational and research purposes</p></div>", unsafe_allow_html=True)
