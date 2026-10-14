# AMPRODE-AI ⚡

**AI-assisted energy optimization for factories and commercial facilities.**

AMPRODE-AI is a software prototype that compares a grid-only baseline with an energy plan that prioritizes available solar power and uses battery storage when appropriate. It helps users explore electricity costs, estimated savings, and energy-demand patterns.

> **Prototype note:** The initial version uses user-adjustable sample/simulated values. Results are estimates for demonstration, not guaranteed real-world savings or a replacement for a certified energy-management system.

## Features

- Interactive energy dashboard
- Solar, grid, and battery scenario inputs
- Baseline vs. optimized estimated-cost comparison
- Estimated monthly savings and savings percentage
- Transparent assumptions and simple charts

## Built with

- Python
- Streamlit
- Pandas
- Plotly

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Open the local address shown in your terminal.

## How the demo works

1. Enter daily electricity demand, available solar energy, grid tariff, and battery settings.
2. AMPRODE-AI estimates a simple solar-first dispatch plan.
3. Review estimated grid energy required, baseline cost, optimized cost, and potential savings.

## Important limitations

This is an early hackathon prototype. It does not yet connect to live meters, utility tariffs, weather forecasts, or physical batteries. Battery efficiency, capacity, and available solar energy are simplified assumptions. Validate the model against actual site data before making operational decisions.

## Roadmap

- Add historical energy-data upload
- Add demand forecasting
- Add time-of-use tariff schedules
- Add more detailed battery constraints
- Evaluate estimates against real facility data

**Project:** AMPRODE-AI  
**Focus:** AI-assisted solar, battery, and grid energy optimization
