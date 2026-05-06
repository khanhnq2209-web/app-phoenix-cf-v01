import streamlit as st


def init_session_state():
    defaults = {
        "global_nam": [2026, 2027, 2028, 2029, 2030],
        "global_quy": [1, 2, 3, 4],
        "global_nhom": "Tất cả",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_sidebar():
    with st.sidebar:
        st.markdown("**Bộ lọc toàn cục**")

        st.multiselect(
            "NĂM",
            [2026, 2027, 2028, 2029, 2030],
            key="global_nam",
        )
        st.multiselect(
            "QUÝ",
            [1, 2, 3, 4],
            format_func=lambda x: f"Q{x}",
            key="global_quy",
        )
        st.selectbox(
            "NHÓM ĐƠN VỊ",
            ["Tất cả", "GEE", "GEL"],
            key="global_nhom",
        )

        st.markdown("---")
        if st.button("Làm mới dữ liệu", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.caption("Đơn vị: triệu VNĐ")
