from restaurant.main import app


def test_fetch_human_readable_form():
    """
    Test API with example given in assignment
    """
    data = {
        "friday": [
            {
                "type": "open",
                "value": 64800
            }],
        "saturday": [
            {
                "type": "close",
                "value": 3600
            },
            {
                "type": "open",
                "value": 32400
            },
            {
                "type": "close",
                "value": 39600
            },
            {
                "type": "open",
                "value": 57600
            },
            {
                "type": "close", "value": 82800
            }
        ]
    }
    expected_result = "Friday: 6 PM - 1 AM\n" \
                      "Saturday: 9 AM - 11 AM, 4 PM - 11 PM\n"
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.get_data(as_text=True) == expected_result


def test_fetch_human_readable_form_full_example():
    """
    Test API with the full example provided in assignment
    """
    data = {
        "monday": [],
        "tuesday": [{"type": "open", "value": 36000},
                    {"type": "close", "value": 64800}],
        "wednesday": [],
        "thursday": [{"type": "open", "value": 36000},
                     {"type": "close", "value": 64800}],
        "friday": [{"type": "open", "value": 36000}],
        "saturday": [{"type": "close", "value": 3600},
                     {"type": "open", "value": 36000}],
        "sunday": [{"type": "close", "value": 3600},
                   {"type": "open", "value": 43200},
                   {"type": "close", "value": 75600}]
    }
    expected_result = "Monday: Closed\n" \
                      "Tuesday: 10 AM - 6 PM\n" \
                      "Wednesday: Closed\n" \
                      "Thursday: 10 AM - 6 PM\n" \
                      "Friday: 10 AM - 1 AM\n" \
                      "Saturday: 10 AM - 1 AM\n" \
                      "Sunday: 12 PM - 9 PM\n"
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.get_data(as_text=True) == expected_result


def test_fetch_human_readable_form_closed_weekend():
    """
    Test API with opening time and restaurant closed on weekend
    """
    data = {
        "monday": [{"type": "open", "value": 28800},
                   {"type": "close", "value": 61200}],
        "tuesday": [{"type": "open", "value": 28800},
                    {"type": "close", "value": 61200}],
        "wednesday": [{"type": "open", "value": 28800},
                      {"type": "close", "value": 61200}],
        "thursday": [{"type": "open", "value": 28800},
                     {"type": "close", "value": 61200}],
        "friday": [{"type": "open", "value": 28800},
                   {"type": "close", "value": 55800}],
        "saturday": [],
        "sunday": []
    }
    expected_result = "Monday: 8 AM - 5 PM\n" \
                      "Tuesday: 8 AM - 5 PM\n" \
                      "Wednesday: 8 AM - 5 PM\n" \
                      "Thursday: 8 AM - 5 PM\n" \
                      "Friday: 8 AM - 3:30 PM\n" \
                      "Saturday: Closed\n" \
                      "Sunday: Closed\n"
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.get_data(as_text=True) == expected_result


def test_fetch_human_readable_form_sunday_open_after_midnight():
    """
    Test API with opening time past Sunday
    """
    data = {
        "sunday": [
            {"type": "open", "value": 64800}
        ],
        "monday": [
            {"type": "close", "value": 7200}
        ]
    }
    expected_result = "Sunday: 6 PM - 2 AM\n"
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.get_data(as_text=True) == expected_result


def test_url_error_unix_exceeds_max_val():
    """
    Test for error condition when unix time exceeds 86399
    """
    data = {
        "monday": [{"type": "open", "value": 75600},
                   {"type": "close", "value": 86400}]
    }
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.status_code == 400
        assert response.get_data(as_text=True) == \
               "Wrong time value 86400 specified. It exceeds the maximum value."


def test_url_error_close_time_not_specified():
    """
    Test for error condition when close time not specified on that day or the next day
    """
    data = {
        "sunday": [{"type": "open", "value": 75600},
                   ],
        "tuesday": [{"type": "open", "value": 28800},
                    {"type": "close", "value": 61200}]
    }
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.status_code == 400
        assert response.get_data(as_text=True) == \
               "Expecting closing time for sunday on  the next day, " \
               "but no such closing time specified."


def test_url_error_two_consecutive_open_time():
    """
    Test for error condition when close time not specified on that day or the next day
    """
    data = {
        "friday": [{"type": "open", "value": 28800},
                   {"type": "open", "value": 61200},
                   {"type": "close", "value": 82800}]
    }
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.status_code == 400
        assert response.get_data(as_text=True) == \
               "Two consecutive open time."


def test_url_error_wrong_time_value_type():
    """
    Test API with value for Monday specified as string
    """
    data = {
        "sunday": [{"type": "open", "value": 64800}],
        "monday": [{"type": "close", "value": "7200"}]
    }
    expected_error_message = 'wrong value type for field "monday.value" - ' \
                             'should be "int" instead of value "7200" of type "str"'
    with app.test_client() as client:
        response = client.post("/restaurant",
                               json=data)
        assert response.status_code == 400
        assert response.get_data(as_text=True) == expected_error_message
