class SupplyChainConfig:
    def __init__(self):
        self.simulation = {
            "num_steps": 5,
            "random_seed": 42,
            "lead_time": 0.5,
        }

        self.inventory = {
            "initial_supplier": 100,
            "initial_manufacturer": 0,
            "initial_distributor": 50,
            "initial_retail": 0,
            "manufacturer_capacity": 50,
            "safety_stock_factor": 0.2,
        }

        self.demand = {
            "initial": 30,
            "min_variation": -5,
            "max_variation": 5,
            "forecast_window": 10,
            "smoothing_alpha": 0.3,
            "smoothing_beta": 0.1,
        }

        self.costs = {
            "raw_material": 10,
            "manufacturing": 15,
            "distribution": 5,
            "holding": 2,
            "backorder": 20,
        }

        self.resupply = {
            "min_amount": 10,
            "max_amount": 20,
        }

    def update(self, new_config):
        """Update configuration with new values."""
        for section, values in new_config.items():
            if hasattr(self, section):
                current_section = getattr(self, section)
                current_section.update(values)

    def validate(self):
        """Validate configuration values."""
        assert self.simulation["num_steps"] > 0, "Number of steps must be positive"
        assert self.simulation["lead_time"] >= 0, "Lead time cannot be negative"
        
        for key, value in self.inventory.items():
            if "initial" in key or "capacity" in key:
                assert value >= 0, f"{key} cannot be negative"
        
        assert 0 <= self.demand["smoothing_alpha"] <= 1, "Smoothing alpha must be between 0 and 1"
        assert 0 <= self.demand["smoothing_beta"] <= 1, "Smoothing beta must be between 0 and 1"
        
        for cost_type, cost in self.costs.items():
            assert cost >= 0, f"{cost_type} cost cannot be negative"

class SafetyStockOptimizer:
    def __init__(self, service_level=0.95):
        self.service_level = service_level

    def calculate_safety_stock(self, demand_history, lead_time):
        """Calculate optimal safety stock level."""
        if len(demand_history) < 2:
            return 0
            
        z_score = self._get_z_score()
        demand_std = np.std(demand_history)
        
        safety_stock = z_score * demand_std * np.sqrt(lead_time)
        return max(int(safety_stock), 0)

    def _get_z_score(self):
        """Get z-score for given service level."""
        from scipy.stats import norm
        return norm.ppf(self.service_level)

class ReorderPointCalculator:
    @staticmethod
    def calculate(demand_rate, lead_time, safety_stock):
        """Calculate reorder point."""
        return int(demand_rate * lead_time + safety_stock)

class InventoryOptimizer:
    def __init__(self, config):
        self.config = config
        self.safety_stock_optimizer = SafetyStockOptimizer()
        self.reorder_calculator = ReorderPointCalculator()

    def optimize(self, demand_history, lead_time):
        """Optimize inventory parameters."""
        safety_stock = self.safety_stock_optimizer.calculate_safety_stock(
            demand_history, lead_time
        )
        
        avg_demand = np.mean(demand_history) if len(demand_history) > 0 else 30
        reorder_point = self.reorder_calculator.calculate(
            avg_demand, lead_time, safety_stock
        )
        
        return {
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "order_quantity": self._calculate_order_quantity(avg_demand)
        }

    def _calculate_order_quantity(self, avg_demand):
        """Calculate economic order quantity."""
        holding_cost = self.config.costs["holding"]
        order_cost = self.config.costs["raw_material"]
        
        eoq = np.sqrt((2 * avg_demand * order_cost) / holding_cost)
        return max(int(eoq), 1)