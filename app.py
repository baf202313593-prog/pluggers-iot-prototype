import streamlit as st
import datetime
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Pluggers App",
    page_icon="💡",
    layout="centered"
)

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'landing' 
if 'selected_room' not in st.session_state:
    st.session_state['selected_room'] = ''

if 'rooms' not in st.session_state:
    st.session_state['rooms'] = [] 

def reset_light_state():
    st.session_state['power'] = False
    st.session_state['brightness'] = 50
    st.session_state['bulb_color'] = "#FFD700"
    st.session_state['reading_mode'] = False
    st.session_state['dim_mode'] = False

if 'power' not in st.session_state: reset_light_state()

# --- Navigation Functions (The Fix) ---

# NO st.rerun() here because we will call this with on_click
def go_to_control(room_name):
    st.session_state['selected_room'] = room_name
    reset_light_state() 
    st.session_state['page'] = 'control'

# NO st.rerun() here because we will call this with on_click
def go_to_landing():
    st.session_state['page'] = 'landing'

# We KEEP st.rerun() here because this is called procedurally inside a form, not a callback
def add_room(name, bulb_id):
    with st.spinner(f"Searching for Device ID: {bulb_id}..."):
        time.sleep(1.0) 
    
    with st.spinner("Verifying Firmware..."):
        time.sleep(0.5)
        
    with st.spinner("Pairing successful!"):
        time.sleep(0.5)

    new_room = {'name': name, 'id': bulb_id}
    st.session_state['rooms'].append(new_room)
    st.success(f"Connected to {name}!")
    time.sleep(1) 
    st.rerun() # Necessary here to refresh the page after form submission

# --- Smart Logic ---
def update_reading_mode():
    if st.session_state.reading_mode:
        st.session_state.dim_mode = False
        st.session_state.power = True
        st.session_state.brightness = 85
        st.session_state.bulb_color = "#E0FFFF" 
    else:
        st.session_state.bulb_color = "#FFD700"

def update_dim_mode():
    if st.session_state.dim_mode:
        st.session_state.reading_mode = False
        st.session_state.power = True
        st.session_state.brightness = 25
        st.session_state.bulb_color = "#FF8C00"
    else:
        st.session_state.bulb_color = "#FFD700"

# =========================================
# PAGE 1: LANDING PAGE
# =========================================
def landing_page():
    st.write("") 
    
    # st.image("logo.png", width=150) 
    
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #003366; margin-bottom: 0px;">PLUGGERS</h1>
            <p style="color: gray; font-size: 14px;">My Home Dashboard</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("---")

    st.subheader("📱 Your Devices")
    
    if len(st.session_state['rooms']) == 0:
        st.info("No devices connected yet. Add a new device below.")
    else:
        for room in st.session_state['rooms']:
            btn_label = f"💡 {room['name']} (ID: {room['id']})"
            
            # UPDATED: We use on_click and args to handle the transition safely
            st.button(
                btn_label, 
                use_container_width=True, 
                key=room['id'],
                on_click=go_to_control,
                args=(room['name'],) # Pass the room name as an argument
            )
    
    st.write("---")

    with st.expander("➕ Add New Device", expanded=True):
        with st.form("add_device_form"):
            st.write("**Pair a new Pluggers Switch**")
            new_room_name = st.text_input("Room Name (e.g. Master Bedroom)")
            new_bulb_id = st.text_input("Device ID (Found on box)")
            
            submitted = st.form_submit_button("Connect & Pair")
            
            if submitted:
                if new_room_name and new_bulb_id:
                    add_room(new_room_name, new_bulb_id)
                else:
                    st.error("Please enter both Room Name and Device ID.")

# =========================================
# PAGE 2: CONTROL PAGE
# =========================================
def control_page():
    col_back, col_title, col_gear = st.columns([1, 4, 1])
    with col_back:
        # UPDATED: Uses on_click callback
        st.button("←", on_click=go_to_landing) 
    with col_title:
        current_room = st.session_state.get('selected_room', 'DEVICE')
        st.markdown(f"<h3 style='text-align: center; margin: 0;'>{current_room}</h3>", unsafe_allow_html=True)
    with col_gear:
        st.write("⚙️")

    st.write("")

    # Bulb Visual
    with st.container(border=False):
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

    # Controls
    with st.container(border=True):
        st.toggle("Master Power", key="power")
        st.write("---")
        col_icon, col_slider = st.columns([1, 5])
        with col_icon: st.write("🔅")
        with col_slider:
            st.slider("Brightness", 0, 100, key="brightness", disabled=not st.session_state.power, label_visibility="collapsed")

    with st.container(border=True):
        st.write("**Modes**")
        st.toggle("Reading Mode", key="reading_mode", on_change=update_reading_mode)
        st.toggle("Dim Light", key="dim_mode", on_change=update_dim_mode)

    with st.container(border=True):
        st.write("**Schedule**")
        sch_col1, sch_col2 = st.columns(2)
        with sch_col1: st.time_input("Start", datetime.time(8, 00))
        with sch_col2: st.time_input("End", datetime.time(21, 00))
        st.write("")
        st.toggle("Enable Schedule", value=True)

# =========================================
# MAIN APP LOGIC
# =========================================
if st.session_state['page'] == 'landing':
    landing_page()
elif st.session_state['page'] == 'control':
    control_page()
