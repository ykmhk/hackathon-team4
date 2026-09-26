from datetime import datetime, timedelta

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
                doctor_comments: str, repo, reminder_type: str = "",
                reminder_datetime=None, reminder_note: str = "") -> MedicalRecord:
    if not date or not diagnosis:
        raise InvalidRecordException("A date and diagnosis are required.")

    record = MedicalRecord(
        owner_username=username,
        date=date,
        diagnosis=diagnosis.strip(),
        prescription=prescription.strip(),
        doctor_comments=doctor_comments.strip(),
        reminder_type=reminder_type.strip(),
        reminder_datetime=reminder_datetime,
        reminder_note=reminder_note.strip(),
    )
    repo.add_record(record)
    return record


def search_records(username: str, keyword: str, repo) -> list[MedicalRecord]:
    records = get_records_for_user(username, repo)
    return [r for r in records if r.matches(keyword)]


def get_upcoming_reminders(records: list[MedicalRecord]) -> list[MedicalRecord]:
    now = datetime.now()
    future = now + timedelta(days=30)
    upcoming = []

    for record in records:
        if record.reminder_datetime is None:
            continue
        if now <= record.reminder_datetime <= future:
            upcoming.append(record)

    upcoming.sort(key=lambda record: record.reminder_datetime)
    return upcoming


def get_alert_reminders(records: list[MedicalRecord]) -> list[MedicalRecord]:
    now = datetime.now()
    soon = now + timedelta(hours=24)
    alerts = []

    for record in records:
        if record.reminder_datetime is None:
            continue
        if now <= record.reminder_datetime <= soon:
            alerts.append(record)

    alerts.sort(key=lambda record: record.reminder_datetime)
    return alerts
