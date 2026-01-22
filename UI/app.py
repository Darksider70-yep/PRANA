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

# -------------------------------------------------
# Streamlit config
# -------------------------------------------------
st.set_page_config(page_title="PRANA", layout="centered")
st.title("PRANA — Disaster Relief Prioritization")

# -------------------------------------------------
# City Selector
# -------------------------------------------------
city = st.selectbox("Select city", ["Chennai", "Generic City"])

if city == "Chennai":
    ZONES = [z.copy() for z in CHENNAI_ZONES]
else:
    ZONES = [z.copy() for z in GENERIC_ZONES]

# -------------------------------------------------
# Disaster Selector
# -------------------------------------------------
disaster_type = st.selectbox(
    "Select disaster type",
    ["Flood", "Cyclone", "Earthquake"]
)

profile = DISASTER_PROFILES[disaster_type]
st.caption(f"Scenario: {city} — {disaster_type}")

# -------------------------------------------------
# Image Upload (Optional ML)
# -------------------------------------------------
st.subheader("Upload Disaster Image (Optional)")
uploaded_image = st.file_uploader(
    "Upload satellite / drone image",
    type=["jpg", "jpeg", "png"]
)

# -------------------------------------------------
# Time Input (STABLE)
# -------------------------------------------------
hours = st.number_input(
    "Hours since disaster",
    min_value=1,
    max_value=48,
    value=6,
    step=1
)

urgency = time_urgency(hours, profile["urgency_curve"])
st.caption(f"⏱ Urgency factor: {urgency}")

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

    # ML-based damage estimation
    if uploaded_image is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_image.read())
            zone["damage_score"] = estimate_damage_from_image(tmp.name)

    # Priority score
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

# Sort by priority
results.sort(key=lambda x: x["priority_score"], reverse=True)

# -------------------------------------------------
# Map Visualization (True Color)
# -------------------------------------------------
st.subheader("Priority Map (Color-Coded)")

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

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=11,
        pitch=0
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Priority Score: {priority}"}
    )

    st.pydeck_chart(deck)

    st.markdown("""
    ### Priority Legend
    - 🔴 **High Priority** – Immediate rescue & medical aid
    - 🟠 **Medium Priority** – Medical aid & essential supplies
    - 🟢 **Low Priority** – Monitoring & support
    """)
else:
    st.warning("Location data not available for selected zones.")

# -------------------------------------------------
# Results Display
# -------------------------------------------------
for idx, zone in enumerate(results, start=1):
    band = priority_band(zone["priority_score"])
    st.subheader(f"#{idx} — {zone['zone_name']} ({band})")
    st.metric("Priority Score", zone["priority_score"])
    st.write("**Recommended Action:**", zone["relief"])
    st.write("**Reasons:**")
    for r in zone["reasons"]:
        st.write("•", r)
    st.divider()
