#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script computes the errors and associated statistics between the
measured steer tube torque and the compensated steer tube torque for a set
of runs and generates some graphs."""

# standard library
import os
from ConfigParser import SafeConfigParser

# external libraries
import numpy as np
import pandas
import matplotlib.pyplot as plt
import bicycledataprocessor as bdp
import dtk

# plot settings
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('axes', titlesize=10, labelsize=8)
column_width_in_pt = 424.58624
inches_per_pt = 1.0 / 72.27
column_width_in_inches = column_width_in_pt * inches_per_pt

try:
    filename = '../data/steer-torque-data.h5'
    with open(filename, 'r') as f:
        time_series = pandas.read_hdf(filename, 'time_series')
        stats = pandas.read_hdf(filename, 'stats')
except IOError:
    # get the paths to the data files
    path_to_config = os.path.join(os.getcwd(), 'bicycle-data.cfg')
    config = SafeConfigParser()
    config.read(path_to_config)
    PATH_TO_BICYCLE_PARAMETER_DATA = \
        config.get('data', 'PATH_TO_BICYCLE_PARAMETER_DATA')
    PATH_TO_INSTRUMENTED_BICYCLE_DATA = \
        config.get('data', 'PATH_TO_INSTRUMENTED_BICYCLE_DATA')

    # select some runs
    riders = ['Charlie', 'Jason', 'Luke']
    maneuvers = ['Balance', 'Balance With Disturbance',
                 'Track Straight Line', 'Track Straight Line With Disturbance']
    environments = ['Horse Treadmill', 'Pavillion Floor']
    data_set = bdp.DataSet(pathToDatabase=PATH_TO_INSTRUMENTED_BICYCLE_DATA)
    runs = data_set.select_runs(riders, maneuvers, environments)

    # initialize the data structures
    time_series = {}
    stats = {'Root Mean Square of the Error': [],
             'Coefficient of Determination': [],
             'Maximum Error': []}
    max_num_samples = 0

    for run in runs:

        ts = {}
        ts['Steer Tube Torque'] = None
        ts['Compensated Steer Torque'] = None
        ts['Error'] = None

        try:
            trial = bdp.Run(run, data_set, filterFreq=15.,
                            pathToParameterData=PATH_TO_BICYCLE_PARAMETER_DATA,
                            forceRecalc=True)
        except bdp.bdpexceptions.TimeShiftError:

            for k in stats.keys():
                stats[k].append(np.nan)

            for k in ts.keys():
                ts[k] = [np.nan, np.nan]

        except IndexError:

            for k in stats.keys():
                stats[k].append(np.nan)

            for k in ts.keys():
                ts[k] = [np.nan, np.nan]

        else:
            measured_torque = \
                trial.truncatedSignals['SteerTubeTorque'].convert_units('newton*meter')
            compensated_torque = trial.computedSignals['SteerTorque']
            error = compensated_torque - measured_torque
            rms = np.sqrt((error ** 2).mean())
            r_squared = \
                dtk.process.coefficient_of_determination(measured_torque,
                                                         compensated_torque)

            ts['Steer Tube Torque'] = measured_torque
            ts['Compensated Steer Torque'] = compensated_torque
            ts['Error'] = error

            if len(measured_torque) > max_num_samples:
                max_num_samples = len(measured_torque)

            stats['Root Mean Square of the Error'].append(rms)
            stats['Coefficient of Determination'].append(r_squared)
            stats['Maximum Error'].append(abs(error).max())

        time_series[run] = pandas.DataFrame(ts)

    time = dtk.process.time_vector(max_num_samples, measured_torque.sampleRate)
    time_series = pandas.Panel(time_series, items=runs, major_axis=time)
    stats = pandas.DataFrame(stats, index=runs)

    results_directory = '../data'
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    time_series.to_hdf('../data/steer-torque-data.h5', 'time_series')
    stats.to_hdf('../data/steer-torque-data.h5', 'stats')


def remove_outliers(num_sigma, data_frame, column_name):
    """Returns a data frame with the rows removed that have values outside
    the num_sigma * sigma bound for the given column."""
    mean = data_frame[column_name].mean()
    std = data_frame[column_name].std()
    mean_subtracted = data_frame[column_name] - mean
    return data_frame[mean_subtracted.abs() < num_sigma * std]

# remove the 2 * sigma outliers
stats = remove_outliers(2, stats, 'Root Mean Square of the Error')
stats = remove_outliers(2, stats, 'Coefficient of Determination')
stats = remove_outliers(2, stats, 'Maximum Error')
stats['Coefficient of Determination'] *= 100.0

# make a histogram of the results
axes = stats.hist(bins=20, layout=(1, 3),
                  figsize=(column_width_in_inches, 2.0),
                  xlabelsize=8,
                  ylabelsize=8)
axes[0, 2].set_title('RMS of the Error')

axes[0, 0].set_xlabel(r'\%')
axes[0, 1].set_xlabel('Nm')
axes[0, 2].set_xlabel('Nm')

plt.tight_layout()

fig = plt.gcf()
fig.savefig('../figures/error-stats.pdf')
fig.savefig('../figures/error-stats.png', dpi=300)

# TODO : should i compute an RMS for the error for all data at once?
# Should I compute rms based on the type of rider, manuever, and environment?
