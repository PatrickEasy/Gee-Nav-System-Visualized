import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Constants
c = 300  # km/ms (speed of light scaled)
delay_slave = 0.1  # ms delay after receiving master pulse

# Plot bounds
xmin, xmax = -1000, 1000
ymin, ymax = -1000, 1000

# Random generator
np.random.seed()

def generate_stations(min_dist=150, count=3):
    stations = []
    while len(stations) < count:
        candidate = np.random.uniform(low=[xmin, ymin], high=[xmax, ymax])
        if all(np.linalg.norm(candidate - s) >= min_dist for s in stations):
            stations.append(candidate)
    return stations

# Generate station and aircraft positions
master, slave_a, slave_b = generate_stations()
margin = 100
aircraft = np.random.uniform(
    low=[xmin + margin, ymin + margin],
    high=[xmax - margin, ymax - margin]
)

# Time from master to slaves
t_master_to_slave_a = np.linalg.norm(slave_a - master) / c
t_master_to_slave_b = np.linalg.norm(slave_b - master) / c

# Slave emit times
t_slave_a_emit = t_master_to_slave_a + delay_slave
t_slave_b_emit = t_master_to_slave_b + delay_slave

# Distances from aircraft to each station
dist_master = np.linalg.norm(aircraft - master)
dist_slave_a = np.linalg.norm(aircraft - slave_a)
dist_slave_b = np.linalg.norm(aircraft - slave_b)

# Pulse arrival times at aircraft
t_master_arrival = dist_master / c
t_slave_a_arrival = t_slave_a_emit + dist_slave_a / c
t_slave_b_arrival = t_slave_b_emit + dist_slave_b / c

# Set up plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')
ax.set_title("GEE Navigation – Accurate Pulse Timing")
ax.set_xlabel("km")
ax.set_ylabel("km")
ax.grid(True)

# Plot fixed points
master_point, = ax.plot(*master, 'ro', label="Master")
slave_a_point, = ax.plot(*slave_a, 'go', label="Slave A")
slave_b_point, = ax.plot(*slave_b, 'bo', label="Slave B")
aircraft_dot, = ax.plot([], [], 'kx', label="Aircraft")
aircraft_label = ax.text(aircraft[0] + 20, aircraft[1] + 20, "", fontsize=9)
slave_a_label = ax.text(slave_a[0] + 20, slave_a[1] + 20, "", fontsize=9, color='green')
slave_b_label = ax.text(slave_b[0] + 20, slave_b[1] + 20, "", fontsize=9, color='blue')

# Expanding pulse circles
master_circle = plt.Circle(master, 0, color='r', fill=False)
slave_a_circle = plt.Circle(slave_a, 0, color='g', fill=False, linestyle='--')
slave_b_circle = plt.Circle(slave_b, 0, color='b', fill=False, linestyle='--')

# Back-calculated circles from aircraft
master_back_circle = plt.Circle(aircraft, 0, color='r', linestyle=':', fill=False)
slave_a_back_circle = plt.Circle(aircraft, 0, color='g', linestyle=':', fill=False)
slave_b_back_circle = plt.Circle(aircraft, 0, color='b', linestyle=':', fill=False)

# Triangulation circles from station (faded)
master_tri_circle = plt.Circle(master, 0, color='r', linestyle=':', fill=False, alpha=0.2)
slave_a_tri_circle = plt.Circle(slave_a, 0, color='g', linestyle=':', fill=False, alpha=0.2)
slave_b_tri_circle = plt.Circle(slave_b, 0, color='b', linestyle=':', fill=False, alpha=0.2)

# Add all circles to plot
for circle in [
    master_circle, slave_a_circle, slave_b_circle,
    master_back_circle, slave_a_back_circle, slave_b_back_circle,
    master_tri_circle, slave_a_tri_circle, slave_b_tri_circle
]:
    ax.add_patch(circle)

# Legend
legend_elements = [
    Line2D([0], [0], color='r', lw=2, label='Pulse from Master'),
    Line2D([0], [0], color='g', lw=2, linestyle='--', label='Pulse from Slave A'),
    Line2D([0], [0], color='b', lw=2, linestyle='--', label='Pulse from Slave B'),
    Line2D([0], [0], color='k', marker='x', linestyle='None', label='Aircraft'),
    Patch(edgecolor='gray', facecolor='none', linestyle=':', label='Dotted = distance from aircraft'),
    Patch(edgecolor='gray', facecolor='none', linestyle=':', alpha=0.2, label='Faded = triangulation range'),
]
ax.legend(handles=legend_elements, loc='upper right')

# Animation function
def animate(frame):
    t = frame * 0.1  # time in ms

    # Expanding pulses
    master_circle.set_radius(c * t)

    if t >= t_slave_a_emit:
        slave_a_circle.set_radius(c * (t - t_slave_a_emit))
    else:
        slave_a_circle.set_radius(0)

    if t >= t_slave_b_emit:
        slave_b_circle.set_radius(c * (t - t_slave_b_emit))
    else:
        slave_b_circle.set_radius(0)

    aircraft_dot.set_data([aircraft[0]], [aircraft[1]])

    label_lines = []

    # Aircraft detects master pulse
    if t >= t_master_arrival:
        master_back_circle.set_radius(dist_master)
        master_tri_circle.set_radius(dist_master)
        label_lines.append(f"Master Δt: {t_master_arrival:.2f} ms ∴ {c*t_master_arrival:.2f} km away")
    else:
        master_back_circle.set_radius(0)
        master_tri_circle.set_radius(0)

    # Aircraft detects Slave A pulse
    if t >= t_slave_a_arrival:
        slave_a_back_circle.set_radius(dist_slave_a)
        slave_a_tri_circle.set_radius(dist_slave_a)
        label_lines.append(f"Slave A Δt: {(t_slave_a_arrival - t_slave_a_emit):.2f} ms ∴ {c*(t_slave_a_arrival - t_slave_a_emit):.2f} km away")
    else:
        slave_a_back_circle.set_radius(0)
        slave_a_tri_circle.set_radius(0)

    # Aircraft detects Slave B pulse
    if t >= t_slave_b_arrival:
        slave_b_back_circle.set_radius(dist_slave_b)
        slave_b_tri_circle.set_radius(dist_slave_b)
        label_lines.append(f"Slave B Δt: {t_slave_b_arrival - t_slave_b_emit:.2f} ms ∴ {c*(t_slave_b_arrival - t_slave_b_emit):.2f} km away")
    else:
        slave_b_back_circle.set_radius(0)
        slave_b_tri_circle.set_radius(0)

    # Annotate when master pulse is received by slaves
    slave_a_label.set_text("Recv Master" if t >= t_master_to_slave_a else "")
    slave_b_label.set_text("Recv Master" if t >= t_master_to_slave_b else "")

    if label_lines:
        label_lines.append("(dotted = from aircraft, faded = from station)")

    aircraft_label.set_text("\n".join(label_lines))

    return (
        master_circle, slave_a_circle, slave_b_circle,
        master_back_circle, slave_a_back_circle, slave_b_back_circle,
        master_tri_circle, slave_a_tri_circle, slave_b_tri_circle,
        aircraft_dot, aircraft_label, slave_a_label, slave_b_label
    )

# Run animation
ani = animation.FuncAnimation(fig, animate, frames=150, interval=50, blit=True)
plt.show()

# Save
# Note: Saving as GIF can be slow and large; commented out for by default
# Uncomment the next line to save the animation as a GIF
#ani.save("gee_animation.gif", writer='pillow', fps=20)

