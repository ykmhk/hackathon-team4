class AIResult:

    def __init__(
        self,
        possible_conditions: list,
        recommended_action: str,
        explanation: str
    ):
        if not isinstance(possible_conditions, list):
            raise ValueError(
                "Possible conditions should be a list."
            )
        self.__possible_conditions = possible_conditions

        if (
            not isinstance(recommended_action, str)
            or recommended_action.strip() == ''
        ):
            raise ValueError(
                "Recommended action should be a non-empty string."
            )
        self.__recommended_action = recommended_action.strip()

        if not isinstance(explanation, str):
            raise ValueError(
                "Explanation should be a string."
            )
        self.__explanation = explanation.strip()

    @property
    def possible_conditions(self) -> list:
        return self.__possible_conditions

    @property
    def recommended_action(self) -> str:
        return self.__recommended_action

    @property
    def explanation(self) -> str:
        return self.__explanation

    def __repr__(self):
        return f'<AIResult: {self.recommended_action}>'