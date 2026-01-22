def time_urgency(hours_since_disaster, curve="fast"):
    """
    Returns a normalized urgency score based on time elapsed
    and disaster-specific urgency curve.
    """

    if curve == "instant":   # earthquakes
        return 1.0 if hours_since_disaster <= 6 else 0.6

    if curve == "medium":    # cyclones
        if hours_since_disaster <= 6:
            return 0.8
        elif hours_since_disaster <= 24:
            return 0.6
        else:
            return 0.4

    # fast (flood default)
    if hours_since_disaster <= 6:
        return 0.9
    elif hours_since_disaster <= 12:
        return 0.7
    elif hours_since_disaster <= 24:
        return 0.5
    else:
        return 0.3
