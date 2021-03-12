import datetime
import pytz


def convert_seconds_to_hours(ts: int) -> str:
    """
    Converts UNIX time to human readable hours (hh or hh:mm)
    :param ts: UNIX time in milliseconds
    :return: Time in hh or hh:mm
    """
    ts_human = datetime.datetime.fromtimestamp(ts, pytz.utc)
    hours = ts_human.hour
    minutes = ts_human.minute
    if hours > 12:
        hours = hours - 12
        am_pm = "PM"
    elif hours < 12:
        am_pm = "AM"
    else:
        am_pm = "Noon"
    if minutes == 0:
        return f"{hours} {am_pm}"
    else:
        return f"{hours}:{minutes} {am_pm}"
