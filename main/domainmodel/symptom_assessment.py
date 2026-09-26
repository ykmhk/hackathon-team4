class SymptomAssessment:

    def __init__(
        self,
        symptoms: list,
        duration: str,
        progress: str,
        previous_experience: bool,
        medications: str,
        medical_conditions: str,
        family_history: str,
        additional_information: str
    ):
        if not isinstance(symptoms, list):
            raise ValueError("Symptoms should be a list.")
        self.__symptoms = symptoms

        if not isinstance(duration, str) or duration.strip() == '':
            raise ValueError("Duration should be a non-empty string.")
        self.__duration = duration.strip()

        if not isinstance(progress, str) or progress.strip() == '':
            raise ValueError("Progress should be a non-empty string.")
        self.__progress = progress.strip()

        if not isinstance(previous_experience, bool):
            raise ValueError(
                "Previous experience should be a boolean."
            )
        self.__previous_experience = previous_experience

        if not isinstance(medications, str):
            raise ValueError("Medications should be a string.")
        self.__medications = medications.strip()

        if not isinstance(medical_conditions, str):
            raise ValueError(
                "Medical conditions should be a string."
            )
        self.__medical_conditions = medical_conditions.strip()

        if not isinstance(family_history, str):
            raise ValueError(
                "Family history should be a string."
            )
        self.__family_history = family_history.strip()

        if not isinstance(additional_information, str):
            raise ValueError(
                "Additional information should be a string."
            )
        self.__additional_information = (
            additional_information.strip()
        )

        self.__ai_result = None

    @property
    def symptoms(self) -> list:
        return self.__symptoms

    @property
    def duration(self) -> str:
        return self.__duration

    @property
    def progress(self) -> str:
        return self.__progress

    @property
    def previous_experience(self) -> bool:
        return self.__previous_experience

    @property
    def medications(self) -> str:
        return self.__medications

    @property
    def medical_conditions(self) -> str:
        return self.__medical_conditions

    @property
    def family_history(self) -> str:
        return self.__family_history

    @property
    def additional_information(self) -> str:
        return self.__additional_information

    @property
    def ai_result(self):
        return self.__ai_result

    def set_ai_result(self, ai_result):
        self.__ai_result = ai_result

    def __repr__(self):
        return (
            f'<SymptomAssessment: '
            f'{len(self.symptoms)} symptoms>'
        )