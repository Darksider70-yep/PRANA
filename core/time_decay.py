# Time-based urgency

def time_urgency(hours_since_disaster):
    # Flood rescue urgency is highest in first 6 hours
    if hours_since_disaster <= 6:
        return 0.9
    elif hours_since_disaster <= 12:
        return 0.7
    elif hours_since_disaster <= 24:
        return 0.5
    else:
        return 0.3
