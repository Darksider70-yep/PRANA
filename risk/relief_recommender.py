# What help is needed where

def recommend_relief(zone):
    damage = zone["damage_score"]
    access = zone["hospital_distance_km"]

    if damage >= 0.8:
        return "Rescue teams, medical aid, emergency evacuation"
    elif damage >= 0.6:
        if access > 10:
            return "Medical aid units and mobile clinics"
        else:
            return "Medical aid and food supply"
    else:
        return "Food supply, shelter, and sanitation support"
