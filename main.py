#Created on Sun Jun 14 16:03:03 2026

from aircraft import selected_aircraft 
from performance import (lift, drag_polar, drag_force, CL_required, steady_flight, stall_speed, V_liftoff, takeoff_distance, rate_of_climb, rate_of_decent, best_glide_CL, best_glide_speed, final_weight, cruise_range, max_range_speed, static_margin, check_stability, mission_profile)

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


#___test conditions___#
V = 70   # test velocity (m/s), not liftoff speed, just a cruise speed
CL = 1.0  # assumed lift coefficient for steady flight check

#___steady level flight___#
L = lift(rho, V, S, CL)
CD = drag_polar(cd0, k, CL)
D = drag_force(rho, V, S, CD)
CL_req = CL_required(W, rho, V, S)



#___takeoff___#
V_stall = stall_speed(W, rho, S, CL_max)
V_to = V_liftoff(V_stall)
s = takeoff_distance(V_to, W, rho, S, mu, T, M, cd0, k)

#___the rates of climb and descent___#
RC = rate_of_climb(T, W, D, V) # uses test conditons v =70
RD = rate_of_decent(D, 0, V, W) # assuming glide T =0
CL_opt = best_glide_CL(cd0, k) # best L/D ratio
glide_V_opt = best_glide_speed(W, CL_opt, rho, S) # speed reqiured to fly at CL_opt

#___maxmum distance traveled and its volocity___#
V_max_range = max_range_speed(glide_V_opt)
W_final = final_weight(W, W_fuel)
CD_opt = drag_polar(cd0, k, CL_opt)
L_opt = lift(rho, V_max_range, S, CL_opt)
D_opt = drag_force(rho, V_max_range, S, CD_opt)
R_max = cruise_range(V_max_range, c, L_opt, D_opt, W, W_final, rho, S)

#___stability___#
SM = static_margin(NP, CG, chord)


#___outputs___#
print(f"Lift: {L:.2f} N")
print(f"drag: {D:.2f} N")
steady_flight(L, W, T, D, tol=100)
print(f"CL required for level flight at V={V} m/s : {CL_req:.2f}")
print(f"The lift off speed: {V_to:.2f} m/s")
print(f"the take off distance is {s:.2f} m")
print(f"rate of climb: {RC:.2f} m/s") 
print(f"glide rate of decent: {RD:.2f} m/s")
print(f"best coefficient of lift: {CL_opt:.2f}") 
print(f"best glide speed: {glide_V_opt:.2f} m/s")
print(f"max range speed: {V_max_range:.2f} m/s")
print(f"the max cruise range is: {R_max / 1000 :.1f} km") 
check_stability(SM)

#___mission profile___#
s, RC, R_max, RD, W = mission_profile(M, cd0, c, k, T, rho, g, CL_max, mu, W_fuel, CG, NP, TFf, CFf, DFf, chord, S)
print("**************************************")
print(f"the take off distance is {s:.2f} m")
print(f"rate of climb: {RC:.2f} m/s")
print(f"the max cruise range is: {R_max / 1000 :.1f} km")
print(f"glide rate of decent: {RD:.2f} m/s")
print(f"final weight: {W:.2f} N")


