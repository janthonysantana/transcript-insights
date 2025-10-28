import sys
import streamlit as st

from pages.Main import show_page

sys.path.append(".")

st.set_page_config(
    page_title="Transcript Insights - A tool to understand transcription",
    page_icon   ="🗣️"
)

if __name__ == "__main__":
    show_page()