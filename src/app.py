"""
Streamlit app for beer price control simulation at Yankee Stadium.

Interactive tool to explore economic impacts of beer pricing policies
on consumer welfare, stadium revenue, attendance, and externalities.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import StadiumEconomicModel
from src.simulation import BeerPriceControlSimulator


# Page configuration
st.set_page_config(
    page_title="Yankee Stadium Beer Price Controls",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #003087;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #E4002B;
        text-align: center;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🍺 Beer Price Controls at Yankee Stadium</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">An Economic Analysis of Consumer Welfare, Revenue, and Externalities</p>', unsafe_allow_html=True)

# Sidebar - Model Parameters
st.sidebar.header("📊 Model Parameters")

st.sidebar.subheader("Stadium Characteristics")
capacity = st.sidebar.number_input(
    "Stadium Capacity",
    min_value=10000,
    max_value=100000,
    value=46537,
    step=1000,
    help="Yankee Stadium capacity"
)

st.sidebar.subheader("Baseline Prices")
base_ticket_price = st.sidebar.slider(
    "Base Ticket Price ($)",
    min_value=20.0,
    max_value=200.0,
    value=80.0,
    step=5.0,
    help="Average ticket price at baseline"
)

base_beer_price = st.sidebar.slider(
    "Base Beer Price ($)",
    min_value=5.0,
    max_value=25.0,
    value=12.5,
    step=0.5,
    help="Average beer price at baseline"
)

st.sidebar.subheader("Demand Elasticities")
ticket_elasticity = st.sidebar.slider(
    "Ticket Demand Elasticity",
    min_value=-2.0,
    max_value=-0.1,
    value=-0.625,
    step=0.05,
    help="Literature range: -0.49 to -0.76 (inelastic)"
)

beer_elasticity = st.sidebar.slider(
    "Beer Demand Elasticity",
    min_value=-2.0,
    max_value=-0.1,
    value=-0.965,
    step=0.05,
    help="Literature range: -0.79 to -1.14 (relatively inelastic)"
)

st.sidebar.subheader("Cost Parameters")
ticket_cost = st.sidebar.slider(
    "Marginal Cost per Ticket ($)",
    min_value=1.0,
    max_value=20.0,
    value=3.5,
    step=0.5,
    help="Realistic: ~$3.50 (most costs are fixed)"
)

beer_cost = st.sidebar.slider(
    "Marginal Cost per Beer ($)",
    min_value=0.5,
    max_value=10.0,
    value=2.0,
    step=0.5
)

st.sidebar.subheader("Consumer Preferences")
consumer_income = st.sidebar.slider(
    "Representative Consumer Income ($)",
    min_value=100.0,
    max_value=500.0,
    value=200.0,
    step=25.0,
    help="Budget for game day spending"
)

alpha = st.sidebar.slider(
    "Utility Weight on Beer (α)",
    min_value=0.5,
    max_value=5.0,
    value=1.5,
    step=0.1,
    help="Higher = stronger preference for beer"
)

beta = st.sidebar.slider(
    "Utility Weight on Stadium Experience (β)",
    min_value=0.5,
    max_value=5.0,
    value=3.0,
    step=0.1,
    help="Higher = stronger preference for stadium experience"
)

st.sidebar.subheader("Complementarity")
cross_price_elasticity = st.sidebar.slider(
    "Cross-Price Elasticity (Tickets-Beer)",
    min_value=0.0,
    max_value=0.5,
    value=0.1,
    step=0.05,
    help="How beer prices affect attendance. Benchmarks: 0.1 (weak), 0.3 (moderate), 1.6 (cars/gas)"
)

st.sidebar.subheader("Internalized Costs (Stadium)")
experience_degradation_cost = st.sidebar.slider(
    "Experience Degradation Cost (α)",
    min_value=50.0,
    max_value=500.0,
    value=250.0,
    step=50.0,
    help="Convex cost from drunk fans hurting other customers' experience"
)

st.sidebar.subheader("Externality Costs (Society)")
crime_cost_per_beer = st.sidebar.slider(
    "Crime Cost per Beer ($)",
    min_value=0.0,
    max_value=10.0,
    value=2.5,
    step=0.5,
    help="External cost from alcohol-related crime/violence"
)

health_cost_per_beer = st.sidebar.slider(
    "Health Cost per Beer ($)",
    min_value=0.0,
    max_value=10.0,
    value=1.5,
    step=0.5,
    help="External cost from alcohol-related health impacts"
)

# Main content - Policy Scenarios
st.header("🎯 Policy Scenarios")

col1, col2 = st.columns(2)

with col1:
    price_ceiling = st.slider(
        "Price Ceiling (Maximum Beer Price) ($)",
        min_value=5.0,
        max_value=20.0,
        value=8.0,
        step=0.5,
        help="Maximum allowed beer price"
    )

with col2:
    price_floor = st.slider(
        "Price Floor (Minimum Beer Price) ($)",
        min_value=10.0,
        max_value=30.0,
        value=15.0,
        step=0.5,
        help="Minimum allowed beer price"
    )

# Initialize model
@st.cache_data
def create_model(capacity, base_ticket_price, base_beer_price, ticket_elasticity,
                beer_elasticity, ticket_cost, beer_cost, consumer_income, alpha, beta,
                experience_degradation_cost, cross_price_elasticity):
    return StadiumEconomicModel(
        capacity=capacity,
        base_ticket_price=base_ticket_price,
        base_beer_price=base_beer_price,
        ticket_elasticity=ticket_elasticity,
        beer_elasticity=beer_elasticity,
        ticket_cost=ticket_cost,
        beer_cost=beer_cost,
        consumer_income=consumer_income,
        alpha=alpha,
        beta=beta,
        experience_degradation_cost=experience_degradation_cost,
        cross_price_elasticity=cross_price_elasticity
    )

model = create_model(
    capacity, base_ticket_price, base_beer_price, ticket_elasticity,
    beer_elasticity, ticket_cost, beer_cost, consumer_income, alpha, beta,
    experience_degradation_cost, cross_price_elasticity
)

# Run simulations
simulator = BeerPriceControlSimulator(model)

with st.spinner("Running simulations..."):
    results_df = simulator.run_all_scenarios(
        price_ceiling=price_ceiling,
        price_floor=price_floor,
        crime_cost_per_beer=crime_cost_per_beer,
        health_cost_per_beer=health_cost_per_beer
    )

# Display results
st.header("📈 Results Summary")

# Add ticket price response analysis
st.subheader("🎯 Key Finding: Ticket Price Response to Beer Ceiling")

baseline_scenario = results_df[results_df['scenario'] == 'Baseline (Profit Max)'].iloc[0]
current_scenario = results_df[results_df['scenario'] == 'Current Observed Prices'].iloc[0]
ceiling_7_scenarios = results_df[results_df['scenario'].str.contains('Price Ceiling.*7')]

if len(ceiling_7_scenarios) > 0 or price_ceiling <= 7.5:
    # Show ticket response
    col1, col2, col3 = st.columns(3)

    # Calculate optimal with beer at $7
    t_ceiling, b_ceiling, r_ceiling = model.optimal_pricing(beer_price_control=price_ceiling)
    t_current, b_current, r_current = model.optimal_pricing(beer_price_control=base_beer_price)

    ticket_change = t_ceiling - t_current
    ticket_pct = (ticket_change / t_current) * 100
    multiplier = abs(ticket_change / (price_ceiling - base_beer_price)) if price_ceiling != base_beer_price else 0

    with col1:
        st.metric(
            "Current Optimal Tickets",
            f"${t_current:.2f}",
            help="Optimal ticket price with $12.50 beer"
        )

    with col2:
        st.metric(
            f"With ${price_ceiling} Beer Ceiling",
            f"${t_ceiling:.2f}",
            f"{ticket_change:+.2f} ({ticket_pct:+.1f}%)",
            help="Optimal ticket price under beer price control"
        )

    with col3:
        st.metric(
            "Price Adjustment Multiplier",
            f"{multiplier:.1f}x",
            help="Ticket increase per $1 beer decrease"
        )

    st.info(f"""
    **Economic mechanism**: When beer revenue is constrained, stadium shifts toward ticket revenue.

    With cross-elasticity {cross_price_elasticity:.2f}:
    - Attendance falls {((r_ceiling['attendance']/r_current['attendance'] - 1) * 100):.1f}% (higher tickets + beer complementarity)
    - Stadium raises tickets {ticket_pct:.1f}% to partially compensate
    - But total revenue still falls {((r_ceiling['total_revenue']/r_current['total_revenue'] - 1) * 100):.1f}%
    """)

    st.divider()

# Original key metrics section
st.subheader("📊 Baseline Metrics")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

baseline_idx = results_df[results_df['scenario'] == 'Current Observed Prices'].index[0]
baseline = results_df.iloc[baseline_idx]

with col1:
    st.metric(
        "Baseline Attendance",
        f"{baseline['attendance']:,.0f}",
        help="Attendance at current prices"
    )

with col2:
    st.metric(
        "Baseline Total Beers",
        f"{baseline['total_beers']:,.0f}",
        help="Total beers sold at current prices"
    )

with col3:
    st.metric(
        "Baseline Profit",
        f"${baseline['profit']:,.0f}",
        help="Stadium profit at current prices"
    )

with col4:
    st.metric(
        "Baseline Social Welfare",
        f"${baseline['social_welfare']:,.0f}",
        help="Total welfare including externalities"
    )

# Results table
st.subheader("Detailed Results by Scenario")

# Format table for display
display_df = results_df.copy()
display_df = display_df[[
    'scenario', 'ticket_price', 'beer_price', 'attendance', 'total_beers',
    'total_revenue', 'profit', 'consumer_surplus', 'externality_cost', 'social_welfare'
]]

# Format numbers
for col in ['ticket_price', 'beer_price']:
    display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")

for col in ['attendance', 'total_beers']:
    display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}")

for col in ['total_revenue', 'profit', 'consumer_surplus', 'externality_cost', 'social_welfare']:
    display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")

st.dataframe(display_df, use_container_width=True)

# Visualizations
st.header("📊 Visualizations")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Revenue & Welfare",
    "Attendance & Consumption",
    "Price Comparison",
    "Externalities",
    "Price Ceiling Analysis"
])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Revenue comparison
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Bar(
            x=results_df['scenario'],
            y=results_df['profit'],
            name='Stadium Profit',
            marker_color='#003087'
        ))
        fig_revenue.update_layout(
            title="Stadium Profit by Scenario",
            xaxis_title="Scenario",
            yaxis_title="Profit ($)",
            height=400
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

    with col2:
        # Welfare comparison
        fig_welfare = go.Figure()
        fig_welfare.add_trace(go.Bar(
            x=results_df['scenario'],
            y=results_df['social_welfare'],
            name='Social Welfare',
            marker_color='#E4002B'
        ))
        fig_welfare.update_layout(
            title="Social Welfare by Scenario",
            xaxis_title="Scenario",
            yaxis_title="Social Welfare ($)",
            height=400
        )
        st.plotly_chart(fig_welfare, use_container_width=True)

    # Stacked welfare components
    fig_components = go.Figure()
    fig_components.add_trace(go.Bar(
        x=results_df['scenario'],
        y=results_df['consumer_surplus'],
        name='Consumer Surplus',
        marker_color='lightblue'
    ))
    fig_components.add_trace(go.Bar(
        x=results_df['scenario'],
        y=results_df['producer_surplus'],
        name='Producer Surplus',
        marker_color='lightgreen'
    ))
    fig_components.add_trace(go.Bar(
        x=results_df['scenario'],
        y=-results_df['externality_cost'],
        name='Externality Cost (negative)',
        marker_color='salmon'
    ))
    fig_components.update_layout(
        title="Welfare Components by Scenario",
        xaxis_title="Scenario",
        yaxis_title="Value ($)",
        barmode='stack',
        height=500
    )
    st.plotly_chart(fig_components, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        # Attendance
        fig_attendance = go.Figure()
        fig_attendance.add_trace(go.Bar(
            x=results_df['scenario'],
            y=results_df['attendance'],
            marker_color='#003087'
        ))
        fig_attendance.update_layout(
            title="Attendance by Scenario",
            xaxis_title="Scenario",
            yaxis_title="Attendance",
            height=400
        )
        st.plotly_chart(fig_attendance, use_container_width=True)

    with col2:
        # Beer consumption
        fig_beers = go.Figure()
        fig_beers.add_trace(go.Bar(
            x=results_df['scenario'],
            y=results_df['total_beers'],
            marker_color='#E4002B'
        ))
        fig_beers.update_layout(
            title="Total Beer Consumption by Scenario",
            xaxis_title="Scenario",
            yaxis_title="Total Beers Sold",
            height=400
        )
        st.plotly_chart(fig_beers, use_container_width=True)

    # Beers per fan
    fig_per_fan = go.Figure()
    fig_per_fan.add_trace(go.Bar(
        x=results_df['scenario'],
        y=results_df['beers_per_fan'],
        marker_color='orange'
    ))
    fig_per_fan.update_layout(
        title="Beers per Fan by Scenario",
        xaxis_title="Scenario",
        yaxis_title="Beers per Fan",
        height=400
    )
    st.plotly_chart(fig_per_fan, use_container_width=True)

with tab3:
    # Price comparison
    fig_prices = go.Figure()
    fig_prices.add_trace(go.Scatter(
        x=results_df['scenario'],
        y=results_df['ticket_price'],
        mode='lines+markers',
        name='Ticket Price',
        line=dict(color='#003087', width=3),
        marker=dict(size=10)
    ))
    fig_prices.add_trace(go.Scatter(
        x=results_df['scenario'],
        y=results_df['beer_price'],
        mode='lines+markers',
        name='Beer Price',
        line=dict(color='#E4002B', width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))
    fig_prices.update_layout(
        title="Ticket and Beer Prices by Scenario",
        xaxis_title="Scenario",
        yaxis_title="Ticket Price ($)",
        yaxis2=dict(
            title="Beer Price ($)",
            overlaying='y',
            side='right'
        ),
        height=500,
        hovermode='x unified'
    )
    st.plotly_chart(fig_prices, use_container_width=True)

with tab4:
    # Externality costs
    fig_ext = go.Figure()
    fig_ext.add_trace(go.Bar(
        x=results_df['scenario'],
        y=results_df['externality_cost'],
        marker_color='darkred'
    ))
    fig_ext.update_layout(
        title="Total Externality Costs by Scenario",
        xaxis_title="Scenario",
        yaxis_title="External Cost ($)",
        height=400
    )
    st.plotly_chart(fig_ext, use_container_width=True)

    # Cost per beer breakdown
    st.subheader("Externality Cost Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Crime Cost per Beer",
            f"${crime_cost_per_beer:.2f}",
            help="External cost from alcohol-related crime/violence per beer"
        )
    with col2:
        st.metric(
            "Health Cost per Beer",
            f"${health_cost_per_beer:.2f}",
            help="External cost from health system burden per beer"
        )

with tab5:
    st.subheader("📈 Price Ceiling Comparative Statics")
    st.markdown("""
    This analysis shows how outcomes vary as we systematically vary the beer price ceiling,
    holding all other parameters constant. This reveals the **stadium's optimal response**
    and the resulting equilibrium effects.
    """)

    # Generate price ceiling sweep
    ceiling_range = np.linspace(5, 20, 31)
    ceiling_results = []

    with st.spinner("Computing price ceiling analysis..."):
        # First find unconstrained optimum
        unc_t, unc_b, unc_rev = model.optimal_pricing()

        for ceiling in ceiling_range:
            # Only apply ceiling if it binds
            if ceiling < unc_b:
                t_p, b_p, rev = model.optimal_pricing(beer_price_control=ceiling)
            else:
                # Ceiling doesn't bind - use unconstrained optimum
                t_p, b_p, rev = unc_t, unc_b, unc_rev

            welf = model.social_welfare(t_p, b_p, crime_cost_per_beer, health_cost_per_beer)
            ceiling_results.append({
                'ceiling': ceiling,
                'ticket_price': t_p,
                'beer_price': b_p,
                'attendance': rev['attendance'],
                'beers_per_fan': rev['beers_per_fan'],
                'total_beers': rev['total_beers'],
                'total_revenue': rev['total_revenue'],
                'profit': rev['profit'],
                'consumer_surplus': welf['consumer_surplus'],
                'externality_cost': welf['externality_cost'],
                'social_welfare': welf['social_welfare']
            })

    ceiling_df = pd.DataFrame(ceiling_results)

    # Chart 1: Pricing Response
    st.subheader("1. Stadium Pricing Response")
    col1, col2 = st.columns(2)

    with col1:
        fig_ticket_response = go.Figure()
        fig_ticket_response.add_trace(go.Scatter(
            x=ceiling_df['ceiling'],
            y=ceiling_df['ticket_price'],
            mode='lines+markers',
            name='Optimal Ticket Price',
            line=dict(color='#003087', width=3),
            marker=dict(size=6)
        ))
        fig_ticket_response.add_hline(
            y=base_ticket_price,
            line_dash="dash",
            line_color="gray",
            annotation_text="Baseline",
            annotation_position="right"
        )
        fig_ticket_response.add_vline(
            x=base_beer_price,
            line_dash="dash",
            line_color="gray"
        )
        fig_ticket_response.update_layout(
            title="Ticket Prices Rise as Beer Ceiling Tightens",
            xaxis_title="Beer Price Ceiling ($)",
            yaxis_title="Optimal Ticket Price ($)",
            height=400
        )
        st.plotly_chart(fig_ticket_response, use_container_width=True)

    with col2:
        fig_beer_response = go.Figure()
        fig_beer_response.add_trace(go.Scatter(
            x=ceiling_df['ceiling'],
            y=ceiling_df['beer_price'],
            mode='lines+markers',
            name='Actual Beer Price',
            line=dict(color='#E4002B', width=3),
            marker=dict(size=6)
        ))
        fig_beer_response.add_trace(go.Scatter(
            x=ceiling_df['ceiling'],
            y=ceiling_df['ceiling'],
            mode='lines',
            name='Ceiling',
            line=dict(color='gray', width=2, dash='dash')
        ))
        fig_beer_response.add_vline(
            x=base_beer_price,
            line_dash="dash",
            line_color="gray"
        )
        fig_beer_response.update_layout(
            title="Beer Price Tracks Ceiling (When Binding)",
            xaxis_title="Beer Price Ceiling ($)",
            yaxis_title="Beer Price ($)",
            height=400
        )
        st.plotly_chart(fig_beer_response, use_container_width=True)

    # Chart 2: Quantities
    st.subheader("2. Quantity Effects")
    col1, col2 = st.columns(2)

    with col1:
        fig_attendance = go.Figure()
        fig_attendance.add_trace(go.Scatter(
            x=ceiling_df['ceiling'],
            y=ceiling_df['attendance']/1000,
            mode='lines+markers',
            line=dict(color='#003087', width=3),
            marker=dict(size=6)
        ))
        fig_attendance.add_vline(x=base_beer_price, line_dash="dash", line_color="gray")
        fig_attendance.update_layout(
            title="Attendance Falls with Lower Ceilings",
            xaxis_title="Beer Price Ceiling ($)",
            yaxis_title="Attendance (thousands)",
            height=400
        )
        st.plotly_chart(fig_attendance, use_container_width=True)

    with col2:
        fig_total_beers = go.Figure()
        fig_total_beers.add_trace(go.Scatter(
            x=ceiling_df['ceiling'],
            y=ceiling_df['total_beers']/1000,
            mode='lines+markers',
            line=dict(color='#E4002B', width=3),
            marker=dict(size=6)
        ))
        fig_total_beers.add_vline(x=base_beer_price, line_dash="dash", line_color="gray")
        fig_total_beers.update_layout(
            title="Total Beer Consumption Rises",
            xaxis_title="Beer Price Ceiling ($)",
            yaxis_title="Total Beers (thousands)",
            height=400
        )
        st.plotly_chart(fig_total_beers, use_container_width=True)

    # Chart 3: Welfare
    st.subheader("3. Welfare Analysis")
    fig_welfare_all = go.Figure()
    fig_welfare_all.add_trace(go.Scatter(
        x=ceiling_df['ceiling'],
        y=ceiling_df['consumer_surplus']/1e6,
        mode='lines+markers',
        name='Consumer Surplus',
        line=dict(width=2.5),
        marker=dict(size=6)
    ))
    fig_welfare_all.add_trace(go.Scatter(
        x=ceiling_df['ceiling'],
        y=ceiling_df['profit']/1e6,
        mode='lines+markers',
        name='Producer Surplus (Profit)',
        line=dict(width=2.5),
        marker=dict(size=6)
    ))
    fig_welfare_all.add_trace(go.Scatter(
        x=ceiling_df['ceiling'],
        y=-ceiling_df['externality_cost']/1e6,
        mode='lines+markers',
        name='Externality Cost (negative)',
        line=dict(width=2.5),
        marker=dict(size=6)
    ))
    fig_welfare_all.add_trace(go.Scatter(
        x=ceiling_df['ceiling'],
        y=ceiling_df['social_welfare']/1e6,
        mode='lines+markers',
        name='Social Welfare (sum)',
        line=dict(width=3.5, color='purple'),
        marker=dict(size=8)
    ))
    fig_welfare_all.add_vline(x=base_beer_price, line_dash="dash", line_color="gray",
                              annotation_text="Baseline")
    fig_welfare_all.update_layout(
        title="Welfare Decomposition: Lower Ceilings Reduce Social Welfare",
        xaxis_title="Beer Price Ceiling ($)",
        yaxis_title="Welfare ($ millions per game)",
        height=500,
        legend=dict(x=0.02, y=0.98)
    )
    st.plotly_chart(fig_welfare_all, use_container_width=True)

    st.info("""
    **Key Insight:** Price ceilings create deadweight loss. The stadium loses more than
    consumers gain, and externalities worsen. This motivates Pigouvian taxation as a
    superior policy instrument.
    """)

# Comparative analysis
st.header("🔍 Comparative Analysis")

changes_df = simulator.calculate_comparative_statics(results_df)

st.subheader("Changes Relative to Current Prices")

comparison_cols = ['scenario', 'profit_change', 'social_welfare_change',
                   'attendance_change', 'total_beers_change', 'externality_cost_change']

comparison_df = changes_df[comparison_cols].copy()

for col in comparison_cols[1:]:
    comparison_df[col] = comparison_df[col].apply(lambda x: f"${x:,.0f}" if not pd.isna(x) else "—")

st.dataframe(comparison_df, use_container_width=True)

# Summary statistics
st.header("📋 Summary Statistics")

summary = simulator.summary_statistics(results_df)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Best for Stadium")
    st.write(f"**{summary['profit_maximizing_scenario']}**")
    max_profit_row = results_df[results_df['scenario'] == summary['profit_maximizing_scenario']].iloc[0]
    st.write(f"Profit: ${max_profit_row['profit']:,.0f}")

with col2:
    st.subheader("Best for Society")
    st.write(f"**{summary['welfare_maximizing_scenario']}**")
    max_welfare_row = results_df[results_df['scenario'] == summary['welfare_maximizing_scenario']].iloc[0]
    st.write(f"Social Welfare: ${max_welfare_row['social_welfare']:,.0f}")

with col3:
    st.subheader("Lowest Externalities")
    st.write(f"**{summary['lowest_externality_scenario']}**")
    min_ext_row = results_df[results_df['scenario'] == summary['lowest_externality_scenario']].iloc[0]
    st.write(f"Externality Cost: ${min_ext_row['externality_cost']:,.0f}")

# About section
with st.expander("ℹ️ About This Model"):
    st.markdown("""
    ### Model Overview

    This simulation analyzes the economic impacts of beer price controls at Yankee Stadium using:

    - **Consumer utility theory**: Fans derive utility from beer consumption and stadium experience
    - **Revenue maximization**: Stadium sets prices to maximize profit from tickets + concessions
    - **Demand elasticities**: Based on academic literature (Noll 1974, Scully 1989, Krautmann & Berri 2007)
    - **Externality estimates**: Crime and health costs from alcohol consumption literature

    ### Key Findings from Literature

    - Ticket demand is **inelastic** (ε ≈ -0.49 to -0.76)
    - Beer demand is **relatively inelastic** (ε ≈ -0.79 to -1.14)
    - ~40% of fans consume alcohol at games
    - 10% increase in alcohol consumption → 1% increase in assault

    ### Policy Implications

    - **Price ceilings** reduce stadium profit but may increase consumer surplus
    - **Price floors** reduce consumption and externalities but create deadweight loss
    - **Social optimum** typically involves higher beer prices than profit maximum
    - Trade-offs exist between revenue, consumer welfare, and public health

    ### References

    See full academic references in the GitHub repository README.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 2rem;'>
    <p>Built with Streamlit | Data based on academic research and industry sources</p>
    <p>For educational and research purposes</p>
</div>
""", unsafe_allow_html=True)
