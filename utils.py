from collections import deque

class DemandForecast:
    def __init__(self, window_size=10, alpha=0.3, beta=0.1):
        self.demand_history = deque(maxlen=window_size)
        self.alpha = alpha  # Level smoothing factor
        self.beta = beta   # Trend smoothing factor
        self.level = None
        self.trend = None
        
    def update(self, actual_demand):
        self.demand_history.append(actual_demand)
        
        if self.level is None:
            self.level = actual_demand
            self.trend = 0
        else:
            last_level = self.level
            self.level = self.alpha * actual_demand + (1 - self.alpha) * (self.level + self.trend)
            self.trend = self.beta * (self.level - last_level) + (1 - self.beta) * self.trend
    
    def forecast(self, steps_ahead=1):
        if self.level is None:
            return 30  # Default demand if not enough history
        
        forecast = self.level + steps_ahead * self.trend
        return max(int(forecast), 0)

class PerformanceMetrics:
    def __init__(self):
        self.total_demand = 0
        self.fulfilled_demand = 0
        self.backorders = 0
        self.inventory_history = []
        self.total_costs = 0
        
    def update_fill_rate(self, demand, fulfilled):
        self.total_demand += demand
        self.fulfilled_demand += fulfilled
        self.backorders += demand - fulfilled
        
    def update_inventory(self, inventory_levels):
        total_inventory = sum(inventory_levels.values())
        self.inventory_history.append(total_inventory)
        
    def update_costs(self, new_costs):
        self.total_costs += new_costs
        
    def calculate_metrics(self):
        fill_rate = (self.fulfilled_demand / self.total_demand * 100) if self.total_demand > 0 else 0
        avg_inventory = sum(self.inventory_history) / len(self.inventory_history) if self.inventory_history else 1
        inventory_turnover = self.fulfilled_demand / avg_inventory if avg_inventory > 0 else 0
        
        return {
            "fill_rate": round(fill_rate, 2),
            "inventory_turnover": round(inventory_turnover, 2),
            "backorders": self.backorders,
            "total_costs": round(self.total_costs, 2),
            "average_inventory": round(avg_inventory, 2)
        }

class CostManager:
    def __init__(self, base_costs):
        self.base_costs = base_costs
        self.cost_history = []
    
    def calculate_costs(self, state, supply, production, distribution):
        daily_costs = (
            supply * self.base_costs["raw_material"] +
            production * self.base_costs["manufacturing"] +
            distribution * self.base_costs["distribution"] +
            (state["supplier_inventory"] + state["manufacturer_inventory"] + 
             state["distributor_inventory"] + state["retail_inventory"]) * self.base_costs["holding"] +
            state["backorders"] * self.base_costs["backorder"]
        )
        self.cost_history.append(daily_costs)
        return daily_costs

def print_state_changes(state, step, action, changes):
    print(f"\n--- Step {step + 1}: {action} ---")
    for key, value in changes.items():
        print(f"{key}: {value}")

def validate_state(state):
    """Validate supply chain state."""
    required_keys = {
        'supplier_inventory', 'manufacturer_capacity',
        'distributor_inventory', 'retail_inventory'
    }
    
    if not required_keys.issubset(state.keys()):
        missing = required_keys - set(state.keys())
        raise ValueError(f"Missing required state keys: {missing}")
        
    for key, value in state.items():
        if isinstance(value, (int, float)) and value < 0:
            raise ValueError(f"Negative value not allowed for {key}: {value}")