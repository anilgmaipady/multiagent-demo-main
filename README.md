## Requirements

```
smolagents==0.1.0
numpy>=1.21.0
```

## Project Structure

```
supply_chain_simulation/
│
├── agents.py          # Core agent definitions
├── utils.py           # Utility classes and functions
├── main.py           # Main simulation runner
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the simulation:
```bash
python main.py
```

## Features

- Multi-agent supply chain simulation
- Advanced demand forecasting
- Performance metrics tracking
- Cost optimization
- Backorder management
- Dynamic inventory adjustments
- Lead time simulation

## Usage

The simulation can be customized by modifying:
1. Initial state parameters in `main.py`
2. Cost structure in `main.py`
3. Forecasting parameters in `utils.py`
4. Simulation steps and random seed in `main.py`


```mermaid
graph TD
  A[Start] --> B{Is it working?}
  B -- Yes --> C[Great!]
  B -- No --> D[Fix it]
  D --> B
