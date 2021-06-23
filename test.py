import math
def idm_acceleration(v, h, lead_vel, rl_action):
        #print(veh_id, "chooses to be a leader with probability:",rl_action)
        if rl_action is None:
            return None
        a=1 # max acceleration, in m/s2 (default: 1)
        delta=4 # acceleration exponent (default: 4)
        s0=2 # linear jam distance, in m (default: 2)
        MAX_T=250#self.env_params.additional_params['max_headway']
        b=1.5 # comfortable deceleration, in m/s2 (default: 1.5)
        v0=30 # desirable velocity, in m/s (default: 30)
        T=MAX_T*rl_action # safe time headway, in s (default: 1)
        if T<=1:
            T=1
         # in order to deal with ZeroDivisionError
        if abs(h) < 1e-3:
            h = 1e-3
        temp=v * T + v * (v - lead_vel) /(2 * math.sqrt(a * b))
        print(temp)
        s_star = s0 + max(0, v * T + v * (v - lead_vel) /(2 * math.sqrt(a * b)))
        return a * (1 - (v / v0)**delta - (s_star / h)**2)
v=22
h=116
lead_vel=27
rl_action=-1
acceleartion=idm_acceleration(v, h, lead_vel, rl_action)
print(acceleartion)

