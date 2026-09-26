from medical_diary.domainmodel.record import MedicalRecord


class InvalidRecordException(Exception):
    pass


def get_records_for_user(username: str, repo) -> list[MedicalRecord]:
    return repo.get_records_for_user(username)


def get_record(record_id: str, username: str, repo) -> MedicalRecord | None:
    record = repo.get_record(record_id)
    if record is None or record.owner_username != username:
        return None
    return record


def add_record(username: str, date: str, diagnosis: str, prescription: str,
                doctor_comments: str, repo) -> MedicalRecord:
    if not date or not diagnosis:
        raise InvalidRecordException("A date and diagnosis are required.")

    record = MedicalRecord(
        owner_username=username,
        date=date,
        diagnosis=diagnosis.strip(),
        prescription=prescription.strip(),
        doctor_comments=doctor_comments.strip(),
    )
    repo.add_record(record)
    return record


def search_records(username: str, keyword: str, repo) -> list[MedicalRecord]:
    records = get_records_for_user(username, repo)
    return [r for r in records if r.matches(keyword)]
