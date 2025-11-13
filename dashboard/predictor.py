"""
Predictive Multi-Objective Scheduler for Dashboard
Simplified version without external dependencies on scheduler module
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
import requests


# Regional cost per vCPU-hour (USD) - Based on Google Cloud pricing
REGION_COSTS = {
    'IN': 0.0476,
    'FI': 0.0570,
    'DE': 0.0475,
    'JP': 0.0560,
    'AU-NSW': 0.0595,
    'BR-CS': 0.0450,
}

# Average network latency from asia-south1 (ms)
REGION_LATENCY = {
    'IN': 10,
    'FI': 180,
    'DE': 150,
    'JP': 90,
    'AU-NSW': 140,
    'BR-CS': 350,
}

# Region display names
REGION_NAMES = {
    'IN': 'India',
    'FI': 'Finland',
    'DE': 'Germany',
    'JP': 'Japan',
    'AU-NSW': 'Australia NSW',
    'BR-CS': 'Brazil CS',
}


class SimplePredictiveScheduler:
    """Simplified multi-objective scheduler for dashboard"""

    def __init__(self, api_key: str = "gwASf8vJiQ92CPIuRzuy"):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def fetch_carbon_data(self) -> Dict[str, float]:
        """Fetch current carbon intensity from ElectricityMap API"""
        try:
            url = "https://api.electricitymap.org/v3/carbon-intensity/latest"
            headers = {"auth-token": self.api_key}

            regions = ['IN', 'FI', 'DE', 'JP', 'AU-NSW', 'BR-CS']
            carbon_data = {}

            for region in regions:
                try:
                    response = requests.get(
                        url,
                        headers=headers,
                        params={"zone": region},
                        timeout=5
                    )

                    if response.status_code == 200:
                        data = response.json()
                        carbon_data[region] = data.get('carbonIntensity', 0)
                    else:
                        # Use default values if API fails
                        defaults = {
                            'IN': 508, 'FI': 40, 'DE': 265,
                            'JP': 502, 'AU-NSW': 327, 'BR-CS': 161
                        }
                        carbon_data[region] = defaults.get(region, 300)
                except:
                    defaults = {
                        'IN': 508, 'FI': 40, 'DE': 265,
                        'JP': 502, 'AU-NSW': 327, 'BR-CS': 161
                    }
                    carbon_data[region] = defaults.get(region, 300)

            return carbon_data

        except Exception as e:
            self.logger.error(f"Failed to fetch carbon data: {e}")
            # Return default values
            return {
                'IN': 508, 'FI': 40, 'DE': 265,
                'JP': 502, 'AU-NSW': 327, 'BR-CS': 161
            }

    def normalize_value(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize value to [0, 1] range"""
        if max_val == min_val:
            return 0.5
        return (value - min_val) / (max_val - min_val)

    def calculate_score(
        self,
        carbon: float,
        latency: float,
        cost: float,
        all_carbon: List[float],
        all_latency: List[float],
        all_costs: List[float],
        w_carbon: float,
        w_latency: float,
        w_cost: float
    ) -> float:
        """Calculate weighted multi-objective score"""
        norm_carbon = self.normalize_value(carbon, min(all_carbon), max(all_carbon))
        norm_latency = self.normalize_value(latency, min(all_latency), max(all_latency))
        norm_cost = self.normalize_value(cost, min(all_costs), max(all_costs))

        return w_carbon * norm_carbon + w_latency * norm_latency + w_cost * norm_cost

    def select_optimal_region(
        self,
        w_carbon: float = 0.5,
        w_latency: float = 0.3,
        w_cost: float = 0.2
    ) -> Dict:
        """Select optimal region using multi-objective optimization"""
        # Normalize weights
        total = w_carbon + w_latency + w_cost
        if total > 0:
            w_carbon /= total
            w_latency /= total
            w_cost /= total

        # Fetch carbon data
        carbon_data = self.fetch_carbon_data()

        if not carbon_data:
            return {'success': False, 'error': 'Failed to fetch carbon data'}

        # Build candidates
        candidates = []
        for region, intensity in carbon_data.items():
            candidates.append({
                'region': region,
                'region_name': REGION_NAMES.get(region, region),
                'carbon_intensity': intensity,
                'latency': REGION_LATENCY.get(region, 100),
                'cost': REGION_COSTS.get(region, 0.05)
            })

        # Extract metrics
        all_carbon = [c['carbon_intensity'] for c in candidates]
        all_latency = [c['latency'] for c in candidates]
        all_costs = [c['cost'] for c in candidates]

        # Calculate scores
        for candidate in candidates:
            candidate['score'] = self.calculate_score(
                carbon=candidate['carbon_intensity'],
                latency=candidate['latency'],
                cost=candidate['cost'],
                all_carbon=all_carbon,
                all_latency=all_latency,
                all_costs=all_costs,
                w_carbon=w_carbon,
                w_latency=w_latency,
                w_cost=w_cost
            )

        # Sort by score
        candidates.sort(key=lambda x: x['score'])
        optimal = candidates[0]

        # Calculate savings
        avg_carbon = np.mean(all_carbon)
        savings = avg_carbon - optimal['carbon_intensity']

        return {
            'success': True,
            'region': optimal['region'],
            'region_name': optimal['region_name'],
            'carbon_intensity': optimal['carbon_intensity'],
            'latency': optimal['latency'],
            'cost': optimal['cost'],
            'score': optimal['score'],
            'weights': {
                'carbon': w_carbon,
                'latency': w_latency,
                'cost': w_cost
            },
            'savings_gco2': savings,
            'avg_carbon_intensity': avg_carbon,
            'all_candidates': candidates,
            'timestamp': datetime.utcnow().isoformat()
        }

    def generate_pareto_frontier(
        self,
        objective1: str = 'carbon',
        objective2: str = 'latency'
    ) -> List[Dict]:
        """Generate Pareto frontier for two objectives"""
        carbon_data = self.fetch_carbon_data()

        if not carbon_data:
            return []

        # Build solutions
        solutions = []
        for region, intensity in carbon_data.items():
            solutions.append({
                'region': region,
                'carbon': intensity,
                'latency': REGION_LATENCY.get(region, 100),
                'cost': REGION_COSTS.get(region, 0.05)
            })

        # Find Pareto-optimal solutions
        pareto_frontier = []

        for i, sol_i in enumerate(solutions):
            is_dominated = False

            for j, sol_j in enumerate(solutions):
                if i == j:
                    continue

                obj1_better = sol_j[objective1] <= sol_i[objective1]
                obj2_better = sol_j[objective2] <= sol_i[objective2]
                strictly_better = (
                    sol_j[objective1] < sol_i[objective1] or
                    sol_j[objective2] < sol_i[objective2]
                )

                if obj1_better and obj2_better and strictly_better:
                    is_dominated = True
                    break

            if not is_dominated:
                pareto_frontier.append(sol_i)

        pareto_frontier.sort(key=lambda x: x[objective1])
        return pareto_frontier
