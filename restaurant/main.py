from flask import Flask, request, make_response
from .models import initialize_opening_hours, convert_to_human_readable

app = Flask(__name__)


@app.route("/restaurant", methods=['GET', 'POST'])
def evaluate_opening_hours():
    """
    API call for opening hours
    :return: Human-readable opening hour format with status code = 200;
    Error message with status code = 400 | 500
    """
    try:
        request_data = request.get_json()
        opening_hours = initialize_opening_hours(request_data)
        result = convert_to_human_readable(opening_hours)
        status_code = 200
        return make_response(result, status_code)
    except ValueError as e:
        status_code = 400
        return make_response(e.__str__(), status_code)
    except Exception as e:
        status_code = 500
        return make_response(e.__str__(), status_code)
