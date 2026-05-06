import streamlit as st
from utils.sidebar import init_session_state, render_sidebar

st.set_page_config(
    page_title="GELEX · CASHPLAN",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

with st.sidebar:
    st.markdown("## GELEX · CASHPLAN")
    st.markdown("---")

pages = [
    st.Page("pages/p2_tracking.py", title="Theo dõi dữ liệu", icon="📋"),
    st.Page("pages/p3_dashboard.py", title="Dashboard chiến lược", icon="📊"),
    st.Page("pages/p4_detail.py", title="Chi tiết CTTV", icon="🏢"),
    st.Page("pages/p5_adl.py", title="Ma trận ADL", icon="🎯"),
]

pg = st.navigation(pages)
render_sidebar()
pg.run()
