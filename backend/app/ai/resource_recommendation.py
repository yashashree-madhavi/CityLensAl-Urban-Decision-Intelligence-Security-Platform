def recommend_resources(
    emergency_type: str,
    flood_risk: str = "LOW",
    traffic_level: str = "LOW",
    incident_count: int = 0
):
    """
    Recommend emergency-response resources using
    CityLens decision-intelligence rules.
    """

    recommendations = []
    reasons = []

    emergency_type = (
        emergency_type or ""
    ).lower()

    flood_risk = (
        flood_risk or "LOW"
    ).upper()

    traffic_level = (
        traffic_level or "LOW"
    ).upper()

    # ---------------------------------
    # Emergency type
    # ---------------------------------

    if emergency_type in [
        "medical",
        "accident",
        "injury"
    ]:
        recommendations.append("AMBULANCE")
        reasons.append(
            "Medical assistance may be required"
        )

    elif emergency_type in [
        "flood",
        "waterlogging"
    ]:
        recommendations.append("RESCUE_TEAM")
        reasons.append(
            "Flood-related emergency requires rescue support"
        )

    elif emergency_type in [
        "fire"
    ]:
        recommendations.append("FIRE_BRIGADE")
        reasons.append(
            "Fire emergency requires fire-response resources"
        )

    elif emergency_type in [
        "crime",
        "security"
    ]:
        recommendations.append("POLICE_UNIT")
        reasons.append(
            "Security-related emergency requires police response"
        )

    else:
        recommendations.append("EMERGENCY_RESPONSE_TEAM")
        reasons.append(
            "General emergency response is required"
        )

    # ---------------------------------
    # Flood intelligence
    # ---------------------------------

    if flood_risk == "CRITICAL":
        recommendations.append("FLOOD_RESCUE_TEAM")
        recommendations.append("EVACUATION_SUPPORT")

        reasons.append(
            "Critical flood risk requires rescue and evacuation support"
        )

    elif flood_risk == "HIGH":
        recommendations.append("FLOOD_RESCUE_TEAM")

        reasons.append(
            "High flood risk requires additional rescue capability"
        )

    elif flood_risk == "MODERATE":
        recommendations.append("FIELD_RESPONSE_TEAM")

        reasons.append(
            "Moderate flood risk requires field monitoring"
        )

    # ---------------------------------
    # Traffic intelligence
    # ---------------------------------

    if traffic_level == "SEVERE":
        recommendations.append("TRAFFIC_CONTROL_UNIT")

        reasons.append(
            "Severe traffic congestion may delay emergency response"
        )

    elif traffic_level == "HIGH":
        recommendations.append("TRAFFIC_CONTROL_UNIT")

        reasons.append(
            "High traffic congestion may affect response time"
        )

    # ---------------------------------
    # Incident intelligence
    # ---------------------------------

    if incident_count >= 3:
        recommendations.append("ADDITIONAL_FIELD_UNITS")
        reasons.append("Multiple nearby incidents require additional field resources")

    elif incident_count > 0:
        reasons.append(
            f"{incident_count} verified or investigating incident(s) are nearby"
        )

    # ---------------------------------
    # Remove duplicates
    # ---------------------------------

    recommendations = list(
        dict.fromkeys(recommendations)
    )

    # ---------------------------------
    # Priority
    # ---------------------------------

    if flood_risk == "CRITICAL":
        priority = "CRITICAL"
    elif flood_risk == "HIGH" or traffic_level == "SEVERE":
        priority = "HIGH"
    elif (
        flood_risk == "MODERATE"
        or traffic_level == "HIGH"
        or incident_count > 0
    ):
        priority = "MODERATE"
    elif flood_risk == "UNAVAILABLE":
        priority = "DATA_LIMITED"
    else:
        priority = "NORMAL"

    return {
        "priority": priority,
        "recommended_resources": recommendations,
        "reasons": reasons
    }