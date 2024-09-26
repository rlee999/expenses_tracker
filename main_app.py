# to run

import streamlit as st

pg = st.navigation([st.Page("1_import.py"), st.Page("2_analyse.py")])
pg.run()