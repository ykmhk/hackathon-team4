class Symptom:

    def __init__(self, name: str, category: str):
        if not isinstance(name, str) or name.strip() == '':
            raise ValueError("Symptom name should be a non-empty string.")
        self.__name = name.strip()

        if not isinstance(category, str) or category.strip() == '':
            raise ValueError(
                "Symptom category should be a non-empty string."
            )
        self.__category = category.strip()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def category(self) -> str:
        return self.__category

    def __repr__(self):
        return f'<Symptom {self.name}>'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Symptom):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)