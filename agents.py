from smolagents import Tool

class SupplyTool(Tool):
    name = "supply_tool"
    description = "Supplies raw materials to the manufacturer."
    inputs = {
        "demand": {"type": "number", "description": "Demand from manufacturer"},
        "inventory": {"type": "number", "description": "Supplier's current inventory"}
    }
    output_type = "number"

    def forward(self, demand: int, inventory: int) -> int:
        supply = min(inventory, demand)
        return supply

class ManufactureTool(Tool):
    name = "manufacture_tool"
    description = "Manufactures goods based on raw materials and demand."
    inputs = {
        "raw_material": {"type": "number", "description": "Raw materials available"},
        "capacity": {"type": "number", "description": "Manufacturing capacity"},
        "demand": {"type": "number", "description": "Production demand"}
    }
    output_type = "number"

    def forward(self, raw_material: int, capacity: int, demand: int) -> int:
        production = min(capacity, raw_material, demand)
        return production

class DistributeTool(Tool):
    name = "distribute_tool"
    description = "Distributes goods to retailers based on demand."
    inputs = {
        "inventory": {"type": "number", "description": "Distributor's inventory"},
        "demand": {"type": "number", "description": "Retailer demand"}
    }
    output_type = "number"

    def forward(self, inventory: int, demand: int) -> int:
        supply = min(inventory, demand)
        return supply

class RetailTool(Tool):
    name = "retail_tool"
    description = "Fulfills customer demand based on available stock."
    inputs = {
        "customer_demand": {"type": "number", "description": "Customer's demand"},
        "available_stock": {"type": "number", "description": "Stock available at retail"}
    }
    output_type = "number"

    def forward(self, customer_demand: int, available_stock: int) -> int:
        fulfilled_demand = min(customer_demand, available_stock)
        return fulfilled_demand