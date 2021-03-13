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
    seconds = ts_human.second
    if ts >= 43200:
        am_pm = "PM"
    else:
        am_pm = "AM"
    if hours > 12:
        hours = hours - 12
    minutes_str = "0" + str(minutes) if minutes < 10 else str(minutes)
    seconds_str = "0" + str(seconds) if seconds < 10 else str(seconds)
    if minutes == 0 and seconds == 0:
        return f"{hours} {am_pm}"
    elif minutes != 0 and seconds == 0:
        return f"{hours}:{minutes_str} {am_pm}"
    elif seconds != 0:
        return f"{hours}:{minutes_str}:{seconds_str} {am_pm}"
    else:
        return f"{hours}:{minutes_str}:{seconds_str} {am_pm}"
