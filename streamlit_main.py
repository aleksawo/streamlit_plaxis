import streamlit as st
from plxscripting.easy import *
import pandas as pd
import os

#streamlit run your_script.py --server.port 80
from plot_model_tab import run_plaxis_model_plotter


tab1, tab2 = st.tabs(["Plott modell", "Hent ankerkrefter"])

with tab1:
    run_plaxis_model_plotter()

