import pytest

from restaurant.utils import convert_seconds_to_hours


@pytest.mark.parametrize("input_val,expected_result",
                         [(11 * 3600 + 15 * 60, "11:15 AM"), (64800, "6 PM"), (12 * 3600 + 5, "12:00:05 PM")])
def test_convert_seconds_to_hour(input_val, expected_result):
    assert convert_seconds_to_hours(input_val) == expected_result
