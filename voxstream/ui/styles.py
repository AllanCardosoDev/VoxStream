"""Custom CSS injection for the VoxStream Streamlit UI."""

import streamlit as st


def inject_custom_css() -> None:
    """Inject global custom CSS rules into the Streamlit app."""
    st.markdown(
        """
        <style>
        .main-title {
            text-align: center;
            color: #1E88E5;
            margin-bottom: 0;
        }
        .sub-title {
            text-align: center;
            color: #666;
            margin-top: 0;
        }
        .footer {
            text-align: center;
            color: #666;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
