import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Constants
c = 300       # km/ms (speed of light scaled)
delay_slave = 0.1  # ms delay for slave station to respond

# Plot bounds
xmin, xmax = -1000, 1000
ymin, ymax = -1000, 1000

# Station placement function
def generate_stations(min_dist=150, count=3):
    stations = []
    while len(stations) < count:
        candidate = np.random.uniform(low=[xmin, ymin], high=[xmax, ymax])
        if all(np.linalg.norm(candidate - s) >= min_dist for s in stations):
            stations.append(candidate)
    return stations

# Generate positions
np.random.seed()
master, slave_a, slave_b = generate_stations()
margin = 50
aircraft = np.random.uniform(low=[xmin + margin, ymin + margin], high=[xmax - margin, ymax - margin])

# Signal travel times
t_master_to_slave_a = np.linalg.norm(slave_a - master) / c
t_master_to_slave_b = np.linalg.norm(slave_b - master) / c
t_slave_a_emit = t_master_to_slave_a + delay_slave
t_slave_b_emit = t_master_to_slave_b + delay_slave

# Aircraft distances
dist_master = np.linalg.norm(aircraft - master)
dist_slave_a = np.linalg.norm(aircraft - slave_a)
dist_slave_b = np.linalg.norm(aircraft - slave_b)

# Arrival times at aircraft
t_master_arrival = dist_master / c
t_slave_a_arrival = t_slave_a_emit + dist_slave_a / c
t_slave_b_arrival = t_slave_b_emit + dist_slave_b / c

# Setup plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')
ax.set_title("GEE Navigation – Static Visualization")
ax.set_xlabel("km")
ax.set_ylabel("km")
ax.grid(True)

# Plot points
ax.plot(*master, 'ro', label="Master")
ax.plot(*slave_a, 'go', label="Slave A")
ax.plot(*slave_b, 'bo', label="Slave B")
ax.plot(*aircraft, 'kx', label="Aircraft")

# Aircraft label
label_lines = [
    f"Master Δt: {t_master_arrival:.2f} ms",
    f"Slave A Δt: {t_slave_a_arrival - t_slave_a_emit:.2f} ms",
    f"Slave B Δt: {t_slave_b_arrival - t_slave_b_emit:.2f} ms",
    "(dotted = from aircraft, faded = from station)"
]
ax.text(aircraft[0] + 20, aircraft[1] + 20, "\n".join(label_lines), fontsize=9)

# Back-calculated circles (from aircraft)
ax.add_patch(plt.Circle(aircraft, dist_master, color='r', fill=False, linestyle=':', label='Back from Aircraft'))
ax.add_patch(plt.Circle(aircraft, dist_slave_a, color='g', fill=False, linestyle=':'))
ax.add_patch(plt.Circle(aircraft, dist_slave_b, color='b', fill=False, linestyle=':'))

# Triangulation circles (from stations)
ax.add_patch(plt.Circle(master, dist_master, color='r', fill=False, linestyle=':', alpha=0.2))
ax.add_patch(plt.Circle(slave_a, dist_slave_a, color='g', fill=False, linestyle=':', alpha=0.2))
ax.add_patch(plt.Circle(slave_b, dist_slave_b, color='b', fill=False, linestyle=':', alpha=0.2))

# Legend
legend_elements = [
    Line2D([0], [0], color='r', lw=2, label='Master Station'),
    Line2D([0], [0], color='g', lw=2, label='Slave A'),
    Line2D([0], [0], color='b', lw=2, label='Slave B'),
    Line2D([0], [0], color='k', marker='x', linestyle='None', label='Aircraft'),
    Patch(edgecolor='gray', facecolor='none', linestyle=':', label='Dotted = distance from aircraft'),
    Patch(edgecolor='gray', facecolor='none', linestyle=':', alpha=0.2, label='Faded = triangulation range')
]
ax.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.show()
