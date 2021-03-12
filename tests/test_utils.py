from restaurant.utils import convert_seconds_to_hours


def test_convert_seconds_to_hours_before_noon():
    """
    Test conversion of seconds to hours.
    Input is before noon, hence expecting AM
    """
    input_val = 11 * 60 * 60 + 15 * 60
    expected_result = "11:15 AM"
    result = convert_seconds_to_hours(input_val)
    assert result == expected_result


def test_convert_seconds_to_hours_after_noon():
    """
    Test conversion of seconds to hours.
    Input is before noon, hence expecting AM
    """
    input_val = 64800
    expected_result = "6 PM"
    result = convert_seconds_to_hours(input_val)
    assert result == expected_result
