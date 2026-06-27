#Created on Sun Jun 14 16:13:54 2026

import numpy as np #gives maths tools
import matplotlib.pyplot as plt #gives ploting library

from aircraft import selected_aircraft #pull in our aircraft date
from performance import (lift, drag_polar, drag_force, V_liftoff, stall_speed, simulate_ground_roll, rate_of_climb, CL_required, rate_of_decent, cruise_range, final_weight, static_margin)

#___unpack aircraft parmeters___#
rho = selected_aircraft["rho"]
S = selected_aircraft["wing_area"]
k = selected_aircraft["k"]
cd0 = selected_aircraft["cd0"]
T = selected_aircraft["thrust"]
M = selected_aircraft["mass"]
g = selected_aircraft["gravity"]
mu = selected_aircraft["mu"]
CL_max= selected_aircraft["max_lift_coefficient"]
c = selected_aircraft["sfc"]
M_fuel = selected_aircraft["fuel_mass"]
NP = selected_aircraft["neutral_point"]
CG = selected_aircraft["centre_of_gravity"]
chord = selected_aircraft["chord_length"]
TFf = selected_aircraft["takeoff_fuel_fraction"]
CFf = selected_aircraft["climb_fuel_fraction"]
DFf = selected_aircraft["descent_fuel_fraction"]
W_fuel = M_fuel * g
W = M * g

V_stall = stall_speed(W, rho, S, CL_max) # minimum speed before the wing stall
W_final = final_weight(W, W_fuel)

CL = 1.0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Lift and Drag vs Velocity - Steady Level Flight Analysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#___build velocity range___#
V_range = np.linspace(50,300,200) #np.linspace(start,finish,no.of points)

#___calculate forces across all velocities ___#
L_values = [lift(rho, V, S, CL) for V in V_range] #produces lift values for all the velocities in v_range

CD_values = [drag_polar(cd0, k, CL) for V in V_range]
D_values = [drag_force(rho, V, S, CD) for V, CD in zip(V_range, CD_values)] # zip pairs up V_range and CD_vlaues so we can use both in the same loop

#___build the plot___#
plt.figure(figsize=(10, 6)) #figsize=(width, height) in inches controls how high and wide the window is

plt.plot(V_range, L_values, label = "Lift (N)", color = "blue") # plt.plot(x_values, y_values)
plt.plot(V_range, D_values, label = "Drag (N)", color = "orange") #label = what actually shows up in the legend

plt.axhline(y = W, color = "red", linestyle = "--", label = "Weight (N)") # axhline draws horizontail line across the whole plot at fixed value of y. 
#this shows the weight, where lift cross this line is the minimum level flight speed required
plt.axhline(y = T, color = "green", linestyle = "--", label = "Thrust (N)") # this shows thrust, where drag crosses this line is max level flight speed

#___labels and formating___#
plt.xlabel("Velocity (m/s)") # x axis label
plt.ylabel("Force (N)") # y axis label
plt.title("Lift and Drag vs Velocity - Steady Level Flight Analysis")
plt.legend() # draws the legend box using all the label = values above
plt.grid(True) # adds gridlines - makes it easier to read values
plt.tight_layout() # automatically adjusts spacing so nothing gets cut off
plt.show() # opens the plot view - nothing appears until you call this

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Velocity vs Distance - Ground Roll Analysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

V_to = V_liftoff(V_stall) # liftoff speed = 1.2 * stall speed (safety margin)

s_list, V_list = simulate_ground_roll(V_to, T, W, rho, S, cd0, k, mu, M, CL_max) # simulate ground roll, and returns distance and velocity lists for plotting

#___build the plot___#
plt.figure(figsize=(10,6)) #figssize = (weight, height) in inches controls how high and wide a window is.

plt.plot(s_list, V_list, label = "Velocity During Ground Roll", color = "blue") # plt.plot(x_values, y_values). label = what actually shows up in the legend

plt.xlabel("Distance (m)") # x axis label
plt.ylabel("Velocity (m/s)") # y axis label
plt.title("Velocity vs Distance - Ground Roll Analysis")
plt.legend() # draws the legend box using all the label = values above
plt.grid(True) # adds gridlines - makes it easier to read values
plt.tight_layout() # automatically adjusts spacing so nothing gets cut off
plt.show() # opens the plot view - nothing appears until you call this

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Rate of Climb vs Velocity ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#___build velocity range___#
V_range = np.linspace(V_stall + 5,250,200) #np.linspace(start,finish,no.of points)

#___calculate force and RC across all velocities ___#
CL_values = [min(CL_required(W, rho, V, S),CL_max) for V in V_range]
CD_values = [drag_polar(cd0, k, CL) for CL in CL_values] #produces drag coefficient values for all the velocities in v_range
D_values = [drag_force(rho, V, S, CD) for V, CD in zip(V_range, CD_values)] # zip pairs up V_range and CD_vlaues so we can use both in the same loop

