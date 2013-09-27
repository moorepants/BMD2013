#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script identifies a selected set of unknown parameters of the speed
dependent canonical formulation of the Whipple model given various sets of
recorded data."""

# standard library
import os
import cPickle

# external
from canonicalbicycleid import canonical_bicycle_id as cbi

# Get the M, C1, K0, K2, and H matrices for the riders.
riders = ['Charlie', 'Jason', 'Luke']
canon = cbi.load_benchmark_canon(riders)
H = cbi.lateral_force_contribution(riders)

# Load in all of the runs that meet the query and that don't have errors.
environments = ['Horse Treadmill', 'Pavillion Floor']
maneuvers = ['Balance',
             'Track Straight Line',
             'Balance With Disturbance',
             'Track Straight Line With Disturbance']
runs = cbi.select_runs(riders, maneuvers, environments)
trials, errors = cbi.load_trials(runs, H)
goodRuns = list(set(runs).difference(errors))

# Pick the free parameters in the canonical model, i.e. the ones we want to
# identify.
roll_parameters = ['Mpd', 'C1pd', 'K0pd']
steer_parameters = ['Mdd', 'C1dp', 'C1dd', 'K0dd', 'K2dd', 'HdF']

# These are the 12 models that we are interested in.
combinations = [(x, y) for x in (riders + ['All'])
                for y in (environments + ['All'])]

id_matrices = {}
covariance_matrices = {}

for combo in combinations:

    print('Computing the estimate for riders: ' +
        '{} and environments: {}'.format(combo[0], combo[1]))

    if combo[0] == 'All':
        riders = ['Charlie', 'Jason', 'Luke']
    else:
        riders = [combo[0]]
    if combo[1] == 'All':
        environments = ['Horse Treadmill', 'Pavillion Floor']
    else:
        environments = [combo[1]]

    # Select the subset of runs and remove any that have errors.
    runs = cbi.select_runs(riders, maneuvers, environments)
    runs = list(set(runs).difference(errors))

    # Compute the mean first principles model with respect to the subset of
    # riders. This returns a tuple: (M, C1, K0, K2, H)
    means = cbi.mean_canon(riders, canon, H)

    # Solve the linear least squares: roll equation first, steer equation
    # second with the matrix symmetry enforced from the roll results.
    id_matrix, roll_covariance, steer_covariance = \
        cbi.enforce_symmetry(runs, trials, roll_parameters,
                            steer_parameters, *means)

    id_matrices[combo[0][0] + '-' + combo[1][0]] = id_matrix
    covariance_matrices[combo[0][0] + '-' + combo[1][0]] = (roll_covariance,
                                                            steer_covariance)

    print('Done.')

# Store the identified models, the parameter covariances, and the list of
# good runs.
results_directory = '../data'
if not os.path.exists(results_directory):
    os.makedirs(results_directory)

with open(os.path.join(results_directory, 'good-runs.p'), 'w') as f:
    cPickle.dump(goodRuns, f)

with open(os.path.join(results_directory, 'id-matrices.p'), 'w') as f:
    cPickle.dump(id_matrices, f)

with open(os.path.join(results_directory, 'covariance-matrices.p'), 'w') as f:
    cPickle.dump(covariance_matrices, f)
