import { readFile } from "node:fs/promises";
import path from "node:path";

export interface ConsumerBreakdown {
  attendance: number;
  beers_per_fan: number;
  total_beers: number;
}

export interface ScenarioSummary {
  label: string;
  ticket_price: number;
  beer_price: number;
  attendance: number;
  drinker_share_attendance: number;
  beers_per_fan: number;
  total_beers: number;
  profit: number;
  consumer_surplus: number;
  social_welfare: number;
  breakdown_by_type: Record<string, ConsumerBreakdown>;
}

export interface CeilingComparison {
  ticket_pct_change: number;
  attendance_pct_change: number;
  beers_pct_change: number;
}

export interface DashboardContext {
  baseline: ScenarioSummary;
  ceiling_5: ScenarioSummary;
  ceiling_6: ScenarioSummary;
  ceiling_8: ScenarioSummary;
  ceiling_10: ScenarioSummary;
  ceiling_summary: Record<string, CeilingComparison>;
  monte_carlo: {
    draws: number;
    ticket_up_share: number;
    profit_down_share: number;
    beers_up_share: number;
  };
  calibration: {
    experience_degradation_cost: number;
    ticket_price_sensitivity: number;
    ticket_elasticity_at_80: number;
  };
  credibility: {
    baseline_attendance_share: number;
    baseline_drinker_beers: number;
    baseline_drinker_share: number;
    ceiling_6_drinker_share: number;
  };
}

export async function loadDashboardContext(): Promise<DashboardContext | null> {
  const contextPath = path.join(process.cwd(), "public", "data", "context.json");

  try {
    const raw = await readFile(contextPath, "utf8");
    return JSON.parse(raw) as DashboardContext;
  } catch (error) {
    if (error instanceof Error && "code" in error && error.code === "ENOENT") {
      return null;
    }

    throw error;
  }
}
