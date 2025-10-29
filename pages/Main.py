import streamlit as st
from pages.TranscriptAnalysis import TranscriptAnalysis

# def Navbar():
#     with st.sidebar:
#         st.page_link("app.py", label="Main Page")
        # st.page_link("", label="Analyze Transcript")
        # st.page_link("", label="Batch Transcript Analysis")
        # st.page_link("pages/Favorites.py", label="Favorites")

def show_page():
    # Navbar()

    st.title("Transcript Insights")

    TranscriptAnalysis()    
