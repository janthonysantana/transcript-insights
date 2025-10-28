
import streamlit as st

uploaded_file = st.file_uploader("Choose a file")

def Navbar():
    with st.sidebar:
        st.page_link("app.py", label="Main Page")
        # st.page_link("pages/Favorites.py", label="Favorites")



def show_page():
    Navbar()

    st.title("Transcript Insights")
    
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        st.write("Filename:", uploaded_file.name)
        st.write("File content (first 100 bytes):", bytes_data[:100])

        st.write("File content (as string):", string_data)
