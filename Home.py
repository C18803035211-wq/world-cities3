import streamlit as st

st.set_page_config(page_title="World Cities", layout="centered")

st.title("🌍 World Cities")

st.write("""
Welcome to the World Cities application! 

This application provides information about cities around the world, including data about population, location, and other interesting facts.

Click the button below to explore the cities database and discover fascinating information about destinations worldwide.
""")

if st.button("Go to App", key="home_button"):
    st.switch_page("pages/app.py")
