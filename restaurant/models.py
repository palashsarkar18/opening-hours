from dataclasses import dataclass, field
from typing import List
from dacite import from_dict, exceptions
from .utils import convert_seconds_to_hours


@dataclass
class TimeInfo:
    type: str = ""
    value: int = -1

    def check_value_within_limit(self) -> None:
        """
        Checks if 'value' field is within limit (0 to 86399), else raise an error
        """
        if self.value > 86399:
            raise ValueError(f"Wrong time value {self.value} specified. "
                             "It exceeds the maximum value.")
        elif self.value < 0:
            raise ValueError("This is a default value, implying that "
                             "this object shouldn't be processed.")

    def convert_epoch_to_human_readable(self) -> str:
        self.check_value_within_limit()
        return f"{convert_seconds_to_hours(self.value)}"


@dataclass
class OpeningHours:
    monday: List[TimeInfo] = field(default_factory=lambda: [TimeInfo()])
    tuesday: List[TimeInfo] = field(default_factory=lambda: [TimeInfo()])
    wednesday: List[TimeInfo] = field(default_factory=lambda: [TimeInfo()])
    thursday: List[TimeInfo] = field(default_factory=lambda: [TimeInfo()])
    friday: List[TimeInfo] = field(default_factory=lambda: [TimeInfo()])
    saturday: List[TimeInfo] = field(default_factory=lambda: [TimeInfo()])
    sunday: List[TimeInfo] = field(default_factory=lambda: [TimeInfo()])


def initialize_opening_hours(data: dict) -> OpeningHours:
    """
    Maps json structure to nested dataclass object
    :param data: JSON data
    :return: OpeningHours object
    """
    try:
        opening_hours_obj = from_dict(data_class=OpeningHours, data=data)
        return opening_hours_obj
    except exceptions.WrongTypeError as e:
        raise ValueError(e.__str__())


def convert_to_human_readable(opening_hours_obj: OpeningHours) -> str:
    """
    Converts the OpeningHours object to Human Readable form
    :param opening_hours_obj: OpeningHours object
    :return: Human readable string
    """
    output = ""
    days = list(opening_hours_obj.__dict__.keys())
    for index in range(0, len(days)):
        day = days[index]
        time_list = getattr(opening_hours_obj, day)
        print(f"time_list 1 : {time_list}")
        if len(time_list) == 1 and not time_list[0].type:
            pass
        elif len(time_list) == 1 and time_list[0].type == "close":
            pass
        elif len(time_list) == 0:
            output += f"{day.capitalize()}: Closed\n"
        elif index == len(days) - 1:
            output += process_opening_hours_on_a_day(day,
                                                     time_list,
                                                     getattr(opening_hours_obj,
                                                             days[0])[0])
        elif len(getattr(opening_hours_obj, days[index + 1])) == 0:
            output += process_opening_hours_on_a_day(day, time_list)
        else:
            output += process_opening_hours_on_a_day(day,
                                                     time_list,
                                                     getattr(opening_hours_obj,
                                                             days[index + 1])[0])
    return output


def process_opening_hours_on_a_day(day: str,
                                   time_list: List[TimeInfo],
                                   next_day_first_time_info: TimeInfo = None) -> str:
    """
    Processes the opening hours on a certain day
    :param day: Day of the week
    :param time_list: List of TimeInfo object on 'day'
    :param next_day_first_time_info: Firs TimeInfo object for the next day, default is None
    :return: Human readable string for the specific day
    """
    day_output = f"{day.capitalize()}:"
    time_list.sort(key=lambda timing: timing.value)
    next_expected_type = "close"
    for j in range(0, len(time_list)):
        time_obj = time_list[j]
        if j == 0 and time_obj.type == "close":
            pass
        elif time_obj.type == next_expected_type:
            raise ValueError(f"Two consecutive {time_obj.type} time.")
        elif time_obj.type == "close":
            day_output += f" - {time_obj.convert_epoch_to_human_readable()},"
            next_expected_type = time_obj.type
        elif j == len(time_list) - 1 \
                and time_list[j].type == "open" \
                and next_day_first_time_info is not None \
                and next_day_first_time_info.type == "close":
            day_output += f" {time_obj.convert_epoch_to_human_readable()} - " \
                          f"{next_day_first_time_info.convert_epoch_to_human_readable()},"
            next_expected_type = time_obj.type
        elif j == len(time_list) - 1 \
                and time_list[j].type == "open" \
                and next_day_first_time_info is None:
            raise ValueError(f"Expecting closing time for {day} on  the next day, "
                             f"but no such closing time specified.")
        elif j == len(time_list) - 1 and time_list[j].type == "open":
            raise ValueError(f"Expecting closing time for {day} on  the next day, "
                             f"but no such closing time specified.")
        elif time_obj.type == "open":
            day_output += f" {time_obj.convert_epoch_to_human_readable()}"
            next_expected_type = time_obj.type
        else:
            raise ValueError(f"Wrong type {time_obj.type} specified on {day}.")
    day_output = day_output[:-1]
    day_output += "\n"
    return day_output
