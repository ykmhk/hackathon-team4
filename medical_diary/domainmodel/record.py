import itertools

_id_counter = itertools.count(1)


class MedicalRecord:
    """A single medical visit entry, owned by a user."""

    def __init__(self, owner_username: str, date: str, diagnosis: str,
                 prescription: str, doctor_comments: str, record_id: str = None,
                 reminder_type: str = "", reminder_datetime=None,
                 reminder_note: str = ""):
        self.id = record_id or f"record_{next(_id_counter):03d}"
        self.owner_username = owner_username
        self.date = date                      # ISO string, e.g. "2026-09-26"
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.doctor_comments = doctor_comments
        self.reminder_type = reminder_type
        self.reminder_datetime = reminder_datetime
        self.reminder_note = reminder_note

    def matches(self, keyword: str) -> bool:
        """Case-insensitive search across all visible fields."""
        keyword = (keyword or "").strip().lower()
        if not keyword:
            return True
        haystack = " ".join([
            self.date, self.diagnosis, self.prescription, self.doctor_comments
        ]).lower()
        return keyword in haystack

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "diagnosis": self.diagnosis,
            "prescription": self.prescription,
            "doctorComments": self.doctor_comments,
        }

    def __repr__(self):
        return f"<MedicalRecord {self.id} {self.date}>"

    def __eq__(self, other):
        return isinstance(other, MedicalRecord) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
