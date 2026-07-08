import matplotlib.pyplot as plt
import streamlit as st
from src.Data_Loader import load_dashboard_data
from src.Plots import Plotter

data= load_dashboard_data()
plots = Plotter(data)

st.markdown("""
# Availability

The Inside Airbnb dataset reports listing availability over four booking horizons: 30, 60, 90, and 365 days. To provide 
a consistent measure of short-term availability across all cities, the 90-day availability window is used throughout 
this analysis.

One limitation of this analysis is that the Inside Airbnb dataset records whether a listing is available, but does not 
distinguish between nights that have already been booked and nights intentionally blocked by the host. Consequently, 
lower availability should not be interpreted exclusively as higher booking demand.

Availability varies more substantially across cities than many of the other metrics considered throughout this report. 
While Austin and Chicago exhibit nearly identical distributions, Los Angeles contains a much larger concentration of 
listings with high availability. Portland falls between these extremes, whereas New York displays by far the greatest 
variability.
""")

_, center, _ = st.columns([1, 2, 1])

with center:
    fig = plots.city_availability(figsize=(10, 8))
    st.pyplot(fig)
    plt.close()

st.divider()

st.markdown("""
    ## Availability per Borough
    The borough-level analysis demonstrates that New York is not a homogeneous rental market. Manhattan and Brooklyn 
    exhibit substantially broader availability distributions than the remaining boroughs, explaining the unusually large
    spread observed in the city-wide violin plot.
    """)

_, center, _ = st.columns([1, 2, 1])

with center:
    fig = plots.borough_availability(figsize=(10, 8))
    st.pyplot(fig, width=750)
    plt.close()

st.divider()

st.markdown("""
## Availability Between Host Types and Listing Types

Availability  and listing composition remains remarkably consistent across host categories. Although modest differences 
exist, the median availability differs by only a few days in most cities.

Overall, the availability analysis suggests that geographic market conditions exert a stronger influence on listing 
availability than either host composition or room type.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Availability per Host Type")
    fig = plots.host_availability(figsize=(10, 10))
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("### Availability per Room Type")
    fig = plots.room_availability(figsize=(10, 10))
    st.pyplot(fig)
    plt.close()