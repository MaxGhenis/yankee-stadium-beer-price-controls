# Beer Price Controls at Yankee Stadium: An Economic Analysis

A comprehensive economic simulation analyzing the impacts of beer price controls at Yankee Stadium on consumer welfare, stadium revenue, attendance, and alcohol-related externalities.

## Overview

This project models the economic tradeoffs when price controls are imposed on beer sales at Yankee Stadium. The analysis considers:

- **Consumer utility** from beer consumption and non-beer stadium experience
- **Revenue maximization** by the stadium across ticket and concession sales
- **Attendance effects** from price changes
- **Negative externalities** from alcohol consumption (crime, violence, public health costs)

## Key Research Findings

### Current Pricing (2025)
- **Average beer price**: $12.50 (range: $10-15)
- **Average ticket price**: $80
- **Stadium capacity**: 46,537

### Demand Elasticities (Literature-Based)
- **Ticket demand elasticity**: -0.49 to -0.76 (Noll 1974, Scully 1989)
  - Demand is inelastic; teams price tickets to maximize total revenue including concessions
- **Beer/concessions elasticity**: -0.79 to -1.14 (relatively inelastic in MLB)
  - Teams can raise prices without significantly reducing volume

### Alcohol Consumption & Externalities
- ~40% of spectators consume alcohol at games
- Mean BAC among drinkers: 0.057%
- **Crime impacts**: 10% increase in alcohol consumption → 1% increase in assault, 2.9% increase in rape (Carpenter & Dobkin 2015)
- Stadium alcohol cutoff (7th inning) reduces post-game crime by allowing fans to sober up

## Economic Model

### Consumer Utility Function
```
U(B, T, Y) = α·ln(B + 1) + β·ln(T + 1) + Y
```
Where:
- B = beers consumed at stadium
- T = time spent enjoying non-beer stadium experience (innings)
- Y = consumption of other goods (numeraire)
- α, β = preference parameters

### Budget Constraint
```
P_ticket + P_beer·B + Y = Income
```

### Stadium Revenue Maximization
```
max R = P_ticket·Attendance + P_beer·B·Attendance - C_ticket·Attendance - C_beer·B·Attendance
```
Subject to:
- Demand for attendance: A(P_ticket, P_beer, quality)
- Demand for beer per attendee: B(P_beer, income)

### Social Welfare with Externalities
```
SW = Consumer_Surplus + Producer_Surplus - External_Costs
```
Where:
```
External_Costs = (Total_Beers)·(Crime_Cost·Crime_Multiplier + Health_Cost)
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run src/app.py
```

The app allows you to adjust:
- Beer price controls (floor/ceiling)
- Demand elasticities
- Externality cost parameters
- Consumer preference parameters

## Simulation Scenarios

1. **Baseline**: Current market prices
2. **Price ceiling**: Maximum beer price (e.g., $8)
3. **Price floor**: Minimum beer price (e.g., $15)
4. **Ban**: Zero beer sales
5. **Free beer**: Zero beer price with ticket price adjustment

## Key Results

The simulation shows:
- **Price ceilings** reduce stadium revenue but may increase consumer surplus (if not offset by ticket price increases)
- **Deadweight loss** from binding price controls
- **Externality reduction** from lower consumption under price floors
- **Attendance impacts** depend on complementarity between tickets and beer

## Academic References

### Stadium Pricing & Demand Elasticity

1. **Noll, R. G. (1974)**. "Attendance and Price Setting." In *Government and the Sports Business*, edited by Roger G. Noll, 115-157. Washington, DC: Brookings Institution.
   - Found ticket demand elasticity of -0.49 for MLB (1970-71)

2. **Scully, G. W. (1989)**. *The Business of Major League Baseball*. Chicago: University of Chicago Press.
   - Estimated elasticities of -0.63 and -0.76 for 1984 MLB season

3. **Krautmann, A. C., & Berri, D. J. (2007)**. "Can We Find It at the Concessions? Understanding Price Elasticity in Professional Sports." *Journal of Sports Economics*, 8(2), 183-191.
   - Found beer/concession demand relatively inelastic in MLB
   - Teams price tickets below revenue-maximizing level to drive concession sales

4. **Coates, D., & Humphreys, B. R. (2007)**. "Ticket Prices, Concessions and Attendance at Professional Sporting Events." *International Journal of Sport Finance*, 2(3), 161-170.
   - Analyzed complementarity between ticket sales and concessions
   - Explains inelastic ticket pricing as revenue maximization strategy

### Alcohol Consumption at Sporting Events

5. **Bormann, C. A., & Stone, M. H. (2001)**. "The Effects of Eliminating Alcohol in a College Stadium: The Folsom Field Beer Ban." *Journal of American College Health*, 50(2), 81-88.
   - Case study of alcohol policy impacts

6. **Glassman, T., et al. (2010)**. "Extreme Ritualistic Alcohol Consumption Among College Students on Game Day." *Journal of American College Health*, 58(5), 413-423.
   - Documents high-risk drinking patterns at sporting events

7. **Lenk, K. M., Toomey, T. L., & Erickson, D. J. (2010)**. "Alcohol Control Policies and Practices at Professional Sports Stadiums." *Public Health Reports*, 125(5), 665-673.
   - Survey of alcohol policies across professional stadiums

### Alcohol Externalities & Crime

8. **Carpenter, C., & Dobkin, C. (2015)**. "The Minimum Legal Drinking Age and Crime." *Review of Economics and Statistics*, 97(2), 521-524.
   - Found 10% increase in alcohol → 1% increase in assault, 2.9% in rape

9. **Rees, D. I., & Schnepel, K. T. (2009)**. "College Football Games and Crime." *Journal of Sports Economics*, 10(1), 68-87.
   - Documented crime increases on college football game days

10. **Humphreys, B. R., & Ruseski, J. E. (2009)**. "The Size and Scope of the Sports Industry in the United States." In *The Business of Sports* (vol. 1), edited by Brad R. Humphreys and Dennis R. Howard, 27-48.
    - Provides context on sports industry economics

### Economic Externalities of Alcohol

11. **Manning, W. G., et al. (1991)**. *The Costs of Poor Health Habits*. Cambridge: Harvard University Press.
    - Estimated external costs of alcohol consumption at $0.48-$1.19 per drink (1986 dollars)

12. **Rehm, J., et al. (2009)**. "Global Burden of Disease and Injury and Economic Cost Attributable to Alcohol Use and Alcohol-Use Disorders." *The Lancet*, 373(9682), 2223-2233.
    - Global estimates of alcohol-related harm

## Model Limitations

- Assumes static attendance capacity (doesn't model long-run capacity adjustments)
- Simplified utility function (doesn't capture full complexity of fan preferences)
- Externality estimates based on general population (stadium-specific may differ)
- Doesn't model secondary markets or substitution to pre-game drinking
- Assumes stadium is monopolist (doesn't model competition from other entertainment)

## Future Extensions

- Dynamic model with repeated games and fan loyalty
- Heterogeneous consumers (casual fans vs. season ticket holders)
- Substitution to tailgating or pre-game bars
- Team performance and winning effects
- Comparison across different stadium alcohol policies

## Data Sources

- Current prices: Team Marketing Report, StubHub, industry sources
- Attendance data: MLB official statistics
- Academic elasticity estimates: Sports economics literature
- Externality costs: Public health and criminology research

## License

MIT

## Citation

If you use this model in academic work, please cite:
```
Beer Price Controls at Yankee Stadium Economic Simulator (2025)
https://github.com/[username]/yankee-stadium-beer-price-controls
```

## Contact

For questions or contributions, please open an issue on GitHub.
