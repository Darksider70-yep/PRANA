# Priority computation logic

def calculate_vulnerability(zone):
    return (
        0.4 * zone["population_density"] +
        0.3 * zone["elderly_ratio"] +
        0.3 * zone["children_ratio"]
    )


def calculate_access_risk(zone):
    return min(zone["hospital_distance_km"] / 20.0, 1.0)

def calculate_priority(zone, time_urgency, profile):
    vulnerability = calculate_vulnerability(zone)
    access_risk = calculate_access_risk(zone)

    w = profile["weights"]

    priority_score = (
        w["damage"] * zone["damage_score"] +
        w["vulnerability"] * vulnerability +
        w["access"] * access_risk +
        w["time"] * time_urgency
    )

    return round(priority_score, 3)
