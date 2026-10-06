import numpy as np
from sklearn.ensemble import IsolationForest


def build_incident_features(incidents):
    """
    Convert existing incident reports into numerical
    features for anomaly detection.
    """

    features = []

    for incident in incidents:
        description_length = len(
            incident.description or ""
        )

        features.append([
            description_length,
            incident.latitude,
            incident.longitude
        ])

    return np.array(features)


def detect_suspicious_report(
    incidents,
    new_incident
):
    """
    Detect whether a new citizen report is unusual
    compared with existing incident reports.

    This is anomaly detection, not proof that a
    report is fake.
    """

    if len(incidents) < 5:
        return {
            "classification": "INSUFFICIENT_DATA",
            "suspicion_score": 0,
            "anomaly_score": None,
            "reason": (
                "Not enough historical incident reports "
                "for reliable anomaly detection."
            )
        }

    historical_features = build_incident_features(
        incidents
    )

    model = IsolationForest(
        n_estimators=100,
        contamination=0.10,
        random_state=42
    )

    model.fit(historical_features)

    new_description_length = len(
        new_incident.description or ""
    )

    new_features = np.array([[
        new_description_length,
        new_incident.latitude,
        new_incident.longitude
    ]])

    prediction = model.predict(
        new_features
    )[0]

    anomaly_score = float(
        model.decision_function(
            new_features
        )[0]
    )

    if prediction == -1:
        classification = "SUSPICIOUS"
    else:
        classification = "NORMAL"

    suspicion_score = int(
        max(
            0,
            min(
                100,
                (0.5 - anomaly_score) * 100
            )
        )
    )

    if classification == "SUSPICIOUS":
        reason = (
            "The report contains unusual characteristics "
            "compared with existing citizen reports."
        )
    else:
        reason = (
            "The report is consistent with the existing "
            "incident-report pattern."
        )

    return {
        "classification": classification,
        "suspicion_score": suspicion_score,
        "anomaly_score": round(
            anomaly_score,
            4
        ),
        "reason": reason
    }