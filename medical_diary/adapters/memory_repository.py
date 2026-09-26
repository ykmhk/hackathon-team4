from werkzeug.security import generate_password_hash

from medical_diary.adapters.repository import AbstractRepository
from medical_diary.domainmodel.user import User
from medical_diary.domainmodel.record import MedicalRecord


class MemoryRepository(AbstractRepository):
    """A simple in-memory repository. Data resets whenever the app restarts."""

    def __init__(self):
        self.__users = {}
        self.__records = {}

    # --- users -----------------------------------------------------
    def add_user(self, user: User):
        self.__users[user.username] = user

    def get_user(self, username: str):
        return self.__users.get(username)

    # --- records -----------------------------------------------------
    def add_record(self, record: MedicalRecord):
        self.__records[record.id] = record

    def get_record(self, record_id: str):
        return self.__records.get(record_id)

    def get_records_for_user(self, username: str):
        records = [r for r in self.__records.values() if r.owner_username == username]
        return sorted(records, key=lambda r: r.date, reverse=True)


def populate(repo: MemoryRepository):
    """Seed the repository with a demo account and a short medical history,
    so the app has something to show as soon as it starts."""

    demo = User(
        username="demo",
        password_hash=generate_password_hash("demo1234"),
        full_name="Alex Morgan",
        date_of_birth="1998-04-12",
    )
    demo.provider_name = "Auckland City Medical Centre"
    demo.provider_address = "12 Grafton Road, Auckland 1010"
    demo.provider_email = "clinic@example.co.nz"
    demo.provider_phone = "+64 9 000 0000"
    demo.provider_hours = "Monday-Friday, 8:00 AM-5:00 PM"
    demo.gp_name = "Dr. Priya Nair"
    demo.gp_practice = "Auckland City Medical Centre"
    demo.gp_email = "p.nair@example.co.nz"
    demo.gp_phone = "+64 9 000 0001"
    repo.add_user(demo)

    seed_records = [
        ("2026-09-26", "Seasonal allergic rhinitis", "Cetirizine 10 mg once daily",
         "Symptoms should improve within several days. Avoid known allergens and "
         "return for another consultation if symptoms worsen."),
        ("2026-09-18", "Mild ankle sprain (left)", "Ibuprofen 400 mg as needed",
         "RICE protocol advised: rest, ice, compression, elevation. Reassess in "
         "two weeks if swelling persists."),
        ("2026-09-03", "Annual check-up", "None",
         "Bloods normal, blood pressure 118/76. No concerns raised."),
        ("2026-08-21", "Tension headache", "Paracetamol 500 mg as needed",
         "Likely related to screen time and posture. Suggested short breaks "
         "every hour and follow-up if headaches become frequent."),
        ("2026-07-14", "Influenza (Type A)", "Rest, fluids, paracetamol",
         "Advised five days off study/work. Return if fever persists beyond "
         "72 hours."),
    ]
    for date, diagnosis, prescription, comments in seed_records:
        repo.add_record(MedicalRecord(demo.username, date, diagnosis, prescription, comments))
