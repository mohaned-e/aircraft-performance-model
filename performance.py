#Created on Sun Jun 14 16:02:19 2026

import math as ma

#___every physics calculation lives here in performance.py___#

def lift(rho, V, S, CL):  # calculates the aerodynamic lift in newtons using L = 0.5 × rho × V² × S × CL
    return 0.5 * rho * V**2 * S * CL

def drag_polar(cd0, k, CL):  # returns the total drag coefficient CD using CD = cd0 + k × CL²
    return cd0 + k * CL**2

def drag_force(rho, V, S, CD):  # converts the CD into actual drag force in newtons using D = 0.5 × rho × V² × S × CD 
    return 0.5 * rho * V**2 * S * CD

def CL_required(W, rho, V, S):  # calculates what lift coeiffient  the aircraft needs at a givien speed to sustain level flight using CL_req = W / (0.5 × rho × V² × S) 
    return W / (0.5 * rho * V**2 * S)  # if CL_req > CL_max than aircraft stalls

def steady_flight(L, W, T, D, tol=100): # checks wether the aircraft is in steady flight by testing two conditions: lift = weight and thrust = drag
    lift_ok = abs(L - W) < tol
    thrust_ok = abs(T - D) < tol
    print(f"  lift={L:.1f}N, weight={W:.1f}N - {'OK' if lift_ok else 'NOT balanced'}")
    print(f"  thrust={T:.1f}N, drag={D:.1f}N - {'OK' if thrust_ok else 'Not balanced'}")
    return lift_ok and thrust_ok

def stall_speed(W, rho, S, CL_max): # calculate the minimum speed at which aircraft can fly, stall speed. derived by rearranging the lift equation with L = W and CL = CL_max
    return (2 * W / (rho * S * CL_max))**0.5 # V_stall = sqrt(2W / (rho × S × CL_max))

def V_liftoff(V_stall): # calculates the speed at which the aircraft actually leaves the ground, aircraft never lifts off at exactly stall speed so a 20% margin is applied
    return 1.2 * V_stall

def takeoff_distance(V_to, W, rho, S, mu, T, M, cd0, k):
    V_avg = V_to * 0.7 #analytical method assumes average conditons occurs at 70% of take off speed
    CL = CL_required(W, rho, V_avg, S) 
    CD = drag_polar(cd0, k, CL)
    D = drag_force(rho, V_avg, S, CD)
    L = lift(rho, V_avg, S, CL) # use this average velocity to calculate your other values
    F_friction = mu * (W - L) # as lift increases there is less weight on wheels and therefore less friction
    resultant_force = T - D - F_friction
    acceleration = resultant_force / M # newtons 2nd law
    return V_to**2 / (2 * acceleration) # estimating take off distance by using  kinematic equation

def simulate_ground_roll(V_to, T, W, rho, S, cd0, k, mu, M, CL_max):
    V = 0.00000001
    s = 0    # initial values of s and V
    dt = 0.1 # time steps of the simulation
    V_list = []
    s_list = [] # lists created for later use in ploting graphs
    while V < V_to: # continues the simulation ontil the take off speed is reached
        CL = CL_required(W, rho, V, S) 
        CL = min(CL, CL_max) # cap CL at max and prevent overflow at near-zero speeds
        CD = drag_polar(cd0, k, CL)
        L = lift(rho, V, S, CL)
        D = drag_force(rho, V, S, CD)
        F_friction = mu * (W - L) # friction reduces as lift icreases due to less weight on wheels
        resultant_force = T - D - F_friction
        acceleration = resultant_force / M
        V = V + acceleration * dt # numerical integration - update velocity
        s = s + V * dt  # numerical integration - update distance
        V_list.append(V)
        s_list.append(s)
    return s_list, V_list # numerical method - more accurate than analytical 

def rate_of_climb(T, W, D, V): # excess thrust converted to clime rate RC = (T-D)×V / W
    return ((T - D) * V)/W

def rate_of_decent(D, T, V, W): # mirror of climb rate  - if T = 0 this is pure glide descent (sink rate)
    return (D - T) * V/ W

def best_glide_CL(cd0, k): # CL required (CL_opt) for best L/D ratio - gives most efficient glide (longest distance travelled)
    return (cd0 / k)**0.5

def best_glide_speed(W, CL_opt, rho, S): # speed required to produce CL_opt - this is the best actual glide speed
    return (2 * W / (CL_opt * rho * S))**0.5

