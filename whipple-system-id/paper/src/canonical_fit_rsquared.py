#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file builds a table of coefficients of deterimation (R^2) for each
identified model and each set of runs."""

# standard library
import os
import cPickle

# external
import pandas
from canonicalbicycleid import canonical_bicycle_id as cbi

riders = ['Charlie', 'Jason', 'Luke']
maneuvers = ['Balance',
             'Track Straight Line',
             'Balance With Disturbance',
             'Track Straight Line With Disturbance']
environments = ['Horse Treadmill', 'Pavillion Floor']

# Get the M, C1, K0, K2, and H matrices for the riders.
canon = cbi.load_benchmark_canon(riders)
H = cbi.lateral_force_contribution(riders)

# Pick the free parameters in the canonical model, i.e. the ones that were
# identified.
roll_parameters = ['Mpd', 'C1pd', 'K0pd']
steer_parameters = ['Mdd', 'C1dp', 'C1dd', 'K0dd', 'K2dd', 'HdF']

# Load in precomputed results.
results_directory = '../data'

with open(os.path.join(results_directory, 'good-runs.p'), 'r') as f:
    good_runs = cPickle.load(f)

with open(os.path.join(results_directory, 'id-matrices.p'), 'r') as f:
    id_matrices = cPickle.load(f)

# TODO : Add the canonical matrices for the Whipple and Arm model.
id_matrices['Whipple'] = None # will be filled in the loop

trials, errors = cbi.load_trials(good_runs, H)

# These are the A and b's for each trial (for Ax=b)
print('Generating the A matrices and b vectors for each run.')
roll_a_dict, roll_b_dict = cbi.lstsq_A_B(trials, roll_parameters)
steer_a_dict, steer_b_dict = cbi.lstsq_A_B(trials, steer_parameters)
print('Done.')

# These are the 12 models that we are interested in.
combinations_of_queries = [(x, y) for x in ([[r] for r in riders] + [riders])
                           for y in ([[e] for e in environments] + [environments])]

data_set_names = []
for queries in combinations_of_queries:

    rider_query = queries[0]
    env_query = queries[1]

    if len(rider_query) > 1:
        first_letter_of_rider = 'A'
    else:
        first_letter_of_rider = rider_query[0][0]

    if len(env_query) > 1:
        first_letter_of_env = 'A'
    else:
        first_letter_of_env = env_query[0][0]

    data_set_names.append(first_letter_of_rider + '-' +
                          first_letter_of_env)

# Columns: Identified Model
# Rows: Data Set
roll_r_squared = {}
steer_r_squared = {}

for model_name, canonical_matrices in id_matrices.items():

    roll_r_squared[model_name] = []
    steer_r_squared[model_name] = []

    for i, queries in enumerate(combinations_of_queries):

        print('Computing the coefficient of determination for data ' +
              'set {} with model {}.'.format(data_set_names[i], model_name))

        if model_name == 'Whipple':
            canonical_matrices = cbi.mean_canon(queries[0], canon, H)
        elif model_name == 'Arm':
            pass
            #A, B, speeds = cbi.mean_arm([rider])
            #M = np.linalg.inv(B[round(v * 10)][2:, [0, 1]])
            #C = -np.dot(M, A[round(v * 10)][2:, [2, 3]])
            #K = -np.dot(M, A[round(v * 10)][2:, [0, 1]])
            # I need some way to compute the A and b matrices using just the
            # M, C, and K matrices.

        # Select the subset of runs and remove any that have errors.
        run_numbers = cbi.select_runs(queries[0], maneuvers, queries[1])
        run_numbers = list(set(run_numbers).intersection(good_runs))
        print('Number of runs: {}'.format(len(run_numbers)))

        roll_r_squared[model_name].append(
            cbi.validation_r_squared(run_numbers, roll_a_dict, roll_b_dict,
                                     roll_parameters, canonical_matrices))

        steer_r_squared[model_name].append(
            cbi.validation_r_squared(run_numbers, steer_a_dict,
                                     steer_b_dict, steer_parameters,
                                     canonical_matrices))

roll_r_squared = pandas.DataFrame(roll_r_squared, index=data_set_names).sort()
steer_r_squared = pandas.DataFrame(steer_r_squared, index=data_set_names).sort()

tables_directory = '../tables'
if not os.path.exists(tables_directory):
    os.makedirs(tables_directory)

roll_r_squared.to_csv(os.path.join(results_directory, 'roll_r_squared.csv'))
roll_r_squared.to_latex(os.path.join(tables_directory,
                                     'roll_r_squared.tex'),
                        float_format=lambda x: '{:1.1f}'.format(x * 100.0))

steer_r_squared.to_csv(os.path.join(results_directory, 'steer_r_squared.csv'))
steer_r_squared.to_latex(os.path.join(tables_directory,
                                      'steer_r_squared.tex'),
                         float_format=lambda x: '{:1.1f}'.format(x * 100.0))
