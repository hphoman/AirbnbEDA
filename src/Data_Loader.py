import streamlit as st
from src.Cleaning import build_cities
from src.Analysis import build_dashboard_data
from src.Plots import Plotter

@st.cache_resource(show_spinner=False)
def load_dashboard_data():
    cities = build_cities()
    data = build_dashboard_data(cities)
    return data
