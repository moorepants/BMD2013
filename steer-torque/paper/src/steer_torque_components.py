#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script generates a plot showing the contributions to torque due to
friction and inertial effects."""

# standard library
import os
from ConfigParser import SafeConfigParser

import bicycledataprocessor as bdp
import matplotlib.pyplot as plt

# get the paths to the data files
path_to_config = os.path.join(os.getcwd(), 'bicycle-data.cfg')
config = SafeConfigParser()
config.read(path_to_config)
PATH_TO_BICYCLE_PARAMETER_DATA = \
    config.get('data', 'PATH_TO_BICYCLE_PARAMETER_DATA')
PATH_TO_INSTRUMENTED_BICYCLE_DATA = \
    config.get('data', 'PATH_TO_INSTRUMENTED_BICYCLE_DATA')

dataset = bdp.DataSet(pathToDatabase=PATH_TO_INSTRUMENTED_BICYCLE_DATA)
dataset.open()

trial = bdp.Run('00700', dataset, PATH_TO_BICYCLE_PARAMETER_DATA,
                forceRecalc=True)

dataset.close()

column_width_in_pt = 424.58624
inches_per_pt = 1.0 / 72.27
column_width_in_inches = column_width_in_pt * inches_per_pt
fig_width = column_width_in_inches
fig_height = 4.5
params = {'backend': 'ps',
          'axes.labelsize': 10,
          'text.fontsize': 10,
          'legend.fontsize': 6,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          'figure.figsize': [fig_width, fig_height],
          'figure.dpi': 200,
          'figure.subplot.left': 0.1,
          'figure.subplot.bottom': 0.1,
          'font.family': 'serif'}
plt.rcParams.update(params)

fig = trial.compute_steer_torque(plot=True)

fig.savefig('../figures/steer-torque-components.pdf')
fig.savefig('../figures/steer-torque-components.png', dpi=300)
