import streamlit as st

from constants import DEFAULT_SPECTRUM, DEFAULT_SEQUENCE, DEFAULT_CHARGES, AVAILABLE_MODS, AAs
from plotting import plot_spectrum_AA, plot_spectrum
from utils import parse_input
from annotation import get_annotations

st.set_page_config(layout="wide")

st.write('# Expert system')

c1, c2 = st.columns(2)

c1.write('### Peak list')
peak_list = c1.text_area('Peak List', DEFAULT_SPECTRUM)
masses, intensities = parse_input(peak_list)
c1.write(f'{len(masses)} peaks')

c2.write('### Identification')
peptide_sequence = c2.text_input("Peptide sequence", DEFAULT_SEQUENCE)

if not set(peptide_sequence).issubset(AAs):
    c2.error('Sequence contains invalid character')

peptide_charge = c2.selectbox("Peptide charge", DEFAULT_CHARGES, 1)

st.write('### Modifications')

mod_peptide_sequence = '_' + peptide_sequence + '_'

mod_cols = st.columns(len(mod_peptide_sequence))

for idx, AA in enumerate(mod_peptide_sequence):
    mod_cols[idx].selectbox(AA, AVAILABLE_MODS, key=f'{idx}_{AA}')

annotations = get_annotations(masses, intensities, peptide_sequence)

figAA = plot_spectrum_AA(peptide_sequence, annotations)
st.write(figAA)

fig = plot_spectrum(masses, intensities, annotations)
st.write(fig)

