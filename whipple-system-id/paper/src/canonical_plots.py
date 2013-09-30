#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script generates several plots which compare the linear
characteristics of the model identified from the data taken from rider L in
the pavilion floor. You must run identify.py first to generate the
identified models."""

# standard library
import os
import cPickle

# external libraries
import numpy as np
import matplotlib.pyplot as plt
from dtk import bicycle, control
from canonicalbicycleid import canonical_bicycle_id as cbi

goldenRatio = (1. + np.sqrt(5.)) / 2.
params = {'axes.labelsize': 10,
          'axes.grid': False,
          'text.fontsize': 10,
          'legend.fontsize': 8,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          }
plt.rcParams.update(params)

# Load in precomputed results from identify.py.
results_directory = '../data'
with open(os.path.join(results_directory, 'id-matrices.p'), 'r') as f:
    id_matrices = cPickle.load(f)


# Eigenvalues versus speed parameters.
v0 = 0.
vf = 10.
num = 100

# Load the identified model from data for rider L and in pavillion floor and
# generate the eigenvalues an eigenvectors as a function of speed.
iM, iC1, iK0, iK2, iH = id_matrices['L-P']
speeds, iAs, iBs = bicycle.benchmark_state_space_vs_speed(iM, iC1, iK0, iK2,
                                                          v0=v0, vf=vf,
                                                          num=num)
w, v = control.eig_of_series(iAs)
iEigenvalues, iEigenvectors = control.sort_modes(w, v)

# Load the Whipple model M, C1, K0, K2, H from first principles and generate
# the eigenvalues and eigenvectors as a function of speed.
wM, wC1, wK0, wK2 = cbi.load_benchmark_canon(['Luke'])['Luke']
wH = cbi.lateral_force_contribution(['Luke'])['Luke']
speeds, wAs, wBs = bicycle.benchmark_state_space_vs_speed(wM, wC1, wK0, wK2,
                                                          v0=v0, vf=vf,
                                                          num=num)
w, v = control.eig_of_series(wAs)
wEigenvalues, wEigenvectors = control.sort_modes(w, v)

# Load the Arm model state space for each rider from first principles and
# generate the eigenvalues and eigenvectors as a function of speed.
aAs, aBs, aSpeed = cbi.mean_arm(['Luke'])
indices = np.int32(np.round(speeds * 10))
w, v = control.eig_of_series(aAs[indices])
aEigenvalues, aEigenvectors = control.sort_modes(w, v)

rlfig = cbi.plot_rlocus_parts(speeds, iEigenvalues, wEigenvalues,
                              aEigenvalues)
rlfig.axes[0].set_ylabel('')
rlfig.set_size_inches(4.0, 4.0 / goldenRatio)
plt.tight_layout()
rlfig.savefig('../figures/L-P-eig.pdf')

# Root locus with respect to speed.
v0 = 0.
vf = 10.
num = 20
speeds, iAs, iBs = bicycle.benchmark_state_space_vs_speed(iM, iC1, iK0, iK2,
                                                          v0=v0, vf=vf,
                                                          num=num)
iEig, null = control.eig_of_series(iAs)

speeds, wAs, wBs = bicycle.benchmark_state_space_vs_speed(wM, wC1, wK0, wK2,
                                                          v0=v0, vf=vf,
                                                          num=num)
wEig, null = control.eig_of_series(wAs)

indices = np.int32(np.round(speeds * 10))
aEig, null = control.eig_of_series(aAs[indices])
rlcfig = cbi.plot_rlocus(speeds, iEig, wEig, aEig)
rlcfig.set_size_inches(3.0, 3.0)
plt.tight_layout()
rlcfig.savefig('../figures/L-P-rlocus.pdf')

# Plot Bode plots of the four basic transfer functions for a few speeds.
speeds = np.array([2.0, 4.0, 6.0, 9.0])
null, iAs, iBs = bicycle.benchmark_state_space_vs_speed(iM, iC1, iK0, iK2,
                                                        speeds)
null, wAs, wBs = bicycle.benchmark_state_space_vs_speed(wM, wC1, wK0, wK2,
                                                        speeds)
figs = cbi.plot_bode(speeds, iAs, iBs, wAs, wBs, aAs, aBs)
for fig in figs:
    fig.set_size_inches(4., 4. / goldenRatio)
    leg = fig.phaseAx.legend(loc=4)
    plt.setp(leg.get_texts(), fontsize='5.0')

figs[0].savefig('../figures/L-P-Tphi-Phi.pdf')
figs[1].savefig('../figures/L-P-Tphi-Del.pdf')
figs[2].savefig('../figures/L-P-Tdel-Phi.pdf')
figs[3].savefig('../figures/L-P-Tdel-Del.pdf')

# Generate a comparison table in LaTeX


def to_latex_bmatrix(arr):

    if len(arr.shape) < 2:
        arr = arr.reshape(arr.shape[0], 1)

    bmatrix = '  $\\begin{bmatrix}\n'
    for row in arr:
        bmatrix += '    '
        for i, val in enumerate(row):
            bmatrix += '{:1.3f} '.format(val)
            if i != len(row) - 1:
                bmatrix += '& '
        bmatrix += '\\\\\n'
    bmatrix += r'  \end{bmatrix}$'

    return bmatrix


def to_tabular(models):

    tabular = \
r"""\begin{tabular}{lccccc}
  \toprule
  Model & $\mathbf{M}$ & $\mathbf{C}_1$ & $\mathbf{K}_0$ & $\mathbf{K}_2$ & $H$ \\
  \midrule
"""
    for i, (k, v) in enumerate(models.items()):
        tabular += '  {} &\n'.format(k)
        for j, arr in enumerate(v):
            tabular += to_latex_bmatrix(arr)
            if j != len(v) - 1:
                tabular += '\n  &\n'
        if i != len(models.keys()) - 1:
            tabular += ' \\\\[0.125in]\n'

    tabular += '\\\\\n  \\bottomrule\n\\end{tabular}'

    return tabular

d = {'Whipple': (wM, wC1, wK0, wK2, wH),
     'L-P': id_matrices['L-P']}

with open('../tables/parameter-compare.tex', 'w') as f:
    f.write(to_tabular(d))
