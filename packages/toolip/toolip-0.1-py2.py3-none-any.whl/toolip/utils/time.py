from datetime import datetime, timezone

import pytz


def now():
    return datetime.now(timezone.utc)


def now_epoch() -> int:
    return int(datetime.now(timezone.utc).timestamp())


def now_epoch_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def make_time_aware(dtime: datetime):
    return dtime.replace(tzinfo=pytz.utc)
