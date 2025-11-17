# Introduction

## Motivation

Professional sports stadiums face a fundamental economic trade-off in alcohol pricing. Higher beer prices reduce consumption and associated negative externalities, including violence, public health costs, and drunk driving. However, beer sales represent a significant revenue stream for stadiums, with high profit margins that complement ticket revenue. This trade-off has motivated policy discussions about imposing price controls on stadium alcohol sales to address public health and safety concerns.

This paper analyzes the economic impacts of beer price controls at Yankee Stadium, one of the nation's most prominent sports venues. We examine:

effects on consumer welfare, stadium profit maximization across both ticket and beer revenue, attendance responses to price changes, and social externalities from alcohol consumption. We also evaluate current alcohol taxation relative to optimal Pigouvian benchmarks.

## Contribution

Our primary contribution is distinguishing between externalities that stadiums internalize through their profit maximization and those borne by society more broadly. We show that stadiums, as monopolists facing repeated interactions with customers, internalize negative effects that drunk fans impose on other attendees. These include increased security costs, reputational damage, and degradation of the stadium experience for other customers. We model these internalized costs as a convex function of total alcohol consumption, calibrated such that observed prices emerge as approximately profit-maximizing.

This distinction is economically important because only true social externalities that remain uninternalized by the stadium justify policy intervention beyond market outcomes. We estimate these remaining external costs at $4.00 per beer (comprising $2.50 for crime and violence and $1.50 for public health impacts), while current taxes total only $1.09 per beer, suggesting substantial under-taxation relative to the Pigouvian optimum.

## Main Findings

Our calibrated model yields several key results. First, we find that current pricing (average $80 tickets, $12.50 beer) is approximately profit-maximizing when accounting for taxes and internalized costs. The model predicts an optimal consumer beer price of $12.85, validating our calibration approach against observed market behavior.

Second, we identify a substantial Pigouvian tax gap. While external costs from alcohol consumption total approximately $4.00 per beer, current combined taxes amount to only $1.09 per beer, implying under-taxation of 73% relative to the social optimum. An additional tax of $2.91 per beer would fully internalize external costs while generating approximately $6.7 million in annual revenue for New York City.

Third, we analyze the general equilibrium effects of a binding beer price ceiling. A $7 ceiling (representing a 44% reduction from current prices) induces substantial adjustments in ticket pricing due to complementarity between the two goods. Specifically, the stadium's profit-maximizing response is to raise ticket prices by approximately $32 (36% increase). This occurs because the beer price ceiling compresses beer profit margins from $6.41 to $1.35 per unit (after accounting for taxes and marginal costs). The stadium optimally shifts toward ticket revenue, despite this causing a 38% decline in attendance. Importantly, per-capita beer consumption increases by 108%, leading to a 97% increase in external costs contrary to the presumed policy objective.

Fourth, we find that alternative policies dominate price ceilings on efficiency grounds. A Pigouvian tax of $2.91 per beer would internalize external costs, reduce consumption by 29%, and generate $6.7 million annually in tax revenue without creating deadweight loss from binding quantity constraints. This represents the first-best policy response to the externality problem.

## Theoretical Framework

Our model builds on the sports economics literature examining joint ticket-concession pricing {cite}`krautmann2007concessions,coates2007ticket` while introducing an explicit treatment of internalized costs. Standard models of stadium pricing typically assume production costs are the only constraint on profit maximization. However, this fails to explain why stadiums charge $12.50 for beer when simple profit maximization with standard demand curves suggests much lower optimal prices.

We resolve this puzzle by recognizing that stadiums, as monopolists in a repeated game with their customer base, internalize negative externalities that intoxicated fans impose on other attendees. These internalized costs include direct expenses (enhanced security, cleanup, liability insurance) and indirect costs (reputational damage reducing future attendance, experience degradation lowering customer willingness to pay). We model these as a convex function of total alcohol consumption, with the convexity reflecting the compounding nature of alcohol-related incidents.

In contrast, true social externalities including crime in surrounding neighborhoods, burdens on public health systems, and drunk driving remain uninternalized by the stadium's optimization problem. These provide the economic rationale for policy intervention through Pigouvian taxation or regulation.

## Data and Calibration

In the absence of proprietary transaction data from Yankee Stadium, we calibrate our model using publicly available information and parameters from the academic literature. Ticket demand elasticities of -0.625 (the midpoint of estimates ranging from -0.49 to -0.76 in {cite}`noll1974attendance,scully1989business`) and beer demand elasticities of -0.965 provide our baseline parameters, adjusted for the stadium context where captive audiences face no alternatives during games.

Current prices are drawn from industry sources and secondary ticket markets, with average beer prices of $12.50 and ticket prices of $80. Tax data come from federal (Alcohol and Tobacco Tax and Trade Bureau), New York State, and New York City sources. External cost estimates draw on {cite}`manning1991costs` for health costs and {cite}`carpenter2015mlda` for crime externalities, both adjusted for inflation.

Our semi-log demand specification for both tickets and beer provides flexibility while avoiding corner solutions inherent in constant-elasticity forms. We calibrate the price sensitivity parameters such that observed prices emerge as approximately profit-maximizing, which serves as an external validation of our approach.

## Structure

The remainder of this paper proceeds as follows. Section 2 reviews the relevant literature on stadium pricing, alcohol demand elasticities, and externalities from alcohol consumption. Section 3 presents our economic model, including the theoretical framework for demand, the stadium's profit maximization problem incorporating internalized costs, and the social welfare function. Section 4 describes our calibration strategy and validates the model against observed behavior. Section 5 presents simulation results for various policy scenarios, with particular attention to the $7 beer price ceiling. Section 6 analyzes alternative policies including Pigouvian taxation, price floors, and hybrid approaches. Section 7 discusses the Pigouvian tax gap and revenue allocation. Section 8 concludes with policy recommendations and directions for future research.

Interactive versions of our analysis, including a Streamlit application allowing real-time parameter adjustment and Monte Carlo simulations quantifying parameter uncertainty, are available in the online appendix.