RC_values = [rate_of_climb(T, W, D, V) for D, V in zip(D_values, V_range)]


#___build the plot___#
plt.figure(figsize=(10,6)) #figsize=(width, height) in inches controls how high and wide the window is

plt.plot(V_range, RC_values, label = "Rate of Climb (m/s)", color = "blue")# plt.plot(x_values, y_values) #label = what actually shows up in the legend

#___labels and formating___#
plt.xlabel("Velocity (m/s)")
plt.ylabel("Rate of Climb (m/s)")
plt.title("Rate of Climb vs Velocity")
plt.legend() # draws the legend box using all the label = values above
plt.grid(True) # adds gridlines - makes it easier to read values
plt.tight_layout() # automatically adjusts spacing so nothing gets cut off
plt.show() # opens the plot view - nothing appears until you call this

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Rate of Descent vs Velocity ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#___build velocity range___#
V_range = np.linspace(V_stall + 5,250,200) #np.linspace(start,finish,no.of points)

#___calculate force and RD across all velocities ___#
CL_values = [min(CL_required(W, rho, V, S),CL_max) for V in V_range]
CD_values = [drag_polar(cd0, k, CL) for CL in CL_values] #produces drag coefficient values for all the velocities in v_range
D_values = [drag_force(rho, V, S, CD) for V, CD in zip(V_range, CD_values)] # zip pairs up V_range and CD_vlaues so we can use both in the same loop

RD_values = [rate_of_decent(D, 0, V, W) for D, V in zip(D_values, V_range)]# zip pairs up D_values and V_range so we can use both in the same loop

#___build the plot___#
plt.figure(figsize=(10,6)) #figsize=(width, height) in inches controls how high and wide the window is

plt.plot(V_range, RD_values, label = "Rate of Descent (m/s)", color = "blue")# plt.plot(x_values, y_values) #label = what actually shows up in the legend

#___labels and formating___#
plt.xlabel("Velocity (m/s)")
plt.ylabel("Rate of Descent (m/s)")
plt.title("Rate of Descent vs Velocity")
plt.legend() # draws the legend box using all the label = values above
plt.grid(True) # adds gridlines - makes it easier to read values
plt.tight_layout() # automatically adjusts spacing so nothing gets cut off
plt.show() # opens the plot view - nothing appears until you call this

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Cruise Range vs Velocity ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#___build velocity range___#
V_range = np.linspace(V_stall + 5,250,200) #np.linspace(start,finish,no.of points)

CL_values = [min(CL_required(W, rho, V, S),CL_max) for V in V_range]
CD_values = [drag_polar(cd0, k, CL) for CL in CL_values] #produces drag coefficient values for all the velocities in v_range
L_values = [lift(rho, V, S, CL) for V, CL in zip(V_range, CL_values)]
D_values = [drag_force(rho, V, S, CD) for V, CD in zip(V_range, CD_values)] # zip pairs up V_range and CD_vlaues so we can use both in the same loop


R_values = [cruise_range(V, c, L, D, W, W_final, rho, S) for L, D, V in zip(L_values, D_values, V_range)]

#___build the plot___#
plt.figure(figsize=(10,6)) #figsize=(width, height) in inches controls how high and wide the window is

plt.plot(V_range, R_values, label = "Cruise Range (m)", color = "blue")# plt.plot(x_values, y_values) #label = what actually shows up in the legend

#___labels and formating___#
plt.xlabel("Velocity (m/s)")
plt.ylabel("Cruise Range (m)")
plt.title("Cruise Range vs Velocity")
plt.legend() # draws the legend box using all the label = values above
plt.grid(True) # adds gridlines - makes it easier to read values
plt.tight_layout() # automatically adjusts spacing so nothing gets cut off
plt.show() # opens the plot view - nothing appears until you call this

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#___build centre of gravity range___#
CG_range = np.linspace(NP - 5, NP + 5, 200) #np.linspace(start,finish,no.of points)
SM_value = [static_margin (NP, CG, chord) for CG in CG_range]

#___build the plot___#
plt.figure(figsize = (10,6)) #figsize=(width, height) in inches controls how high and wide the window is

plt.plot(CG_range, SM_value, label = "Static Margin", color = "blue")# plt.plot(x_values, y_values) #label = what actually shows up in the legend

 #___labels and formating___#
plt.xlabel("Centre of Gravity (m)")
plt.ylabel("Static Margin")
plt.title("Static Margin vs Centre of Gravity")
plt.legend() # draws the legend box using all the label = values above
plt.grid(True) # adds gridlines - makes it easier to read values
plt.tight_layout() # automatically adjusts spacing so nothing gets cut off
plt.show() # opens the plot view - nothing appears until you call this

