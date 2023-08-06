# import libraries
import streamlit as st

import numpy as np
import pandas as pd

import hvplot
import hvplot.pandas

import holoviews as hv
hv.extension('bokeh', logo=False)

# create sample data
@st.cache
def get_data():
    return pd.DataFrame(data=np.random.normal(size=[50, 2]), columns=['col1', 'col2'])

df = get_data()

# streamlit plotting works
st.line_chart(df)

# creating a holoviews plot
nice_plot = df.hvplot(kind='scatter')

# this doesn't work unfortunately. How can i show 'nice_plot'
st.bokeh_chart(nice_plot)
