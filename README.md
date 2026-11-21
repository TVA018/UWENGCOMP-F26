# University of Waterloo Engineering Competition Fall 2026
## Objective
- Managing a electrical grid
  - Backup generator
  - Meet the energy demand of every building
  - Manage available energy sources
  - Respond to Changing Conditions
- Computational problem
## 1.2 Background Information
The campus microgrid supplies electricity to five buildings:
- Library
- Laboratory
- Lecture Hall
- Student Centre
- Student Residence

Each building has its own electricity demand, which changes throughout the day. Electricity can be supplied through solar generation, battery storage, or the electrical grid.
Due to their old age, the lecture halls do not have solar panels installed and cannot be powered with solar energy.
A backup generator is also available to recharge the shared battery, allowing energy to be stored for future use.
Electricity purchased from the grid and energy produced by the generator have associated operating costs. Solar energy is available at no additional operating cost, but its availability may be affected by weather conditions.
The microgrid operates over a simulated 24-hour period, with the controller making decisions once per hour.

During the simulation, random events may occur that alter grid operations or component availability. These conditions are introduced through various random events:

| Random Events | Description |
|---|---|
| "cloudy_weather" | Solar power can’t be used |
| "generator_failure" | Generator can't be used |
| "battery_failure" | Battery can't be used | 
| "grid_failure" | Grid can't be used |

## 1.3	Problem Statement
Your team has six hours to develop an automated campus microgrid controller.
Your program must determine how electricity should be distributed among campus buildings while minimizing total operating costs. Throughout the simulation, your controller will encounter changing electricity demands and unexpected events that may temporarily restrict the availability of certain energy sources.
Your solution must respond to these conditions automatically, ensuring that each building receives sufficient electricity without violating the operating constraints of the microgrid.

## 1.4 Design Objective
The objective is to design a controller capable of operating the campus microgrid over a simulated 24-hour period at the lowest possible total cost.
At each hour, your controller will receive updated information about campus electricity demand and any unexpected operating conditions.

Your controller must determine how much electricity to allocate from each available source.

| Energy Source | Operating Cost | Constraints |
|---|---|---|
| Solar | $0/unit | Only 200 units of energy can be generated per hour |
| Electrical Grid | Fluctuates | None |
| Backup Generator | $1.00/unit | Has a capacity of 100 units. Attempting to charge it past its capacity will cause an error. |

Demands throughout the day will fluctuate, you must make a design that is able to handle unknown variables.