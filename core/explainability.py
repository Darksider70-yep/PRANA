# "Why this zone?" logic

def explain_zone(zone, priority_score):
    reasons = []

    if zone["damage_score"] >= 0.75:
        reasons.append("Severe flood damage reported")

    if zone["population_density"] >= 0.75:
        reasons.append("High population density")

    if zone["hospital_distance_km"] >= 10:
        reasons.append("Limited access to medical facilities")

    if zone["elderly_ratio"] >= 0.25:
        reasons.append("High elderly population")

    return {
        "zone_id": zone["zone_id"],
        "zone_name": zone["name"],
        "priority_score": priority_score,
        "reasons": reasons
    }
