from demo.mock_data import ZONES
from core.scoring_engine import calculate_priority
from core.explainability import explain_zone
from core.time_decay import time_urgency
from risk.relief_recommender import recommend_relief
from demo.demo_config import ENABLE_VISION
from vision.damage_estimator import estimate_damage_from_image


def main():
    hours_since_disaster = 10
    urgency = time_urgency(hours_since_disaster)

    results = []

    for zone in ZONES:
        if ENABLE_VISION:
            zone["damage_score"] = estimate_damage_from_image(
                f"demo/images/{zone['zone_id']}.jpg"
            )
        score = calculate_priority(zone, urgency)
        explanation = explain_zone(zone, score)
        explanation["recommended_relief"] = recommend_relief(zone)
        results.append(explanation)

    results.sort(key=lambda x: x["priority_score"], reverse=True)

    print("\nPRANA — Disaster Relief Priority Assessment\n")

    for idx, zone in enumerate(results, start=1):
        print(f"#{idx} | {zone['zone_name']}")
        print(f"Priority Score: {zone['priority_score']}")
        print("Recommended Action:")
        print(f" - {zone['recommended_relief']}")
        print("Reasons:")
        for r in zone["reasons"]:
            print(f" - {r}")
        print("-" * 45)


if __name__ == "__main__":
    main()
