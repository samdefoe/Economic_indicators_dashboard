import streamlit as st
from data_retrieval import retrieve_all_data, convert_data_to_dfs
from visualize_data import create_economic_dashboard
from llm_summarizer import generate_economic_summary, _create_all_snapshots
from economy_health_score import generate_economy_health_score

def display_health_bar(score):
    if score >= 80:
        label = "Strong"
        color = "#00C853"
    elif score >= 65:
        label = "Stable"
        color = "#64DD17"
    elif score >= 45:
        label = "Pressured"
        color = "#FFD600"
    else:
        label = "Weak"
        color = "#FF1744"

    st.subheader("Health Score of the Current Economy")

    st.markdown(
        f"""
        <div style="width: 100%; background-color: #E5E7EB; border-radius: 15px; height: 28px;">
            <div style="
                width: {score}%;
                background-color: {color};
                height: 28px;
                border-radius: 15px;
                font-family: Aptos;
                text-align: center;
                color: black;
                font-weight: 700;
                line-height: 28px;
            ">
                {score}/ · {label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    snapshots = _create_all_snapshots(economic_data, return_dict=True)
    economic_score = generate_economy_health_score(snapshots)
    display_health_bar(economic_score)

    fig = create_economic_dashboard(economic_data)

    st.plotly_chart(fig, use_container_width=(True))

    if st.button("Generate AI Summary"):
        with st.spinner("Analyzing economic metrics..."):
            summary = llm_summary
        st.subheader("Economic Summary")
        st.write(summary)

if __name__ == "__main__":
    main()