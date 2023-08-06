
This is a library containing a pretrained machine learning model for predicting 
the force applied to a piston by a tapered transition-piece at the end of a pump-tube
for a two-stage gas gun.

Provided that a given machine has an up-to-date instillation of `pip`, the
library can be installed using

`pip install piston-v-taper`

If the library is updated, the update of the library can be installed using

`pip install -U piston-v-taper`

## Usage
The library provides a `PistonVTaper` class which can be imported as follows:

`from piston_v_taper.model import PistonVTaper`

After importing the class, a `PistonVTaper` object can be instantiated as follows:

`my_piston_v_taper_object = PistonVTaper()`

Here, the variable `my_piston_v_taper_object` can be named as the user desires.
The force applied to the piston during a given time-step `f` can be determined by calling the 
`PistonVTaper.inc()` method and parsing in the position of the piston 
past the start of the taper `x` in **mm**, the velocity of the piston `v` in **mm/s**,
and the size of the time increment `dt` in **s**; that is:

`f = my_piston_v_taper_object.inc(x, v, dt)`

Note that the `.inc` method predicts whether the piston is in contact with
the transition piece and updates the degree of plastic deformation that has occurred
in the end-cap. As such, **the `.inc` method should only be called once per time step**, 
otherwise the degree of plastic deformation of the end-cap will be increased multiple times
in a single time step.

### Example
Here, we illustrate the usage of the `PistonVTaper` class with an example script shown below.
The example script makes use of some artificial data for time, and position and velocity of the piston. 
In a 1D computational code, the position and velocity of the piston the start of a given time step is typically known.
```import pandas as pd
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
x = 10 * (1 + np.sin(np.pi * HALF_PERIODS * t / t[-1] - np.pi / 2)) * (OFF_SET + \
    t * (1 - OFF_SET)/t[-1]) / 2
v = np.gradient(x, t)  # Velocity of piston
f = np.zeros(t.size)  # Force applied to the piston from the taper (to be determined)

# Step 3: Loop through the loading data to determine the forces
for i in range(1, t.size):
    dt = t[i] - t[i - 1]
    # .inc (short for increment) method returns the force and determines 
    # the plastic dissipation of the cap.
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
sns.scatterplot(data=results, x='x (mm)', y='F (N)', hue='t (s)', palette='viridis', 
                linewidth=0, hue_order=get_hue_order(results['t (s)'], N_HUES), legend='brief')
plt.tight_layout()

plt.figure()
sns.scatterplot(data=results, x='t (s)', y='F (N)', hue='x (mm)', palette='viridis', 
                linewidth=0, hue_order=get_hue_order(results['x (mm)'], N_HUES), legend='brief')
plt.tight_layout()

plt.figure()
sns.scatterplot(data=results, x='t (s)', y='x (mm)', hue='F (N)', palette='viridis', 
                linewidth=0, hue_order=get_hue_order(results['F (N)'], N_HUES), legend='brief')
plt.tight_layout()

plt.show()
```
The resulting output of this script should be the figures
shown below. Hopefully the interpretation of these figures 
is somewhat intuitive. One particularly attractive feature of the 
model is that the point at which the cap makes contact
with the end piece increasingly becomes further and further
away due to plastic deformation, which is clear from the 
first figure.

[comment]: <> (![image]&#40;./images/x-vs-t.png&#41;)

[comment]: <> (![image]&#40;./images/f-vs-t.png&#41;)

[comment]: <> (![image]&#40;./images/f-vs-x.png&#41;)
![image](https://raw.githubusercontent.com/BenAlheit/piston-vs-taper/1cf2f27ef7673319e146ec86da3ed88088b56666/computation/piston_v_taper_ml/images/x-vs-t.png)
![image](https://raw.githubusercontent.com/BenAlheit/piston-vs-taper/1cf2f27ef7673319e146ec86da3ed88088b56666/computation/piston_v_taper_ml/images/f-vs-t.png)
![image](https://raw.githubusercontent.com/BenAlheit/piston-vs-taper/1cf2f27ef7673319e146ec86da3ed88088b56666/computation/piston_v_taper_ml/images/f-vs-x.png)


## Improvements and future work

It is clear that the machine learning model can be improved upon.
In particular, some non-physical behaviour is observed: 
* There are occasionally negative forces. It is possible that these could arise
from the end-cap being wedged in the transition piece due to friction. However, since these
negative forces are not observed in the data used to train the model (see below) it is apparent that 
this is an undesirable artifact of the machine learning model.
* The force curves contain significant discontinuous jumps. 
  These are somewhat reasonable given the discontinuous nature of the
  underlying contact problem. However, again, this is slightly inconsistent
  with the data (see below).

I (Ben Alheit) have some ideas on how this may be improved, but I do not have the time to 
implement them. If someone is interested in contributing in this regard, please feel free
to reach out using the email address provided. Broadly speaking these include:

* Improving the machine learning model.
* Obtaining more data from finite element simulations to train the machine learning model on (see below).

## Some notes of the development of the model
To train the machine learning model data is required. This is obtained
by means of finite element simulations, which are outlined briefly in the subsection below.
With the data in hand, a machine learning model was trained to produce the
required force given the known input information. This is outlined briefly in the
subsection that follows the Finite element simulation subsection.

For a more detailed description of the development see 
[this report on model creation](https://github.com/BenAlheit/piston-vs-taper/blob/master/report/piston-vs-taper.pdf) (currently under development).

### Finite element simulation
A finite element analysis simulation is used to determine the force
on the piston due to contact with the transition piece.
Material parameters for each material are take from the literature
and axisymmetric elements are used. Increasing cyclical displacements are
applied to the back of the back of the piston forcing the 
end-cap into the transition piece increasing degrees. An animation of the results
is presented below. Note the increasing plastic deformation of the end-cap.
![Alt Text](https://raw.githubusercontent.com/BenAlheit/piston-vs-taper/master/computation/piston_v_taper_ml/images/loading-animation.gif)
### Machine learning model
[comment]: #(TODO)
TODO

Comparison of test data and machine learning model:

![image](https://raw.githubusercontent.com/BenAlheit/piston-vs-taper/1cf2f27ef7673319e146ec86da3ed88088b56666/computation/piston_v_taper_ml/images/comparison-with-data.png)


Zooming in on an arbitrarily chosen contact cycle:

[comment]: <> (![image]&#40;./images/comparison-with-data-zoom.png&#41;)
![](https://raw.githubusercontent.com/BenAlheit/piston-vs-taper/1cf2f27ef7673319e146ec86da3ed88088b56666/computation/piston_v_taper_ml/images/comparison-with-data-zoom.png)

[ this report on model creation.]: https://github.com/BenAlheit/piston-vs-taper/blob/master/report/piston-vs-taper.pdf