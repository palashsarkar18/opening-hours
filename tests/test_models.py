import pytest

from restaurant.models import TimeInfo, OpeningHours, \
    initialize_opening_hours, process_opening_hours_on_a_day, \
    convert_to_human_readable


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


def test_process_opening_hours_a_day():
    """
    Test for processing human readable opening on a Saturday
    """
    day = "saturday"
    time_info_list = [TimeInfo(type="close", value=7200),
                      TimeInfo(type="open", value=75600)]
    next_day_first_time_info = TimeInfo(type="close", value=7200)
    day_value = process_opening_hours_on_a_day(day, time_info_list, next_day_first_time_info)
    expected_value = "Saturday: 9 PM - 2 AM\n"
    assert day_value == expected_value


def test_opening_hours_human_readable():
    """
    Test for converting a json dict into human readable format
    """
    data = {"monday": [{"type": "close", "value": 3600},
                       {"type": "open", "value": 32400},
                       {"type": "open", "value": 54000},
                       {"type": "close", "value": 43200},
                       {"type": "close", "value": 72000},
                       # {"type": "close", "value": 75600}
                       ],
            "tuesday": [{"type": "open", "value": 34200},
                        {"type": "close", "value": 72000}],
            "wednesday": [],
            "friday": [{"type": "open", "value": 75600}],
            "saturday": [{"type": "close", "value": 7200},
                         {"type": "open", "value": 75600}],
            "sunday": [{"type": "close", "value": 7200},
                       {"type": "open", "value": 75600}]}
    opening_hours_obj = initialize_opening_hours(data)
    expected_result = "Monday: 9 AM - 12 PM, 3 PM - 8 PM\n" \
                      "Tuesday: 9:30 AM - 8 PM\n" \
                      "Wednesday: Closed\n" \
                      "Friday: 9 PM - 2 AM\n" \
                      "Saturday: 9 PM - 2 AM\n" \
                      "Sunday: 9 PM - 1 AM\n"
    assert convert_to_human_readable(opening_hours_obj) == expected_result


def test_opening_hours_human_readable_empty_json():
    """
    Test for calculating human readable timetable if json input is empty.
    """
    data = {}
    opening_hours_obj = initialize_opening_hours(data)
    expected_result = ""
    assert convert_to_human_readable(opening_hours_obj) == expected_result


def test_define_time_info_object_with_error():
    """
    Test for field error (typo/mistake) in TimeInfo object
    """
    time_dict = {"tyep": "close", "value": 4950}
    with pytest.raises(TypeError):
        time_info_obj = TimeInfo(**time_dict)
        time_info_obj.check_value_within_limit()


def test_define_time_info_object_with_error_value_exceed_max():
    """
    Test for error condition if value in TimeInfo object exceeds 83499
    :return:
    """
    time_dict = {"type": "close", "value": 86499}
    with pytest.raises(ValueError):
        time_info_obj = TimeInfo(**time_dict)
        time_info_obj.check_value_within_limit()
