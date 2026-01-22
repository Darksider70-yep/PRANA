DISASTER_PROFILES = {
    "Flood": {
        "weights": {
            "damage": 0.40,
            "vulnerability": 0.20,
            "access": 0.20,
            "time": 0.20
        },
        "urgency_curve": "fast"
    },
    "Cyclone": {
        "weights": {
            "damage": 0.35,
            "vulnerability": 0.25,
            "access": 0.15,
            "time": 0.25
        },
        "urgency_curve": "medium"
    },
    "Earthquake": {
        "weights": {
            "damage": 0.45,
            "vulnerability": 0.25,
            "access": 0.20,
            "time": 0.10
        },
        "urgency_curve": "instant"
    }
}
