import matplotlib.pyplot as plt
import streamlit as st
from src.Data_Loader import load_dashboard_data
from src.Plots import Plotter

data = load_dashboard_data()
plots = Plotter(data)

st.markdown("""
# Price Drivers

One of our goals is to get a basic idea of what factors drive a higher rental price. A natural way of answering this 
question is to perform regression analysis. As a proof of concept, we perform an ordinary least-squares estimation on a 
few columns that are relatively independant to one another but may be associated to an increase in price. Using Python's
Statsmodel module, we can then perform the regression an get an see if, when the other independat variables are held 
constant, a change in a variable will result in a change in monthly price. 
 
To obtain a meaningful regression, our comparisons should be made among similar listing types. For example, an entire 
home and a hotel room serve different markets and are therefore not directly comparable. Looking at the room types 
across all five cities we have the following break down of listing types:

- Entire Homes/Apartments: 68.33%
- Private Rooms: 30.07%
- Shared Rooms: 0.6888%
- Hotel Rooms: 0.9017%

Shared rooms and hotel rooms represent less than 1% of the observations and were therefore excluded from the regression
 analysis due to insufficient sample sizes.

Private rooms, while more common, presented a different challenge. Multiple model specifications were explored, 
including different combinations of explanatory variables. Across all five cities, these models consistently exhibited 
poor explanatory power, few explanatory variables were statistically significant, and the overall model significance 
remained weak. Consequently, the remaining analysis focuses on Entire Home/Apt listings, where the regression models 
produced substantially stronger and more interpretable results.
""")

option = st.selectbox(
    "What city would you like to explore?",
    ["Austin", "Chicago", "Los Angeles", "New York", "Portland"])

def pvalue_checks(pvalue:float) -> tuple:
    if pvalue < 0.05:
        return "Significant", "green", "off"
    else:
        return "Not Significant", "red", "off"

def get_intervals(coefficient_names, intervals) -> dict:
    plus_minus = []
    for i in range(len(coefficient_names)):
        val = (intervals.iloc[i, 1] - intervals.iloc[i, 0])/2
        plus_minus.append(val)
    return dict(zip(coefficient_names, plus_minus))


col1, col2 = st.columns(2)

with col1:
    st.markdown("""
            ### Regression Coefficients
    """)
    fig = plots.regression_coef(city=option, figsize=(10, 10))
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown("""
    ### Regression Values and Significance
    """)
    pvalues = data.price_models[option].pvalues.drop("Intercept").tolist()
    coefficient_names = ['Accommodates', 'Host is Superhost', 'Bathrooms', 'Review Score']
    coef = data.price_models[option].params.drop("Intercept").tolist()
    intervals = data.price_models[option].conf_int(alpha=0.05).drop("Intercept")
    intervals = get_intervals(coefficient_names, intervals)
    for pvalue, coef, name in zip(pvalues, coef, coefficient_names):
        sig, color, arrow = pvalue_checks(pvalue)
        st.metric(name, f'\\${round(coef, 2)} \u00B1 \\${round(intervals[name], 2)}', sig, delta_color=color, delta_arrow=arrow)

r_squared_checkbox = st.checkbox("See R-squared")
std_checkbox = st.checkbox("Show Standard Deviations")

if r_squared_checkbox:
    r_squared = data.price_models[option].rsquared
    adjusted_r_squared = data.price_models[option].rsquared_adj

    col1_inner, col2_inner = st.columns(2)
    with col1_inner:
        st.metric('R-squared', round(r_squared, 2), delta=None)
    with col2_inner:
        st.metric('Adjusted R-Squared', round(adjusted_r_squared, 2), delta=None)

if std_checkbox:
    stds = data.price_models[option].bse.tolist()
    st.markdown("### Standard Deviations")
    for name, deviations in zip(coefficient_names, stds):
        st.write(f'{name}: {deviations:.2f}')

with st.expander("What does this model mean?"):
    st.markdown("""
    This model provided a linear relationship between our chosen independent variable. Then, if a variable is determined 
    to be significant, we can estimate a change in price by looking at the value of the coefficient. For example, the 
    variable of "bathrooms" is significant in Portland. So, if we compare two nearly identical listings with the only 
    difference being the number of bathrooms, then we would expect the listing having more bathrooms to have a $68.16 
    increase in price per additional bathroom. 
    """)
with st.expander("How did we determine if a coefficient is significant?"):
    st.markdown("""
    The models that are calculated from the Statsmodel module come with many types of statics, include p-values. In 
    general, p-values are used to determine whether a relationship between our independent variables and a change in 
    price is caused by an actual relationship or if a change could have been caused by random chance. If a p-value is
    below 0.05, there is a high likelyhood that an change in the independent variable will result in a change in price 
    with other independent variables held constant. However, if our p-value is equal to or above 0.05, there is not 
    enough evidence to conclude that a relationship exists. 
    
    If a variable is listed as significant, it's p-value is less than 0.05 and thus it is likely that a relationship 
    exists for that variable. 
    """)