import matplotlib.pyplot as plt
import streamlit as st
from src.Data_Loader import load_dashboard_data
from src.Plots import Plotter

data = load_dashboard_data()
plots = Plotter(data)

st.markdown("""
    # Host Information
    Across all five cities, hosts range from individuals managing a single listing to organizations operating many 
    listings. To compare these groups, hosts were classified according to the number of active listings associated with 
    each host. We break the hosts into three main categories:
    
    - Individual: A host owning a single listing
    - Small Host: A host owning between 2 and 9 listings
    - Large Host: A host owning 10 or more listings
    """)

option = st.selectbox(
    "What city would you like to explore?",
    ["Austin", "Chicago", "Los Angeles", "New York", "Portland"])

_, center, _ = st.columns([1, 2, 1])

with center:
    fig = plots.host_population_listing_percentages(city=option, figsize=(12,10))
    st.pyplot(fig)
    plt.close()

st.divider()

st.markdown("""
    ## Price per Host

    Individual hosts and small hosts hold a similar majority in the listings on Airbnb. This result is slightly 
    unexpected since small host have at minimum twice the number of listings compared to those who have just a single 
    listing. Because small hosts account for a similar share of listings despite representing a much smaller fraction 
    of hosts, the typical small multi-host appears to manage several listings, while only a relatively small number
    manage close to the upper limit of the category.
""")

_, center, _ = st.columns([1, 2, 1])

with center:
    fig = plots.host_price(city=option, figsize=(8,6))
    st.pyplot(fig)
    plt.close()

st.divider()

st.markdown("""
    ## Borough Host Information
    We note that a majority of boroughs have a fairly consistent percentage of host types, except for Manhattan. 
    Despite making up a minority of the host population and number of listings, it seems that a majority of large hosts 
    have focused their efforts in Manhattan to the point where the number of listings is fairly evenly distributed 
    between all three groups. Looking at the price distribution per host group in Manhattan, we see that they all are 
    fairly equal with the Large hosts slightly less than the other two types of hosts.    
    """)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Host percentages per Borough
    """)
    fig = plots.borough_hosts(figsize=(11, 11))
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("""
    ### Manhattan Prices per Host Group
    """)
    fig = plots.manhattan_price(figsize=(8,8))
    st.pyplot(fig)
    plt.close()
