import streamlit as st

st.set_page_config(
    page_title="RIGAZUP - ML Inventory Planner",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Streamlit Navigation (v1.36+)
pages = {
    "Menu Utama": [
        st.Page("src/overview.py", title="RIGAZUP", icon="🏠", default=True),
        st.Page("pages/1_Upload_Dataset.py", title="Upload Dataset", icon="📂"),
        st.Page("pages/2_Data_Quality.py", title="Data Quality", icon="🧹"),
        st.Page("pages/3_Business_Intelligence.py", title="Business Intelligence", icon="📊"),
        st.Page("pages/4_AI_Forecasting.py", title="AI Forecasting", icon="📈"),
        st.Page("pages/5_Inventory_Management.py", title="Inventory Management", icon="📦"),
        st.Page("pages/6_AI_Insight_Generator.py", title="AI Insight Generator", icon="🧠"),
        st.Page("pages/7_About_Project.py", title="About Project", icon="ℹ️")
    ]
}

pg = st.navigation(pages)
pg.run()
