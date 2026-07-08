import matplotlib.pyplot as plt
import streamlit as st
from src.Data_Loader import load_dashboard_data
from src.Plots import Plotter

data = load_dashboard_data()
plots = Plotter(data)

st.markdown("""
    # Airbnb Market Explorer
    
    This dashboard explores Airbnb markets across five major U.S. cities using publicly available Inside Airbnb data.
    The analysis combines exploratory data analysis, spatial clustering, and regression modeling to investigate how 
    pricing, host composition, listing room types, and availability differ across cities. Use the sidebar to navigate
    between topics and the dropdown menus to explore individual markets.

""")

option = st.selectbox(
    "What city would you like to explore?",
    ["Austin", "Chicago", "Los Angeles", "New York", "Portland"])


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Listings', data.metrics[option]['Listings'], None)
with col2:
    st.metric('Median Rental Price', f'${data.metrics[option]['Median Price']}', None)
with col3:
    st.metric('Number of Hosts', data.metrics[option]['Unique Hosts'], None)
with col4:
    st.metric("Median Days Available", data.metrics[option]['Median Availability'], None)

_, center, _ = st.columns([1, 2, 1])

with center:
    fig = plots.clusters(city=option,figsize=(12,10))
    st.pyplot(fig)
    plt.close()


with st.expander("How were the clusters defined?"):
    st.markdown(f"""
    DBSCAN (Density-Based Spatial Clustering of Applications with Noise), an unsupervised machine learning algorithm,
    was used to define all cluster. The algorithm relies on two parameter: the maximum radius of a neighborhood,
    (epsilon) and the minimum number of points required to form a cluster. The algorithm will then cluster the points,
    and any point that isn't with a cluster is labeled as an outlier.
    
    For {option}, we chose epsilon = {data.param_pairs[option][0]}, and minimum points = {data.param_pairs[option][1]}. 
    """)

