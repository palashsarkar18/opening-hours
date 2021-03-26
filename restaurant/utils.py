import datetime
import pytz


def convert_seconds_to_hours(ts: int) -> str:
    """
    Converts UNIX time to human readable hours (hh or hh:mm or hh:mm:ss)
    :param ts: UNIX time in milliseconds
    :return: Time in hh or hh:mm or hh:mm:ss
    """
    time_format = "%-I:%M:%S %p"
    if ts % 60 == 0:
        time_format = "%-I:%M %p"
    if ts % 3600 == 0:
        time_format = "%-I %p"
    ts_human_new = datetime.datetime.fromtimestamp(ts, pytz.utc).strftime(time_format)
    return ts_human_new
