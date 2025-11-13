# Predictive Multi-Objective Scheduler

Advanced carbon-aware scheduler with time-series forecasting and multi-objective optimization.

## Features

### 1. **Time-Series Forecasting**
- Uses **Prophet** (Facebook's time series forecasting library)
- Predicts future carbon intensity based on historical patterns
- Supports forecasting 1-24 hours ahead
- Captures daily and weekly seasonality

### 2. **Multi-Objective Optimization**
Balances three objectives with weighted scoring:

| Objective | Weight | Description |
|-----------|--------|-------------|
| 🌱 **Carbon** | 50% (default) | Minimize carbon intensity (gCO2/kWh) |
| ⚡ **Latency** | 30% (default) | Minimize network latency (ms) |
| 💰 **Cost** | 20% (default) | Minimize regional compute cost ($/vCPU-hour) |

**Weighted Score Formula:**
```
score = w_carbon × norm_carbon + w_latency × norm_latency + w_cost × norm_cost
```

Where each metric is normalized to [0, 1] range.

### 3. **Pareto Frontier Analysis**
- Generates Pareto-optimal solutions for any two objectives
- Identifies regions where no improvement can be made without trade-offs
- Visualizes optimal trade-off curve

## Regional Data

### Network Latency (from asia-south1)
- 🇮🇳 Mumbai (IN): **10ms** (same region)
- 🇯🇵 Tokyo (JP): **90ms**
- 🇦🇺 Sydney (AU-NSW): **140ms**
- 🇩🇪 Frankfurt (DE): **150ms**
- 🇫🇮 Finland (FI): **180ms**
- 🇧🇷 São Paulo (BR-CS): **350ms**

### Regional Costs (USD per vCPU-hour)
- 🇧🇷 Brazil (BR-CS): **$0.0450**
- 🇩🇪 Germany (DE): **$0.0475**
- 🇮🇳 India (IN): **$0.0476**
- 🇯🇵 Japan (JP): **$0.0560**
- 🇫🇮 Finland (FI): **$0.0570**
- 🇦🇺 Australia (AU-NSW): **$0.0595**

## Usage

### Python API

```python
from scheduler.predictive_scheduler import PredictiveScheduler

# Initialize scheduler
scheduler = PredictiveScheduler(firestore_project_id="cass-lite")

# Carbon-optimized (70% carbon, 20% latency, 10% cost)
result = scheduler.select_optimal_region(
    w_carbon=0.7,
    w_latency=0.2,
    w_cost=0.1,
    use_prediction=True,
    hours_ahead=1
)

print(f"Optimal Region: {result['region']}")
print(f"Carbon: {result['carbon_intensity']:.0f} gCO2/kWh")
print(f"Latency: {result['latency']}ms")
print(f"Cost: ${result['cost']:.4f}/vCPU-hour")
print(f"Score: {result['score']:.3f}")

# Generate Pareto frontier
pareto = scheduler.generate_pareto_frontier('carbon', 'latency')
```

### Dashboard Integration

The dashboard includes an interactive **Multi-Objective Optimization** section:

1. **Adjust Weights** - Use sliders to prioritize different objectives
2. **Enable Forecasting** - Toggle Prophet predictions
3. **Optimize** - Find the best region for your weights
4. **View Pareto Curve** - See optimal trade-offs visualized

## Example Scenarios

### Scenario 1: Green First (Environmental Focus)
```python
result = scheduler.select_optimal_region(
    w_carbon=0.8,  # 80% carbon priority
    w_latency=0.1,  # 10% latency
    w_cost=0.1      # 10% cost
)
# Likely selects: Finland (FI) - lowest carbon despite higher latency
```

### Scenario 2: Performance First (Low Latency)
```python
result = scheduler.select_optimal_region(
    w_carbon=0.2,  # 20% carbon
    w_latency=0.7,  # 70% latency priority
    w_cost=0.1      # 10% cost
)
# Likely selects: India (IN) - lowest latency from asia-south1
```

### Scenario 3: Cost First (Economic Efficiency)
```python
result = scheduler.select_optimal_region(
    w_carbon=0.2,  # 20% carbon
    w_latency=0.2,  # 20% latency
    w_cost=0.6      # 60% cost priority
)
# Likely selects: Brazil (BR-CS) - lowest cost
```

### Scenario 4: Balanced (Default)
```python
result = scheduler.select_optimal_region(
    w_carbon=0.5,  # 50% carbon
    w_latency=0.3,  # 30% latency
    w_cost=0.2      # 20% cost
)
# Balances all three objectives
```

## How It Works

### 1. Data Collection
- Fetches current carbon intensity from ElectricityMap API
- Queries Firestore for historical carbon data (168 hours)
- Uses regional latency and cost constants

### 2. Forecasting (Optional)
- Trains Prophet model on historical data
- Requires minimum 48 data points (2 days)
- Predicts carbon intensity 1-24 hours ahead
- Captures daily/weekly patterns

### 3. Normalization
```python
normalized = (value - min_value) / (max_value - min_value)
```
Each objective scaled to [0, 1] for fair comparison.

### 4. Scoring
```python
score = w_carbon × carbon_norm + w_latency × latency_norm + w_cost × cost_norm
```
Lower score = better overall performance.

### 5. Selection
Region with minimum weighted score is selected.

## Pareto Frontier

**Definition:** Set of solutions where improving one objective requires worsening another.

**Example:** Carbon vs Latency
- Finland: Low carbon (40 gCO2), High latency (180ms) ✅ Pareto-optimal
- India: High carbon (508 gCO2), Low latency (10ms) ✅ Pareto-optimal
- Germany: Medium carbon (265 gCO2), Medium latency (150ms) ❌ Dominated by Finland & India

## Dependencies

```bash
pip install prophet pandas numpy google-cloud-firestore
```

## API Reference

### `PredictiveScheduler`

**Methods:**

- `select_optimal_region(w_carbon, w_latency, w_cost, use_prediction, hours_ahead)` - Find optimal region
- `predict_carbon_intensity(region, hours_ahead)` - Forecast carbon intensity
- `generate_pareto_frontier(objective1, objective2)` - Generate Pareto-optimal points
- `fetch_historical_data(region, hours)` - Query historical Firestore data

**Returns:**
```python
{
    'success': True,
    'region': 'FI',
    'carbon_intensity': 42.5,
    'latency': 180,
    'cost': 0.057,
    'score': 0.423,
    'weights': {'carbon': 0.5, 'latency': 0.3, 'cost': 0.2},
    'all_candidates': [...],
    'timestamp': '2025-11-13T10:30:00'
}
```

## Performance

- **Optimization:** < 1 second (without forecasting)
- **Forecasting:** 2-5 seconds per region (with Prophet)
- **Pareto Generation:** < 100ms

## Limitations

- Forecasting requires ≥48 historical data points
- Latency values are estimates (not real-time measurements)
- Cost data based on Google Cloud pricing (Nov 2025)
- Prophet model trained per-request (not cached)

## Future Enhancements

- [ ] Cache Prophet models for faster predictions
- [ ] Real-time latency measurements
- [ ] Dynamic cost API integration
- [ ] Multi-cloud support (AWS, Azure regions)
- [ ] GPU/TPU regional pricing
- [ ] Renewable energy mix consideration

---

**Built with ❤️ for a greener, faster, cheaper cloud.**
