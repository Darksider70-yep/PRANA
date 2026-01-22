import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from vision.damage_estimator import estimate_damage_from_image
import pandas as pd
import tempfile
import streamlit as st
from demo.mock_data import ZONES
from core.scoring_engine import calculate_priority
from core.explainability import explain_zone
from core.time_decay import time_urgency
from risk.relief_recommender import recommend_relief

st.set_page_config(page_title="PRANA", layout="centered")

st.title("PRANA — Disaster Relief Prioritization")

st.subheader("Upload Disaster Image (Optional)")
uploaded_image = st.file_uploader(
    "Upload satellite/drone image",
    type=["jpg", "jpeg", "png"]
)

hours = st.slider("Hours since disaster", 1, 48, 6)
urgency = time_urgency(hours)

results = []
map_data = []

for zone in ZONES:
    if uploaded_image is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_image.read())
            inferred_damage = estimate_damage_from_image(tmp.name)
            zone["damage_score"] = inferred_damage
    score = calculate_priority(zone, urgency)
    if "lat" in zone and "lon" in zone:
        map_data.append({
            "lat": zone["lat"],
            "lon": zone["lon"],
            "priority": score,
            "name": zone["name"]
        })
    explanation = explain_zone(zone, score)
    explanation["relief"] = recommend_relief(zone)
    results.append(explanation)

results.sort(key=lambda x: x["priority_score"], reverse=True)

st.subheader("Priority Map")

df = pd.DataFrame(map_data)

st.map(
    df,
    latitude="lat",
    longitude="lon",
    size="priority"
)
if len(map_data) == 0:
    st.warning("Location data not available for selected zones.")

for idx, zone in enumerate(results, start=1):
    st.subheader(f"#{idx} — {zone['zone_name']}")
    st.metric("Priority Score", zone["priority_score"])
    st.caption(f"⏱ Time urgency factor: {urgency}")
    st.caption(f"Damage severity (ML-estimated): {zone['priority_score']}")
    st.write("**Recommended Action:**", zone["relief"])
    st.write("**Reasons:**")
    for r in zone["reasons"]:
        st.write("•", r)
    st.divider()
