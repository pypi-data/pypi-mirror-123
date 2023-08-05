import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
import piston_v_taper.plotting_config

import seaborn as sns

from piston_v_taper.model import PistonVTaper
from piston_v_taper import get_path


def example():
    # Step 1: Create a PistonVTaper object
    pist_v_taper = PistonVTaper()

    # Step 2: Create some artificial loading data
    t = np.linspace(0, 20, 10000)  # time in seconds
    x = np.sin(t)  # Position of front of piston past front of taper in mm
    v = np.gradient(x, t)  # Velocity of piston
    f = np.zeros(t.size)  # Force applied to the piston from the taper (to be determined)

    # Step 3: Loop through the loading data to determine the forces
    for i in range(1, t.size):
        dt = t[i] - t[i-1]
        # .inc (short for increment) method returns the force and determines the plastic dissipation of the cap.
        # The plastic dissipation is stored inside the PistonVTaper object
        f[i] = pist_v_taper.inc(x, v, dt)

    # Step 4: Plot the results
    sns.lineplot(x=x, y=f, hue=t)
    plt.figure()
    sns.lineplot(x=t, y=f, hue=x)
    plt.show()