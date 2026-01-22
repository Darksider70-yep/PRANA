# Priority computation logic

def calculate_vulnerability(zone):
    return (
        0.4 * zone["population_density"] +
        0.3 * zone["elderly_ratio"] +
        0.3 * zone["children_ratio"]
    )


def calculate_access_risk(zone):
    return min(zone["hospital_distance_km"] / 20.0, 1.0)


def calculate_priority(zone, time_urgency=0.5):
    vulnerability = calculate_vulnerability(zone)
    access_risk = calculate_access_risk(zone)

    priority_score = (
    0.35 * zone["damage_score"] +
    0.25 * vulnerability +
    0.2 * access_risk +
    0.2 * time_urgency
)

    return round(priority_score, 3)
