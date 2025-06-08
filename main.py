import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define station coordinates (in km)
master = np.array([0, 0])
slave_a = np.array([100, 0])
slave_b = np.array([50, 86.6])  # forms an equilateral triangle

# Time delay simulation (in microseconds)
speed_of_radio = 300_000  # km/s

# Aircraft position
aircraft = np.array([70, 40])

# Function to calculate distance difference
def time_diff(p1, p2, p3):
    return (np.linalg.norm(p1 - p2) - np.linalg.norm(p1 - p3))

# Calculate time difference between slave and master pulses
td_a = time_diff(aircraft, master, slave_a)
td_b = time_diff(aircraft, master, slave_b)

# Create a grid for plotting
x = np.linspace(-50, 150, 400)
y = np.linspace(-50, 150, 400)
X, Y = np.meshgrid(x, y)

# Calculate hyperbolas
def hyperbola(X, Y, A, B, delay_diff):
    dist_a = np.sqrt((X - A[0])**2 + (Y - A[1])**2)
    dist_b = np.sqrt((X - B[0])**2 + (Y - B[1])**2)
    return dist_a - dist_b - delay_diff

Z1 = hyperbola(X, Y, slave_a, master, td_a)
Z2 = hyperbola(X, Y, slave_b, master, td_b)

# Plotting setup
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-50, 150)
ax.set_ylim(-50, 150)
ax.set_title("GEE Navigation System Demonstration")
ax.set_xlabel("km")
ax.set_ylabel("km")
ax.grid(True)

# Plot stations
ax.plot(*master, 'ro', label="Master Station")
ax.plot(*slave_a, 'go', label="Slave A")
ax.plot(*slave_b, 'bo', label="Slave B")
ax.plot(*aircraft, 'kx', label="Aircraft (Unknown Pos)")

# Plot hyperbolic lines of position
contour1 = ax.contour(X, Y, Z1, levels=[0], colors='g', linestyles='--')
contour2 = ax.contour(X, Y, Z2, levels=[0], colors='b', linestyles='--')

ax.legend()

plt.show()
