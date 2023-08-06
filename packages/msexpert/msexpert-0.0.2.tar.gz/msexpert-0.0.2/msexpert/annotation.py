# Rules for Annotation
import numpy as np
from numba import njit
from constants import mass_dict

def parse_sequence(sequence):
    return [_ for _ in sequence]

def get_b_ions(parsed_pep):

    ions = {}
    n_frags = (len(parsed_pep) - 1) * 2
    frag_masses = np.zeros(n_frags, dtype=np.float64)

    frag_m = mass_dict["Proton"]
    for idx, _ in enumerate(parsed_pep[:-1]):
        frag_m += mass_dict[_]
        ions[f'b_{idx+1}'] =  frag_m

    return ions

def get_y_ions(parsed_pep):
    ions = {}
    n_frags = (len(parsed_pep) - 1) * 2
    frag_masses = np.zeros(n_frags, dtype=np.float64)

    frag_m = mass_dict["Proton"] + mass_dict["H2O"]
    for idx, _ in enumerate(parsed_pep[::-1][:-1]):
        frag_m += mass_dict[_]
        ions[f'y_{idx+1}'] =  frag_m

    return ions

def match_ions(ions, db_frag, ppm=True, frag_tol = 30):
    """
    Assumes ions are sorted
    """

    matches = []

    ions_ = list(ions.keys())

    q_max = len(ions_)
    d_max = len(db_frag)

    q, d = 0, 0  # q > query, d > database

    while q < q_max and d < d_max:
        mass1 = ions[ions_[q]]
        mass2 = db_frag[d]
        delta_mass = mass1 - mass2

        if ppm:
            sum_mass = mass1 + mass2
            mass_difference = 2 * delta_mass / sum_mass * 1e6
        else:
            mass_difference = delta_mass

        if abs(mass_difference) <= frag_tol:

            matches.append((d, ions_[q], mass_difference)) #mass_idx, ion type, tolerance
            d += 1
            q += 1  # Only one query for each db element
        elif delta_mass < 0:
            q += 1
        elif delta_mass > 0:
            d += 1

    return matches

def get_loss_dict(ion_dict, loss, matched):

    loss_dict = {}

    for ion, mass in ion_dict.items():
        if ion in matched:
            loss_dict[ion+'-'+loss] = mass-mass_dict[loss]

    return loss_dict


# Annotations Scheme: query_idx (query_index), ion_type(b_1,y _2), tolerance)
import streamlit as st 
def get_annotations(masses, intensities, peptide_sequence):

    annotations = []
    parsed_pep = parse_sequence(peptide_sequence)

    b_ions = get_b_ions(parsed_pep)
    y_ions = get_y_ions(parsed_pep)

    annotations.extend(match_ions(b_ions, masses))
    annotations.extend(match_ions(y_ions, masses))

    matched_ions = [_[1] for _ in annotations]

    annotations.extend(match_ions(get_loss_dict(b_ions, 'H2O', matched_ions), masses))
    annotations.extend(match_ions(get_loss_dict(y_ions, 'H2O', matched_ions), masses))

    return annotations


