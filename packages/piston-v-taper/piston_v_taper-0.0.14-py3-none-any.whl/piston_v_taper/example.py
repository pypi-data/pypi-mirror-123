import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import piston_v_taper.plotting_config
import seaborn as sns

from piston_v_taper.model import PistonVTaper


N_HUES = 10
HALF_PERIODS = 12
OFF_SET = 0.3


def get_hue_order(val, n_hues):
    return np.linspace(np.min(val), np.max(val), n_hues)


# Step 1: Create a PistonVTaper object
pist_v_taper = PistonVTaper()

# Step 2: Create some artificial loading data
t = np.linspace(0, 0.5, 10000)
x = 10 * (1 + np.sin(np.pi * HALF_PERIODS * t / t[-1] - np.pi / 2)) * (OFF_SET + t * (1 - OFF_SET)/t[-1]) / 2
v = np.gradient(x, t)  # Velocity of piston
f = np.zeros(t.size)  # Force applied to the piston from the taper (to be determined)

# Step 3: Loop through the loading data to determine the forces
for i in range(1, t.size):
    dt = t[i] - t[i - 1]
    # .inc (short for increment) method returns the force and determines the plastic dissipation of the cap.
    # The plastic dissipation is stored inside the PistonVTaper object
    f[i] = pist_v_taper.inc(x[i], v[i], dt)

# Step 4: Construct data frame for plotting
results = pd.DataFrame(data={
    't (s)': t,
    'x (mm)': x,
    'v (mm/s)': v,
    'F (N)': f,
})

# Step 5: Plot the results
sns.scatterplot(data=results, x='x (mm)', y='F (N)', hue='t (s)', palette='viridis', linewidth=0,
                hue_order=get_hue_order(results['t (s)'], N_HUES), legend='brief')
plt.tight_layout()

plt.figure()
sns.scatterplot(data=results, x='t (s)', y='F (N)', hue='x (mm)', palette='viridis', linewidth=0,
                hue_order=get_hue_order(results['x (mm)'], N_HUES), legend='brief')
plt.tight_layout()

plt.figure()
sns.scatterplot(data=results, x='t (s)', y='x (mm)', hue='F (N)', palette='viridis', linewidth=0,
                hue_order=get_hue_order(results['F (N)'], N_HUES), legend='brief')
plt.tight_layout()

plt.show()



