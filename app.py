import streamlit as st

from data_retrieval import retrieve_all_data
from visualize_data import create_economic_dashboard
from llm_summarizer import generate_economic_summary

st.set_page_config(
    page_title="Economic Health Dashboard",
    layout="wide",
)

st.title("Economic Health Dashboard")

st.subheader("Dashboard")
fig = create_economic_dashboard(show=False)
st.plotly_chart(fig, use_container_width=True)

if st.button("Generate AI Summary"):
    with st.spinner("Analyzing economic metrics..."):
        summary = generate_economic_summary()
    st.subheader("AI Economic Summary")
    st.write(summary)
