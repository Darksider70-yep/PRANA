import sys
import os
import tempfile
import pandas as pd
import streamlit as st
import pydeck as pdk

# -------------------------------------------------
# Ensure project root is in Python path
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# Project imports
# -------------------------------------------------
from vision.damage_estimator import estimate_damage_from_image
from core.disaster_profiles import DISASTER_PROFILES
from core.scoring_engine import calculate_priority
from core.explainability import explain_zone
from core.time_decay import time_urgency
from risk.relief_recommender import recommend_relief

from demo.chennai_data import CHENNAI_ZONES
from demo.generic_city_data import ZONES as GENERIC_ZONES


EMERGENCY_FACILITIES = [
    # --------------------
    # Hospitals
    # --------------------
    {
        "name": "Government General Hospital",
        "type": "Hospital",
        "lat": 13.0878,
        "lon": 80.2785
    },
    {
        "name": "Stanley Medical College Hospital",
        "type": "Hospital",
        "lat": 13.1094,
        "lon": 80.2824
    },
    {
        "name": "Kilpauk Medical College Hospital",
        "type": "Hospital",
        "lat": 13.0846,
        "lon": 80.2441
    },
    {
        "name": "Rajiv Gandhi Government Hospital (Omanturar)",
        "type": "Hospital",
        "lat": 13.0810,
        "lon": 80.2707
    },

    # --------------------
    # Fire & Rescue Stations
    # --------------------
    {
        "name": "Chennai Central Fire Station",
        "type": "Fire Station",
        "lat": 13.0823,
        "lon": 80.2757
    },
    {
        "name": "Adyar Fire Station",
        "type": "Fire Station",
        "lat": 13.0065,
        "lon": 80.2572
    },
    {
        "name": "T. Nagar Fire Station",
        "type": "Fire Station",
        "lat": 13.0400,
        "lon": 80.2337
    },
    {
        "name": "Velachery Fire Station",
        "type": "Fire Station",
        "lat": 12.9753,
        "lon": 80.2206
    },
    {
        "name": "Manali Fire Station",
        "type": "Fire Station",
        "lat": 13.1645,
        "lon": 80.2582
    },

    # --------------------
    # Police & Emergency Control
    # --------------------
    {
        "name": "Greater Chennai Police HQ",
        "type": "Police",
        "lat": 13.0674,
        "lon": 80.2546
    },
    {
        "name": "Chennai City Police Control Room",
        "type": "Police",
        "lat": 13.0720,
        "lon": 80.2609
    },

    # --------------------
    # Emergency Operations
    # --------------------
    {
        "name": "Tamil Nadu State Emergency Operations Center",
        "type": "Emergency Ops",
        "lat": 13.0690,
        "lon": 80.2594
    }
]


# -------------------------------------------------
# Streamlit config
# -------------------------------------------------
st.set_page_config(page_title="PRANA", layout="centered")

st.title("PRANA")
st.caption("AI-assisted disaster impact assessment & relief prioritization")

# -------------------------------------------------
# Sidebar Controls
# -------------------------------------------------
with st.sidebar:
    st.header("Scenario Controls")

    city = st.selectbox("City", ["Chennai", "Generic City"])

    disaster_type = st.selectbox(
        "Disaster Type",
        ["Flood", "Cyclone", "Earthquake"]
    )

    st.divider()

    hours = st.number_input(
        "Hours since disaster",
        min_value=1,
        max_value=48,
        value=6,
        step=1
    )

    st.divider()

    uploaded_image = st.file_uploader(
        "Upload disaster image (optional)",
        type=["jpg", "jpeg", "png"]
    )

# -------------------------------------------------
# Dataset selection
# -------------------------------------------------
if city == "Chennai":
    ZONES = [z.copy() for z in CHENNAI_ZONES]
else:
    ZONES = [z.copy() for z in GENERIC_ZONES]

profile = DISASTER_PROFILES[disaster_type]
urgency = time_urgency(hours, profile["urgency_curve"])

# -------------------------------------------------
# Context Bar
# -------------------------------------------------
st.markdown(
    f"""
    <div style="
        padding:10px;
        border-radius:8px;
        background:#0e1117;
        border:1px solid #262730;
        margin-bottom:10px;">
        <b>City:</b> {city} &nbsp; | &nbsp;
        <b>Disaster:</b> {disaster_type} &nbsp; | &nbsp;
        <b>Hours:</b> {hours} &nbsp; | &nbsp;
        <b>Urgency:</b> {urgency}
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def priority_band(score):
    if score >= 0.75:
        return "🔴 High"
    elif score >= 0.55:
        return "🟠 Medium"
    else:
        return "🟢 Low"

def priority_color(score):
    if score >= 0.75:
        return [255, 0, 0]       # Red
    elif score >= 0.55:
        return [255, 165, 0]     # Orange
    else:
        return [0, 200, 0]       # Green

# -------------------------------------------------
# Core Processing
# -------------------------------------------------
results = []
map_data = []

for zone in ZONES:

    # ML-based damage estimation (optional)
    if uploaded_image is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_image.read())
            zone["damage_score"] = estimate_damage_from_image(tmp.name)

    # Priority calculation
    score = calculate_priority(zone, urgency, profile)

    # Map data
    if "lat" in zone and "lon" in zone:
        map_data.append({
            "lat": zone["lat"],
            "lon": zone["lon"],
            "priority": score,
            "color": priority_color(score),
            "radius": int(score * 2000)
        })

    # Explainability + relief
    explanation = explain_zone(zone, score)
    explanation["relief"] = recommend_relief(zone)
    results.append(explanation)

# Sort zones by priority
results.sort(key=lambda x: x["priority_score"], reverse=True)

# -------------------------------------------------
# Map Visualization
# -------------------------------------------------
st.subheader("Operational Priority Map")
st.caption("Color indicates priority • Size indicates urgency")

if len(map_data) > 0:
    df = pd.DataFrame(map_data)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[lon, lat]",
        get_radius="radius",
        get_fill_color="color",
        pickable=True,
        opacity=0.8
    )

    facilities_df = pd.DataFrame(EMERGENCY_FACILITIES)

    facility_layer = pdk.Layer(
        "ScatterplotLayer",
        data=facilities_df,
        get_position="[lon, lat]",
        get_radius=120,
        get_fill_color=[0, 150, 255],  # Blue
        pickable=True,
        opacity=0.9
    )

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=11,
        pitch=0
    )

    deck = pdk.Deck(
        layers=[layer, facility_layer],
        initial_view_state=view_state,
        tooltip={
            "text": "{name}\n{type}\nPriority: {priority}"
        }
    )
    st.pydeck_chart(deck)

    st.markdown("""
    ## Map Legend
    - #🔴 **High Priority Zone** – Immediate rescue & medical aid  
    - 🟠 **Medium Priority Zone** – Medical aid & essential supplies  
    - 🟢 **Low Priority Zone** – Monitoring & support  
    - 🔵 **Emergency Facility** – Fire stations, hospitals, police
    """)

else:
    st.warning("Location data not available for selected zones.")

# -------------------------------------------------
# Results Display
# -------------------------------------------------
for idx, zone in enumerate(results, start=1):
    band = priority_band(zone["priority_score"])
    st.subheader(f"#{idx} — {zone['zone_name']} ({band})")

    cols = st.columns([1, 2])

    with cols[0]:
        st.metric("Priority", zone["priority_score"])

    with cols[1]:
        st.markdown(f"**Action:** {zone['relief']}")
        st.markdown("**Drivers:**")
        for r in zone["reasons"]:
            st.markdown(f"- {r}")

    st.divider()
