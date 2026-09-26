import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from medical_diary.domainmodel.record import MedicalRecord
from medical_diary.domainmodel.user import User


def test_record_matches_keyword_in_diagnosis():
    record = MedicalRecord("demo", "2026-09-26", "Seasonal allergic rhinitis",
                            "Cetirizine 10 mg", "Avoid allergens.")
    assert record.matches("allergic")
    assert record.matches("CETIRIZINE")
    assert not record.matches("influenza")


def test_record_matches_everything_with_empty_keyword():
    record = MedicalRecord("demo", "2026-09-26", "Check-up", "None", "All clear.")
    assert record.matches("")
    assert record.matches(None)


def test_record_to_dict_contains_expected_keys():
    record = MedicalRecord("demo", "2026-09-26", "Check-up", "None", "All clear.")
    data = record.to_dict()
    assert set(data.keys()) == {"id", "date", "diagnosis", "prescription", "doctorComments"}


def test_user_equality_is_based_on_username():
    user_a = User("demo", "hash1")
    user_b = User("demo", "hash2")
    user_c = User("other", "hash1")
    assert user_a == user_b
    assert user_a != user_c
