from orcropTab1 import modalContent
from orcropTab2 import tab1Content
from orcropTab3 import tab2Content
import streamlit as st

# Title of the app
st.title('OR Farming Calculator')
custom_css = """
<style>
.st-emotion-cache-fw8xvw { /* stElementContainer */
  width: 100%;
  max-width: 100%;  
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if 'calc' not in st.session_state:
    st.session_state.calc = True

# Function to set the active tab
def set_active_tab(tab_name):
    st.session_state.calc = not st.session_state.calc

# Function to show the dialog with crop information
@st.dialog("How to Use")
def show_crop_dialog():
    modalContent() 

# Create columns for buttons
col1, col2 = st.columns(2)

with col1:
    st.button("Crop Calculator", on_click=set_active_tab, args=("Tab 1",))
with col2:
    if st.button("How to Use"):
        show_crop_dialog()  # Call the dialog function

# Display content based on the active tab
if st.session_state.calc:
    tab1Content()
else:
    tab2Content()