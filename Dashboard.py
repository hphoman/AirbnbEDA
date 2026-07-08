from src.Data_Loader import load_dashboard_data
import streamlit as st

with st.spinner("Loading Dashboard"):
    data = load_dashboard_data()


st.set_page_config(
    page_title="Airbnb Market Explorer",
    layout="wide"
)

pages = {"Select Feature to Analyze":[
    st.Page("pages/overview.py", title="Overview"),
    st.Page("pages/pricing.py", title="Pricing"),
    st.Page("pages/hosts.py", title="Hosts"),
    st.Page("pages/rooms.py", title="Rooms"),
    st.Page("pages/regression.py", title="Price Drivers"),
    st.Page("pages/availability.py", title="Availability"),
]}

page = st.navigation(pages)
page.run()