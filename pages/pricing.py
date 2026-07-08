import matplotlib.pyplot as plt
import streamlit as st
from src.Data_Loader import load_dashboard_data
from src.Plots import Plotter

data = load_dashboard_data()
plots = Plotter(data)

def is_average(value: int, type: str):
    if (type != 'median') and (type != 'cv'):
        raise ValueError(f'Type {type} is not available. Type parameter must either be "median" or "cv"')
    else:
        average = sum(data.median_cv_cities[type]) / len(data.median_cv_cities[type])
        if value > average:
            return 'Above average', 'green', 'up'
        elif value < average:
            return 'Below average', 'red', 'down'
        else:
            return 'Average', 'grey', 'off'

st.markdown("""
    # Pricing
    Looking across all cities, the median price is reasonable with tourism and average wages within those cities. 
    What is different though is the variability across the markets. The Coefficient of Variability (CV) of New York and 
    Portland are the only two cities that manage to be relatively centered around their means.
    """)

col1, col2 = st.columns(2)

with col1:
    fig = plots.median_cv(figsize=(10, 10))
    st.pyplot(fig)
    plt.close()

with col2:
    fig = plots.price_population(figsize=(10, 10))
    st.pyplot(fig)
    plt.close()

with st.expander("What is a CV, and what does it measure?"):
    st.markdown("""
        The Coefficient of Variation (CV) measures the dispersion of data points around it's mean. In our case, if the CV 
        is less than one then the market price is more centered. However, if the CV is greater than 1, then the market has 
        more price volatility.
    """)

st.divider()

st.markdown("""
    ## Price per Cluster
""")

option = st.selectbox(
    "What city would you like to explore?",
    ["Austin", "Chicago", "Los Angeles", "New York", "Portland"])

left, right = st.columns([1, 1])

with left:
    fig = plots.price_per_cluster(city=option, figsize=(12, 10))
    st.pyplot(fig, width=750)
    plt.close()

with right:
    idx = data.names.index(option)
    median_val = round(data.median_cv_cities['median'][idx], 2)
    cv_val = round(data.median_cv_cities['cv'][idx], 2)
    median_delta, median_color, median_arrow = is_average(median_val, 'median')
    cv_delta, cv_color, cv_arrow = is_average(cv_val, 'cv')
    st.metric('Median Price', f"${median_val}", delta=median_delta,
              delta_color=median_color, delta_arrow=median_arrow)
    st.metric('CV', cv_val, delta=cv_delta,
              delta_color=cv_color, delta_arrow=cv_arrow)

st.divider()

st.markdown("""
    ## Borough Price Distribution
    Manhattan and Brooklyn make up relatively equal majorities of the listings, with the remaining 20% being split 
    between the remaining boroughs. Looking at the price distribution per borough, we see that Manhattan is 
    substantially more expensive than the other boroughs with Brooklyn trailing behind. Both boroughs are the most 
    expensive boroughs and have the largest influx of tourism which could explain why they are priced so expensively. 
    """)

_, center, _ = st.columns([1, 2, 1])

with center:
    fig = plots.borough_price_listing(figsize=(12, 8))
    st.pyplot(fig, width = 1000)
    plt.close()
