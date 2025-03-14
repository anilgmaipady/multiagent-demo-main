# main.py
from smolagents import CodeAgent, HfApiModel
import random
import time

from agents import SupplyTool, ManufactureTool, DistributeTool, RetailTool
from utils import DemandForecast, PerformanceMetrics, CostManager, print_state_changes, validate_state

# Import our automl predictor function
from automl_predictor import predict_action

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
        "retail_inventory": 0,
        "retailer_customer_demand": 40,
        "backorders": 0,
        "forecast_demand": 40
    }
    validate_state(state)

    for step in range(num_steps):
        print(f"\nStep {step + 1}")
        print("Starting state:", state)
        
        # Update demand forecast (example)
        state["forecast_demand"] = demand_forecast.forecast()
        print(f"Forecast demand: {state['forecast_demand']}")

        # Use our AutoML predictor to decide which action to run
        predicted_action = predict_action(state)
        print("Predicted action from AutoML:", predicted_action)

        # Use dynamic decision to run the corresponding tool
        if predicted_action == "supply":
            manufacturer_demand = max(state["forecast_demand"] - state["manufacturer_inventory"], 0)
            supply = supply_tool.forward(manufacturer_demand, state["supplier_inventory"])
            state["supplier_inventory"] -= supply
            print_state_changes(state, step, "Supply", {"Raw materials supplied": supply})
            time.sleep(0.5)  # Simulate lead time

        elif predicted_action == "manufacture":
            production = manufacture_tool.forward(
                raw_material=state["manufacturer_inventory"],
                capacity=state["manufacturer_capacity"],
                demand=state["retailer_customer_demand"] + state["backorders"]
            )
            state["manufacturer_capacity"] -= production
            state["manufacturer_inventory"] += production
            print_state_changes(state, step, "Production", {"Goods manufactured": production})

        elif predicted_action == "distribute":
            distributor_intake = min(state["manufacturer_inventory"], 50 - state["distributor_inventory"])
            state["manufacturer_inventory"] -= distributor_intake
            state["distributor_inventory"] += distributor_intake
            retail_supply = distribute_tool.forward(
                inventory=state["distributor_inventory"],
                demand=state["retailer_customer_demand"] + state["backorders"]
            )
            state["distributor_inventory"] -= retail_supply
            state["retail_inventory"] += retail_supply
            print_state_changes(state, step, "Distribution", {"Retail supply": retail_supply})

        else:
            print("Unknown action predicted. Executing default supply action.")
            manufacturer_demand = max(state["forecast_demand"] - state["manufacturer_inventory"], 0)
            supply = supply_tool.forward(manufacturer_demand, state["supplier_inventory"])
            state["supplier_inventory"] -= supply
            print_state_changes(state, step, "Supply (default)", {"Raw materials supplied": supply})

        # Other simulation steps: backorder management, cost calculations, etc.
        # For example:
        # ... (rest of simulation logic)
        
        # Update metrics, adjust state for the next step, etc.
        # Reset capacities, resupply inventories, etc.
        state["manufacturer_capacity"] = 50  # reset capacity
        state["supplier_inventory"] += random.randint(10, 20)  # simulate resupply
        state["retailer_customer_demand"] = max(40 + random.randint(-5, 5), 0)  # update demand
        demand_forecast.update(state["retailer_customer_demand"])

        # Print performance metrics at the end of the step
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
