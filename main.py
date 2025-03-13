from smolagents import CodeAgent, HfApiModel
import random
import time
from agents import SupplyTool, ManufactureTool, DistributeTool, RetailTool
from utils import DemandForecast, PerformanceMetrics, CostManager, print_state_changes, validate_state

def run_simulation(num_steps=5):
    # Initialize tools
    supply_tool = SupplyTool()
    manufacture_tool = ManufactureTool()
    distribute_tool = DistributeTool()
    retail_tool = RetailTool()

    # Initialize support classes
    model = HfApiModel(model_id="meta-llama/Llama-3.3-70B-Instruct")
    demand_forecast = DemandForecast()
    metrics = PerformanceMetrics()

    # Cost configuration
    costs = {
        "raw_material": 10,
        "manufacturing": 15,
        "distribution": 5,
        "holding": 2,
        "backorder": 20
    }
    cost_manager = CostManager(costs)

    # Initialize the central agent
    agent = CodeAgent(
        tools=[supply_tool, manufacture_tool, distribute_tool, retail_tool],
        model=model
    )

    # Define initial state
    state = {
        "supplier_inventory": 100,
        "manufacturer_capacity": 50,
        "manufacturer_inventory": 0,
        "distributor_inventory": 50,
        "retailer_customer_demand": 30,
        "retail_inventory": 0,
        "backorders": 0,
        "forecast_demand": 30
    }

    # Validate initial state
    validate_state(state)

    # Simulation loop
    for step in range(num_steps):
        print(f"\nStep {step + 1}")
        print("Starting state:", state)
        initial_demand = state["retailer_customer_demand"]

        # 1. Update demand forecast
        state["forecast_demand"] = demand_forecast.forecast()
        print(f"Forecast demand: {state['forecast_demand']}")

        # 2. Supply raw materials
        manufacturer_demand = max(state["forecast_demand"] - state["manufacturer_inventory"], 0)
        supply = supply_tool.forward(manufacturer_demand, state["supplier_inventory"])
        state["supplier_inventory"] -= supply
        print_state_changes(state, step, "Supply", {"Raw materials supplied": supply})
        time.sleep(0.5)  # Simulate lead time

        # 3. Manufacturing
        production = manufacture_tool.forward(
            raw_material=supply,
            capacity=state["manufacturer_capacity"],
            demand=manufacturer_demand
        )
        state["manufacturer_capacity"] -= production
        state["manufacturer_inventory"] += production
        print_state_changes(state, step, "Production", {"Goods manufactured": production})

        # 4. Distribution
        distributor_intake = min(state["manufacturer_inventory"], 50 - state["distributor_inventory"])
        state["manufacturer_inventory"] -= distributor_intake
        state["distributor_inventory"] += distributor_intake

        retail_supply = distribute_tool.forward(
            inventory=state["distributor_inventory"],
            demand=state["retailer_customer_demand"] + state["backorders"]
        )
        state["distributor_inventory"] -= retail_supply
        state["retail_inventory"] += retail_supply

        # 5. Retail sales and backorder management
        total_demand = state["retailer_customer_demand"] + state["backorders"]
        fulfilled_demand = retail_tool.forward(
            customer_demand=total_demand,
            available_stock=state["retail_inventory"]
        )
        state["retail_inventory"] -= fulfilled_demand

        # Update backorders
        new_backorders = total_demand - fulfilled_demand
        state["backorders"] = new_backorders

        # Update metrics
        metrics.update_fill_rate(initial_demand, fulfilled_demand)
        metrics.update_inventory({
            "supplier": state["supplier_inventory"],
            "manufacturer": state["manufacturer_inventory"],
            "distributor": state["distributor_inventory"],
            "retail": state["retail_inventory"]
        })

        # Calculate and update costs
        daily_costs = cost_manager.calculate_costs(state, supply, production, retail_supply)
        metrics.update_costs(daily_costs)

        # 6. Daily updates
        state["manufacturer_capacity"] = 50  # Reset capacity
        state["supplier_inventory"] += random.randint(10, 20)  # Resupply
        state["retailer_customer_demand"] = max(30 + random.randint(-5, 5), 0)  # New demand
        demand_forecast.update(state["retailer_customer_demand"])

        # Print performance metrics
        print("\nPerformance Metrics:")
        current_metrics = metrics.calculate_metrics()
        for metric, value in current_metrics.items():
            print(f"{metric}: {value}")

        print("\nEnd state:", state)

    return metrics.calculate_metrics()

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    final_metrics = run_simulation()
    print("\nFinal Simulation Metrics:")
    for metric, value in final_metrics.items():
        print(f"{metric}: {value}")