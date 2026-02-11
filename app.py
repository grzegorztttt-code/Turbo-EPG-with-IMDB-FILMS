import streamlit as st
from importer import run_import
from db import init_db

st.set_page_config(layout="wide")

init_db()

st.title("📺 TV Guide TURBO")

if st.button("Import EPG"):
    bar = st.progress(0)
    run_import(bar)
    st.success("Import finished 🚀")
