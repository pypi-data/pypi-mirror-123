from openspace.propagators import ClohessyWiltshireModel, TwoBodyModel
from openspace.math.linear_algebra import Vector
from openspace.math.measurements import Epoch
from openspace.math.coordinates import j2000_to_hill, vector_to_coes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

def test():
    rel_mod = ClohessyWiltshireModel([0, -200000, 0, 1, 0, 1], 42164000)
    x, y, z = [], [], []
    for t in range(0, 86400*2, 300):
        state = rel_mod.solve_next_state(t)
        burn_mod = ClohessyWiltshireModel(state, 42164000)
        for t2 in range(300, 86400, 300):
            burn = burn_mod.solve_waypoint_burn(t2, Vector([0, 0, 0]))
            x.append(t)
            y.append(t2)
            #burn = Vector(burn[0:2])
            if burn.magnitude() < 50:
                z.append(burn.magnitude())
            else:
                z.append(50)

    data = pd.DataFrame(data={'x':x, 'y':y, 'z':z})
    data = data.pivot(index='y', columns='x', values='z')
    ax = sns.heatmap(data, cbar_kws={'label': 'Burn Magnitude (m/s)'})
    ax.invert_yaxis()
    ax.set_xlabel("Time Past Initial Epoch (s)")
    ax.set_ylabel("Time to Intercept (s)")
    ax.set_title('Threat Delta-V')
    plt.show()

def run():
    r = Vector([42164000, 0, 0])
    v = Vector([0, 3070, 0])
    a, e, i, ta, aop, raan = vector_to_coes(r, v)
    now = time.time()
    epoch1 = Epoch.from_timestamp(now)
    epoch2 = Epoch.from_timestamp(now + 3)

    tbm1 = TwoBodyModel(r, v, epoch1)
    tbm2 = TwoBodyModel(r, v, epoch2)

    r2, v2 = tbm2.get_state_at_epoch(epoch1)
    r1 = j2000_to_hill(raan, aop, i, r)
    v1 = j2000_to_hill(raan, aop, i, v)
    r2 = j2000_to_hill(raan, aop, i, r2)
    v2 = j2000_to_hill(raan, aop, i, v2)
    rel_pos = r1.minus(r2)
    rel_vel = v1.minus(v2)
    rel_state = Vector([
        rel_pos.get_element(0),
        rel_pos.get_element(1),
        rel_pos.get_element(2),
        rel_vel.get_element(0),
        rel_vel.get_element(1),
        rel_vel.get_element(2)
    ])
    print(rel_vel)
    rel_mod = ClohessyWiltshireModel(rel_state, a)

    x,y,z = rel_mod.get_positions_over_interval(0, 86400, 600)
    plt.plot(y, x)
    plt.show()
