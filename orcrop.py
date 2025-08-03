from orcropTab1 import tab1Content
from orcropTab2 import tab2Content
from orcropTab3 import tab3Content
import streamlit as st

# Title of the app
st.title('OR Farming Calculator')
custom_css = """
<style>
.st-emotion-cache-z8vbw2 { /* stElementContainer */
  width: 100%;
  max-width: 100%;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state for active tab if it doesn't exist
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Tab 1'

# Function to set the active tab
def set_active_tab(tab):
    st.session_state.active_tab = tab

# Create columns for buttons
col1, col2, col3 = st.columns(3)
# Create buttons for tabs
with col1:
    st.button("How to Use", on_click=set_active_tab, args=("Tab 1",))
with col2:
    st.button("Crop Calculator", on_click=set_active_tab, args=("Tab 2",))
with col3:
    st.button("Calculated Results", on_click=set_active_tab, args=("Tab 3",))

# Display content based on the active tab
if st.session_state.active_tab == 'Tab 1':
    tab1Content()
elif st.session_state.active_tab == 'Tab 2':
    tab2Content()
elif st.session_state.active_tab == 'Tab 3':
    tab3Content()