import streamlit as st
from agent import ambient_agent

st.title("Ambient Finance Simulation")

user_input = st.text_input("Ask your financial assistant:")

if st.button("Run Simulation"):
    response = ambient_agent(user_input)
    st.write("Assistant Response:")
    st.success(response)
