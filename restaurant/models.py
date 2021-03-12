from dataclasses import dataclass, field
from typing import List
from dacite import from_dict, exceptions
from .utils import convert_seconds_to_hours


@dataclass
class TimeInfo:
    type: str = ""
    value: int = -1

    def check_value_within_limit(self) -> None:
        if self.value > 86399:
            # pass
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
    try:
        opening_hours_obj = from_dict(data_class=OpeningHours, data=data)
        return opening_hours_obj
    except exceptions.WrongTypeError as e:
        raise ValueError(e.__str__())
