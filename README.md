# Aircraft Performance Model

A Python-based aircraft performance model built from first principles, covering five major flight phases and integrated into a single end-to-end mission simulation. Built as a personal engineering project to apply core aerodynamics and flight mechanics theory to a working computational tool.

## What this does

The model calculates and visualises:

- **Steady level flight** — lift/drag balance, force equilibrium
- **Takeoff performance** — stall speed, liftoff speed, ground roll distance (analytical and numerical methods)
- **Climb and descent** — rate of climb, glide performance, best glide speed
- **Cruise and range** — Breguet range equation, fuel burn, max range vs max endurance speed
- **Longitudinal static stability** — centre of gravity, neutral point, static margin

All five phases are chained into a single `mission_profile()` function that tracks aircraft weight as fuel is consumed throughout a full flight — takeoff through descent — rather than treating each phase in isolation.

The model is applied to two contrasting aircraft configurations (long-haul vs short-haul) to demonstrate how thrust-to-weight ratio and mission profile drive real performance trade-offs.

## Key result

One of the more interesting findings to come out of this project: **maximum range speed and maximum endurance speed are not the same speed.** Initially this looked like a bug in my code — the plotted range peak didn't match my calculated best glide speed. It turned out to be correct, well-established aerospace behaviour:

```
V_max_range = 3^(1/4) × V_max_endurance ≈ 1.316 × V_max_endurance
```

Full explanation and derivation is in the [final report](./report/Aircraft_Performance_Final_Report.docx).

## Project structure

```
.
├── aircraft.py        # Aircraft parameter dictionaries (mass, geometry, aerodynamics, fuel data)
├── performance.py     # All physics functions — lift, drag, takeoff, climb/descent, cruise, stability
├── main.py            # Runs the model, prints results
├── plots.py           # Generates all visualisations
└── report/
    └── Aircraft_Performance_Final_Report.docx
```

Each file has one job. Physics lives in `performance.py` only — if an equation needs fixing, it only needs fixing in one place.

## Sample results

| Metric | Long-haul aircraft | Short-haul aircraft |
|---|---|---|
| Takeoff distance | 4,242.7 m | 2,265.2 m |
| Rate of climb | 11.15 m/s | 18.06 m/s |
| Max cruise range | 10,477.5 km | 4,346.3 km |
| Glide rate of descent | 5.70 m/s | 6.73 m/s |

## Running it

```
pip install numpy matplotlib
python main.py     # prints all calculated performance figures
python plots.py    # generates all six plots
```

To switch between aircraft configurations, change one line in `aircraft.py`:

```
selected_aircraft = aircraft_1   # or aircraft_2
```

## Methodology notes

This model operates at conceptual design level — the level of fidelity used early in aircraft design to compare configurations before detailed engineering analysis. Several simplifications were made deliberately and are documented explicitly in the final report, including:

- A cruise-climb assumption for the range equation (standard for Breguet range analysis)
- Fixed empirical fuel fractions for takeoff/climb/descent (the standard "fuel fraction method")
- A ratio-based approximation for best climb speed, since no closed-form solution exists

Full reasoning and limitations are documented in the [final report](./report/Aircraft_Performance_Final_Report.docx).

## Background

Built independently over several weeks as a personal portfolio project, structured around progressively building up each flight phase before integrating them into a single mission simulation.