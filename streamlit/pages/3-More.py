import streamlit as st

tab1, tab2,tab3,tab4= st.tabs(["The project itself","📂 General structure", "🤖 Our Model", "🔌 The APIs"])
with tab1:
    st.write("This is the metrics overview")
with tab2:
    st.write("This is the detailed breakdown")
with tab3:
    st.write("This is the metrics overview")
with tab4:
    st.write("This is the detailed breakdown")
