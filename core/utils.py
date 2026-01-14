import streamlit as st
def card_percentual(percentual, ano):
    st.markdown(
        f"""
        <div style="
            background-color: #1f2937;
            padding: 14px;
            border-radius: 8px;
            text-align: center;
        ">
            <div style="
                font-size: 13px;
                color: #d1d5db;
                margin-bottom: 6px;
            ">
                {ano}
            </div>
            <div style="
                font-size: 32px;
                font-weight: 700;
                color: #f9fafb;
            ">
                {percentual:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )