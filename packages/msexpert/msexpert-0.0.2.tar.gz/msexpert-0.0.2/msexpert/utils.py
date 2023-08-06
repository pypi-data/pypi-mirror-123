#utils
import numpy as np
import streamlit as st 

def parse_input(peak_list):

    masses = []
    intensities = []

    lines = peak_list.splitlines()

    for line in lines:
        mass, int_ = line.split('\t')
        masses.append(float(mass))
        intensities.append(float(int_))

    masses = np.array(masses)
    intensities = np.array(intensities)

    sortindex = np.argsort(masses)

    return masses[sortindex], intensities[sortindex],