def max_range_speed(glide_V_opt): # max range speed = 3^(1/4) × best glide speed (~1.316×) — a known result for jet aircraft, trades slightly higher drag for more distance covered per unit fuel
    return 3**0.25 * glide_V_opt

def final_weight(W, W_fuel): # weight of aircraft after fuel has been burnt
    return W - W_fuel

def cruise_range(V, c, L, D, W, W_final, rho, S): # the distance travelled by air craft for a given velocity
    return (V / c) * (L / D) * ma.log(W / W_final)

def static_margin (NP, CG, chord): # SM = (NP - CG)/chord - means CG ahead of NP (stable), negative  means NP ahead of CG (unstable)
    return (NP - CG) / chord

def check_stability(SM): # clssifies SM into design bands - order matters here by checking most extreme cases first
    if SM < 0:
        print(f"Static margin {SM:.3f} — UNSTABLE (CG behind neutral point)")
    elif SM < 0.05:
        print(f"Static margin {SM:.3f} — marginally stable (below typical 5% minimum)")
    elif SM <= 0.15:
        print(f"Static margin {SM:.3f} — well stable (typical design range)")
    else:
        print(f"Static margin {SM:.3f} — overly stable (likely sluggish controls)")
    return SM

# Mission profile chains all five flight phases together sequentially,
# updating aircraft weight after each phase as fuel is burned.
# Unlike earlier weeks where every phase used a fixed full weight,
# this function tracks W as a running value that decreases throughout the mission.
def mission_profile(M, cd0,c , k, T, rho, g, CL_max, mu, W_fuel, CG, NP, TFf, CFf, DFf, chord, S):
   W = M * g
   
   # takeoff uses full weight - aircraft hasn't burned any fuel yet
   V_stall = stall_speed(W, rho, S, CL_max)
   V_to = V_liftoff(V_stall)
   s = takeoff_distance(V_to, W, rho, S, mu, T, M, cd0, k)
   W = W - TFf * W_fuel # subtract takeoff fuel AFTER calculating takeoff, not before
   
   # climb speed approximated as 1.3 x stall speed (same style as V_liftoff = 1.2 x stall)
   # true best climb speed (Vy) has no closed-form equation - only found by plotting in Week 3
   # this ratio is a standard conceptual-design-level approximation, consistent with
   # the rest of this function's fidelity (fixed fuel fractions, no full optimisation)
   V_climb = 1.3 * V_stall
   CL_climb = CL_required(W, rho, V_climb, S)
   CD_climb = drag_polar(cd0, k, CL_climb)
   D_climb = drag_force(rho, V_climb, S, CD_climb)
   RC = rate_of_climb(T, W, D_climb, V_climb)
   
   W = W - CFf * W_fuel

   # cruise needs BOTH W (before cruise) and W_after_cruise (after) simultaneously,
   # since the Breguet range equation itself is built from that ratio - W_after_cruise
   # is calculated here but W is only updated to it AFTER cruise_range has used both
   W_after_cruise =  W - (1-(TFf + CFf + DFf)) * W_fuel
   CL_opt = best_glide_CL(cd0, k)
   CD_opt = drag_polar(cd0, k, CL_opt)
   glide_V_opt = best_glide_speed(W, CL_opt, rho, S)
   V_max_range = max_range_speed(glide_V_opt)
   L_cruise = lift(rho, V_max_range, S, CL_opt)
   D_cruise = drag_force(rho, V_max_range, S, CD_opt)
   R_max = cruise_range(V_max_range, c, L_cruise, D_cruise, W, W_after_cruise, rho, S)

   W = W - (1-(TFf + CFf + DFf)) * W_fuel

   # descent uses the genuine best_glide_speed function (not an approximated ratio)
   # since this is the actual optimum glide condition validated back in Week 3 -
   # CL_opt is reused rather than recalculated, since best_glide_CL only depends
   # on cd0 and k, which never change
   V_descent = best_glide_speed(W, CL_opt, rho, S)
   CD_descent = drag_polar(cd0, k, CL_opt)
   D_descent = drag_force(rho, V_descent, S, CD_descent)
   RD = rate_of_decent(D_descent, 0, V_descent, W)
   
   W = W - DFf * W_fuel
   
   return s, RC, R_max, RD, W




