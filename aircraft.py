#Created on Sun Jun 14 15:57:04 2026

#___aircraft.py stores aircrafts fixed physical perameters___#

aircraft_1 = {
    "mass": 60000,
    "wing_area": 120,
    "cd0": 0.02,                  # zero lift drag coefficient (this is parasitic drag when producing no lift)
    "k": 0.045,                   # induced drag factor (drag caused by generating lift)
    "thrust": 120000,
    "rho": 1.225,
    "gravity": 9.81,
    "max_lift_coefficient": 2.0,  # max CL a wing can produce before stall
    "mu": 0.02,                   # rolling friction coefficient on tarmac during ground roll
    "fuel_mass": 15000,
    "sfc": 0.00006,
    "centre_of_gravity": 25,      # centre of gravity location, metres from nose
    "neutral_point": 25.4,        # neutral point location, metres from nose
    "chord_length": 4,            # mean wing chord length, metres - needed to normalise static margin}   #  specific fuel consumption (kg/N/s) - typical jet engine value
    "takeoff_fuel_fraction": 0.03,   # ~3% of fuel burned during takeoff
    "climb_fuel_fraction": 0.05,     # ~5% of fuel burned during climb
    "descent_fuel_fraction": 0.01,   # ~1% - mostly idle thrust
}

aircraft_2 = {
    "mass": 40000,                   # smaller - regional/short-haul jet
    "wing_area": 80,
    "cd0": 0.022,                    # slightly higher - less aerodynamically refined
    "k": 0.05,
    "thrust": 110000,                 # less powerful engines
    "rho": 1.225,
    "gravity": 9.81,
    "max_lift_coefficient": 1.8,
    "mu": 0.02,
    "fuel_mass": 6000,                # much less fuel - short routes don't need it
    "sfc": 0.00007,                   # slightly less efficient engine
    "centre_of_gravity": 18,
    "neutral_point": 18.3,
    "chord_length": 3,
    "takeoff_fuel_fraction": 0.04,    # higher % - short flights spend proportionally more on takeoff
    "climb_fuel_fraction": 0.08,      # same reasoning - climb is a bigger share of a short flight
    "descent_fuel_fraction": 0.02,
}

# pick which aircraft to analyse - change this one line to switch
selected_aircraft = aircraft_2