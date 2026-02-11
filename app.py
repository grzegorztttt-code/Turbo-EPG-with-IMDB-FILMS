import streamlit as st
from importer import run_import

st.title("Turbo EPG z TMDB")

bar = st.progress(0)
run_import(bar)

st.success("Gotowe!")
