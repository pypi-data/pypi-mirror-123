# Helper files for plotting

import matplotlib.pyplot as plt

import numpy as np

def plot_b_ion(idx):
    x = np.array([-0.35, 0.5, 0.5]) + idx
    y = np.array([-2, -2, 2])
    plt.plot(x, y, color ='b', linewidth=LW)
    plt.text(idx, -1, f"b{idx}", fontsize=FONT_SIZE_SMALL, horizontalalignment='center', verticalalignment='center', color='b')

def plot_y_ion(idx, nAA):
    idx_ = nAA-idx+1
    x = np.array([-0.5, -0.5, 0.35]) + idx_
    y = np.array([2, 5, 5])
    plt.plot(x, y, color ='r', linewidth=LW)
    plt.text(idx_, 4, f"y{idx}", fontsize=FONT_SIZE_SMALL, horizontalalignment='center', verticalalignment='center', color='r')

def plot_y_loss(idx, nAA, losstype, offset=0):
    idx_ = nAA-idx+1
    x = np.array([-0.5, -0.5, 0.35]) + idx_
    y = np.array([5, 6.5, 6.5]) + offset*1.5
    plt.plot(x, y, color ='tab:orange', linewidth=LW)
    plt.text(idx_, 5.75 + offset*1.5, f"{losstype}", fontsize=FONT_SIZE_SMALL, horizontalalignment='center', verticalalignment='center', color='tab:orange')

def plot_b_loss(idx, losstype, offset=0):
    x = np.array([-0.35, 0.5, 0.5]) + idx
    y = np.array([-3.5, -3.5, -2]) - offset*1.5
    plt.plot(x, y, color ='tab:orange', linewidth=LW)
    plt.text(idx, -2.75 - offset*1.5, f"{losstype}", fontsize=FONT_SIZE_SMALL, horizontalalignment='center', verticalalignment='center', color='tab:orange')

def plot_bounding_rect(nAA, nMods):
    x_ = nAA+2
    y_ = 6+nMods
    x = [0,x_,x_,0]
    y = [-y_+3,-y_+3,y_,y_]
    plt.plot(x,y, color='w')

FONT_SIZE = 25
FONT_SIZE_SMALL = 8
LW = 2

import streamlit as st 

def plot_spectrum_AA(peptide_sequence, annotations=None):

    nAA = len(peptide_sequence)

    sequence = peptide_sequence
    n_term = '_'
    c_term = '_'

    mod_sequence = n_term + sequence + c_term

    matched_ions = []

    fig = plt.figure(figsize=(nAA+2, 3))

    plot_bounding_rect(nAA, 2)

    for idx, aa in enumerate(mod_sequence):
        plt.text(idx, 1, aa, fontsize=FONT_SIZE, horizontalalignment='center', verticalalignment='center')

    if annotations:
        for db_idx, a, tol in annotations:

            if '-' not in a: #Loss
                ion, pos = a.split('_')
                if ion.startswith('b'):
                    plot_b_ion(int(pos))
                else:
                    plot_y_ion(int(pos), nAA)
            
            else:
                ion, _ = a.split('_')

                pos, loss = _.split('-')
                loss = '-'+loss

                if ion.startswith('b'):
                    plot_b_loss(int(pos), loss)
                else:
                    plot_y_loss(int(pos), nAA, loss)

    plt.axis('off')

    return fig

def plot_spectrum(masses, intensities, annotations=None):

    max_int = np.max(intensities)
    ann_limit_ion = max_int*1.4
    ann_limit_loss = max_int*1.2

    fig = plt.figure(figsize=(15, 5))
    plt.vlines(masses, 0, intensities, "k", label="Spectrum", alpha=0.5)


    if annotations:
        for db_idx, a, tol in annotations:
            if 'b' in a:
                color = 'b'
            elif 'y' in a:
                color = 'r'
            else:
                color = 'k'

            if '-' in a:
                lim = ann_limit_loss
                color = 'tab:orange'
            else:
                lim = ann_limit_ion

            plt.vlines(masses[db_idx], intensities[db_idx], lim, linestyle=':', alpha=0.5, color=color)
            plt.text(masses[db_idx], lim, a.replace('_',''), horizontalalignment='center')

    plt.xlabel("m/z")
    plt.ylabel('Intensity')

    plt.ylim([0, max_int*1.5])
    
    return fig


if False:
    plt.vlines(query_frag, 0, query_int, "k", label="Query", alpha=0.5)

    plt.vlines(masses, ints, max(query_int)*(1+0.1*ion_type), "k", label="Hits", alpha=0.5, linestyle=':')

    plt.vlines(masses, 0, ints, "r", label="Hits", alpha=0.5)

    for i in range(len(masses)):
        plt.text(masses[i], (1+0.1*ion_type[i])*max(query_int), ion[i])