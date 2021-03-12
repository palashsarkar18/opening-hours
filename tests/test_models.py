import pytest

from restaurant.models import TimeInfo, OpeningHours, \
    initialize_opening_hours


def test_define_time_info_object():
    """
    Test for mapping time content (json dict) to TimeInfo object
    """
    time_dict = {"type": "close", "value": 4950}
    time_info_obj = TimeInfo(**time_dict)
    time_info_obj.check_value_within_limit()
    expected_result = "TimeInfo(type='close', value=4950)"
    assert time_info_obj.__str__() == expected_result


def test_define_opening_hours_object():
    """
    Test for mapping json to OpenHour object
    """
    data = {"monday": [{"type": "close", "value": 3600},
                       {"type": "open", "value": 32400},
                       {"type": "open", "value": 54000},
                       {"type": "close", "value": 43200},
                       {"type": "close", "value": 72000}],
            "tuesday": [{"type": "open", "value": 32400},
                        {"type": "close", "value": 72000}],
            "wednesday": [],
            "friday": [{"type": "open", "value": 75600}],
            "saturday": [{"type": "close", "value": 7200},
                         {"type": "open", "value": 75600}],
            "sunday": [{"type": "close", "value": 7200},
                       {"type": "open", "value": 75600}]}
    opening_hours_obj = initialize_opening_hours(data)
    expected_result = OpeningHours(monday=[TimeInfo(type="close", value=3600),
                                           TimeInfo(type="open", value=32400),
                                           TimeInfo(type="open", value=54000),
                                           TimeInfo(type="close", value=43200),
                                           TimeInfo(type="close", value=72000)],
                                   tuesday=[TimeInfo(type="open", value=32400),
                                            TimeInfo(type="close", value=72000)],
                                   wednesday=[],
                                   thursday=[TimeInfo(type="", value=-1)],
                                   friday=[TimeInfo(type="open", value=75600)],
                                   saturday=[TimeInfo(type="close", value=7200),
                                             TimeInfo(type="open", value=75600)],
                                   sunday=[TimeInfo(type="close", value=7200),
                                           TimeInfo(type="open", value=75600)])
    assert opening_hours_obj == expected_result
