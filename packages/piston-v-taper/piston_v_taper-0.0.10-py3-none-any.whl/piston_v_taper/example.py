import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
import piston_v_taper.plotting_config

from piston_v_taper.model import PistonVTaper
from piston_v_taper import get_path

def example():
    test = PistonVTaper()
    data = pd.read_csv(get_path('./data/processed_test_data.csv'))
    x = data['x_t (mm)'].to_numpy()
    v = data['v_t (mm/s)'].to_numpy()
    t = data['time (s)'].to_numpy()

    f = np.zeros(t.shape)
    plastic_disp_rate = np.zeros(t.shape)
    plastic_disp = np.zeros(t.shape)
    contact = np.zeros(t.shape)
    plastic = np.zeros(t.shape)

    for i in range(1, t.size):
        dt = t[i] - t[i - 1]
        f[i], plastic_disp_rate[i], plastic_disp[i], cont = test.inc(x[i], v[i], dt, True)
        if cont == 1 or cont == 2:
            contact[i] = 1
        if cont == 2:
            plastic[i] = 1

    data.set_index('time (s)', inplace=True)
    model = pd.DataFrame({'plastic dissipation (mJ)': plastic_disp,
                          'contact': contact,
                          'elastoplastic': plastic,
                          'force (N)': f,
                          'plastic dissipation rate (mJ/s)': plastic_disp_rate},
                         index=t)

    plt.figure(figsize=(8, 10))
    cnt = 2
    ax1 = plt.subplot(int(f'711'))
    ax = ax1

    for column in ['x_t (mm)',
                   'v_t (mm/s)',
                   'plastic dissipation (mJ)',
                   'contact',
                   'elastoplastic',
                   'force (N)',
                   'plastic dissipation rate (mJ/s)',
                   ]:
        plt.plot(data.index, data[column], label='Data')
        if column in model.columns:
            plt.plot(model.index, model[column], label='Model')

        plt.ylabel('\n'.join(wrap(column, 20)))
        if cnt < 8:
            plt.setp(ax.get_xticklabels(), visible=False)
            place = int(f'71{cnt}')
            ax = plt.subplot(place, sharex=ax1)
        cnt += 1

    plt.xlabel('Time (s)')
    plt.tight_layout()
    plt.legend()
    plt.show()

example()
