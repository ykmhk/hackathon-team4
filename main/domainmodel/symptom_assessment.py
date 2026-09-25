class SymptomAssessment:
    """Store all information provided by a user."""

    def __init__(
        self,
        symptoms,
        duration,
        progress,
        experienced_before,
        medical_history,
        family_history,
        additional_information
    ):
        self.symptoms = symptoms
        self.duration = duration
        self.progress = progress
        self.experienced_before = experienced_before
        self.medical_history = medical_history
        self.family_history = family_history
        self.additional_information = additional_information

    def __repr__(self):
        return (
            f"<SymptomAssessment "
            f"symptoms={self.symptoms}, "
            f"duration={self.duration}>"
        )