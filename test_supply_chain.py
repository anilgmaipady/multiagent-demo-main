import unittest
from agents import SupplyTool, ManufactureTool, DistributeTool, RetailTool
from utils import DemandForecast, PerformanceMetrics, CostManager

class TestSupplyChainAgents(unittest.TestCase):
    def setUp(self):
        self.supply_tool = SupplyTool()
        self.manufacture_tool = ManufactureTool()
        self.distribute_tool = DistributeTool()
        self.retail_tool = RetailTool()

    def test_supply_tool(self):
        # Test normal supply
        self.assertEqual(self.supply_tool.forward(demand=30, inventory=100), 30)
        # Test limited inventory
        self.assertEqual(self.supply_tool.forward(demand=100, inventory=50), 50)
        # Test zero inventory
        self.assertEqual(self.supply_tool.forward(demand=30, inventory=0), 0)

    def test_manufacture_tool(self):
        # Test normal production
        self.assertEqual(
            self.manufacture_tool.forward(raw_material=50, capacity=40, demand=30),
            30
        )
        # Test capacity constraint
        self.assertEqual(
            self.manufacture_tool.forward(raw_material=100, capacity=30, demand=50),
            30
        )
        # Test material constraint
        self.assertEqual(
            self.manufacture_tool.forward(raw_material=20, capacity=50, demand=30),
            20
        )

    def test_distribute_tool(self):
        # Test normal distribution
        self.assertEqual(self.distribute_tool.forward(inventory=100, demand=50), 50)
        # Test limited inventory
        self.assertEqual(self.distribute_tool.forward(inventory=30, demand=50), 30)
        # Test zero inventory
        self.assertEqual(self.distribute_tool.forward(inventory=0, demand=50), 0)

    def test_retail_tool(self):
        # Test normal retail
        self.assertEqual(
            self.retail_tool.forward(customer_demand=30, available_stock=50),
            30
        )
        # Test limited stock
        self.assertEqual(
            self.retail_tool.forward(customer_demand=50, available_stock=30),
            30
        )
        # Test zero stock
        self.assertEqual(
            self.retail_tool.forward(customer_demand=30, available_stock=0),
            0
        )

class TestDemandForecast(unittest.TestCase):
    def setUp(self):
        self.forecast = DemandForecast(window_size=5)

    def test_initial_forecast(self):
        # Test initial forecast without history
        self.assertEqual(self.forecast.forecast(), 30)

    def test_forecast_with_history(self):
        # Add some history
        for demand in [100, 110, 120, 130, 140]:
            self.forecast.update(demand)
        
        # Test forecast
        forecast = self.forecast.forecast()
        self.assertTrue(130 <= forecast <= 150)  # Reasonable range

    def test_window_size(self):
        # Test that window size is respected
        for i in range(10):
            self.forecast.update(i)
        
        self.assertEqual(len(self.forecast.demand_history), 5)

class TestPerformanceMetrics(unittest.TestCase):
    def setUp(self):
        self.metrics = PerformanceMetrics()

    def test_fill_rate(self):
        self.metrics.update_fill_rate(demand=100, fulfilled=80)
        metrics = self.metrics.calculate_metrics()
        self.assertEqual(metrics["fill_rate"], 80.0)

    def test_inventory_turnover(self):
        self.metrics.update_fill_rate(demand=100, fulfilled=80)
        self.metrics.update_inventory({
            "supplier": 50,
            "manufacturer": 30,
            "distributor": 40,
            "retail": 20
        })
        metrics = self.metrics.calculate_metrics()
        self.assertTrue(metrics["inventory_turnover"] > 0)

    def test_backorders(self):
        self.metrics.update_fill_rate(demand=100, fulfilled=80)
        metrics = self.metrics.calculate_metrics()
        self.assertEqual(metrics["backorders"], 20)

class TestCostManager(unittest.TestCase):
    def setUp(self):
        self.costs = {
            "raw_material": 10,
            "manufacturing": 15,
            "distribution": 5,
            "holding": 2,
            "backorder": 20
        }
        self.cost_manager = CostManager(self.costs)

    def test_cost_calculation(self):
        state = {
            "supplier_inventory": 100,
            "manufacturer_inventory": 50,
            "distributor_inventory": 30,
            "retail_inventory": 20,
            "backorders": 10
        }
        daily_costs = self.cost_manager.calculate_costs(
            state=state,
            supply=30,
            production=25,
            distribution=20
        )
        
        # Calculate expected costs
        expected_costs = (
            30 * self.costs["raw_material"] +  # Raw material costs
            25 * self.costs["manufacturing"] +  # Manufacturing costs
            20 * self.costs["distribution"] +   # Distribution costs
            (100 + 50 + 30 + 20) * self.costs["holding"] +  # Holding costs
            10 * self.costs["backorder"]        # Backorder costs
        )
        
        self.assertEqual(daily_costs, expected_costs)

if __name__ == '__main__':
    unittest.main()