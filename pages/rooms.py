import matplotlib.pyplot as plt
import streamlit as st
from src.Data_Loader import load_dashboard_data
from src.Plots import Plotter

data = load_dashboard_data()
plots = Plotter(data)

st.markdown("""
    # Room Type Breakdown
    The Inside Airbnb dataset seperates the property typebetween one of four possible options: Entire home/apartments, 
    Private Rooms, Shared Rooms, and Hotel Rooms. We then can look at the percentages of room types across each of the 
    cluster in the cities. Entire property listings seem to have an overwhelming majority in most cities, with a smaller
     percentage of properties being private rooms. Shared rooms and hotel rooms barely have any representation, if at all in a few cities.
""")

option = st.selectbox(
    "What city would you like to explore?",
    ["Austin", "Chicago", "Los Angeles", "New York", "Portland"])


col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Room Type per Cluster
    """)
    fig = plots.cluster_room(city=option, figsize=(8, 7))
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("""
    ### Room Type per Host           
    """)
    fig = plots.room_host(city=option, figsize=(8, 7))
    st.pyplot(fig)
    plt.close()

st.markdown("""
## Room Type per Borough 
For our Boroughs, we see a similar situation to the host composition in the room composition: all boroughs are 
fairly contestant with one another except for Manhattan. In this case Manhattan has an overwhelming majority of 
entire property rentals compared to the private room listings. 

With this in mind, the large price disparity in Manhattan comes into better focus. We have an evenly mixed group of 
hosts renting primarily entire properties in one of the busiest tourist destinations in the world. With these 
factors in mind, the jump in median prices in Manhattan makes more sense because entire properties tend to 
have higher median rental prices which are then driven further up by an existing competitive market. 
""")

_, center, _ = st.columns([1, 2, 1])

with center:
    fig = plots.borough_rooms(figsize=(11, 10))
    st.pyplot(fig)
    plt.close()



