import streamlit as st
from data_retrieval import retrieve_all_data, convert_data_to_dfs
from visualize_data import create_economic_dashboard
from llm_summarizer import generate_economic_summary

def main():
    st.set_page_config(
        page_title="Economic Health Dashboard",
        layout="wide",
    )

    st.title("Economic Health Dashboard")

    if st.button("Get Fresh Data"):
        st.info("Fresh economic data is being retrieved. This may take a moment.")
        with st.spinner("Updating economic data..."):
            retrieve_all_data()
            data = convert_data_to_dfs()
            generate_economic_summary(data)
        st.success("Fresh economic data has been generated.")

    with open('economic_data/llm_summary', 'r') as f:
        llm_summary = f.read()

    economic_data = convert_data_to_dfs()

    fig = create_economic_dashboard(economic_data)

    st.plotly_chart(fig, use_container_width=(True))

    if st.button("Generate AI Summary"):
        with st.spinner("Analyzing economic metrics..."):
            summary = llm_summary
        st.subheader("Economic Summary")
        st.write(summary)

if __name__ == "__main__":
    main()