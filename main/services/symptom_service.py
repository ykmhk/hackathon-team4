from main.domainmodel.symptom_assessment import SymptomAssessment


VALID_DURATIONS = {
    "less_than_3_days",
    "3_7_days",
    "1_4_weeks",
    "more_than_1_month"
}

VALID_PROGRESS = {
    "better",
    "same",
    "worse"
}


def create_assessment(data):
    """Validate user input and create a SymptomAssessment."""

    symptoms = data.get("symptoms", [])

    if not symptoms:
        raise ValueError("At least one symptom must be selected.")

    duration = data.get("duration")

    if duration not in VALID_DURATIONS:
        raise ValueError("Invalid duration.")

    progress = data.get("progress")

    if progress not in VALID_PROGRESS:
        raise ValueError("Invalid symptom progress.")

    return SymptomAssessment(
        symptoms=symptoms,
        duration=duration,
        progress=progress,
        experienced_before=data.get("experienced_before"),
        medical_history=data.get("medical_history", ""),
        family_history=data.get("family_history"),
        additional_information=data.get(
            "additional_information", ""
        )
    )