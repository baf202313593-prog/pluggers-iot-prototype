import streamlit as st
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Pluggers App",
    page_icon="💡",
    layout="centered"
)

# --- State Management ---
# Initialize session state variables if they don't exist
if 'power' not in st.session_state:
    st.session_state['power'] = False 
if 'brightness' not in st.session_state:
    st.session_state['brightness'] = 50      
if 'bulb_color' not in st.session_state:
    st.session_state['bulb_color'] = "#FFD700" # Default Gold/Yellow
if 'reading_mode' not in st.session_state:
    st.session_state['reading_mode'] = False
if 'dim_mode' not in st.session_state:
    st.session_state['dim_mode'] = False

# --- Callback Functions ( The "Smart" Logic ) ---
def update_reading_mode():
    if st.session_state.reading_mode:
        st.session_state.dim_mode = False # Turn off Dim if Reading is on
        st.session_state.power = True     # Ensure light is on
        st.session_state.brightness = 85
        st.session_state.bulb_color = "#E0FFFF" # Cool White
    else:
        # If turned off, revert to standard
        st.session_state.bulb_color = "#FFD700"

def update_dim_mode():
    if st.session_state.dim_mode:
        st.session_state.reading_mode = False # Turn off Reading if Dim is on
        st.session_state.power = True         # Ensure light is on
        st.session_state.brightness = 25
        st.session_state.bulb_color = "#FF8C00" # Deep Orange
    else:
        # If turned off, revert to standard
        st.session_state.bulb_color = "#FFD700"

# --- UI Design ---

# 1. Header Section
col_back, col_title, col_gear = st.columns([1, 4, 1])
with col_back:
    st.write("←") # Mock back button
with col_title:
    st.markdown("<h3 style='text-align: center; margin: 0;'>LIVING ROOM</h3>", unsafe_allow_html=True)
with col_gear:
    st.write("⚙️") # Mock settings icon

st.write("") # Spacer

# 2. Main Bulb Display (Your favorite part)
# We put this in a container to separate it visually
with st.container(border=False):
    
    # Dynamic styling based on power state
    if st.session_state.power:
        glow_intensity = st.session_state['brightness'] / 1.5
        glow_color = st.session_state['bulb_color']
        opacity = 1.0
        status_text = "STATUS: ON"
    else:
        glow_intensity = 0
        glow_color = "transparent"
        opacity = 0.2
        status_text = "STATUS: OFF"

    st.markdown(
        f"""
        <div style="
            text-align: center; 
            font-size: 120px; 
            padding: 20px;
            filter: drop-shadow(0 0 {glow_intensity}px {glow_color});
            opacity: {opacity};
            transition: all 0.5s ease;">
        💡
        </div>
        <p style="text-align: center; font-weight: bold; color: #555;">{status_text}</p>
        """, unsafe_allow_html=True
    )

st.write("") 

# 3. Control Sections (The "Boxed" Look from your drawing)

# --- Box A: Brightness ---
with st.container(border=True):
    # Master Power Toggle
    st.toggle("Master Power", key="power")
    
    st.write("---")
    
    # Slider
    col_icon, col_slider = st.columns([1, 5])
    with col_icon:
        st.write("🔅")
    with col_slider:
        if st.session_state.power:
            st.slider("Brightness", 0, 100, key="brightness", label_visibility="collapsed")
        else:
            st.slider("Brightness", 0, 100, 0, disabled=True, label_visibility="collapsed")

# --- Box B: Modes (The Toggles you wanted) ---
with st.container(border=True):
    st.write("**Modes**")
    
    # Toggle for Reading Mode
    st.toggle("Reading Mode", key="reading_mode", on_change=update_reading_mode)
    
    # Toggle for Dim Light
    st.toggle("Dim Light", key="dim_mode", on_change=update_dim_mode)

# --- Box C: Schedule ---
with st.container(border=True):
    st.write("**Schedule**")
    
    sch_col1, sch_col2 = st.columns(2)
    with sch_col1:
        st.time_input("Start", datetime.time(8, 00))
    with sch_col2:
        st.time_input("End", datetime.time(21, 00))
        
    st.write("")
    st.toggle("Enable Schedule", value=True)