from datetime import datetime, timedelta


def parse_current_time(datetime_utc=None):
    datetime_now = datetime_utc or datetime.utcnow()

    ins_datetime = datetime_now + timedelta(hours=7)

    return ins_datetime