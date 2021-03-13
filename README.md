## Restaurant's Opening Hours

### Introduction
This project aims at building an HTTP API that takes a restaurant's opening hours in a specific JSON structure
and converts the time to a human-readable format.

### Setup
* Clone the project. Note that the python version is 3.8.2, as specified in [.python-version](.python_version) 
  file.
* Initialize development environment `source ./init-project`.
* Start the server `make run`.


### API input
Input JSON consist of keys indicating days of a week and corresponding opening hours as values. One JSON file includes data for one restaurant.
```
{
    <dayofweek>: <opening hours> 
    <dayofweek>: <opening hours> 
    ...
}
```
where,
```
<dayofweek>: monday / tuesday / wednesday / thursday / friday / saturday / sunday 
<opening hours>: an array of objects containing opening hours.
```
Each `<opening hours>` object consist of two keys:
* `type`: `open` or `close
* `value`: opening / closing time as UNIX time (1.1.1970 as a date),
e.g. 32400 = 9 AM, 37800 = 10.30 AM, max value is 86399 = 11.59:59 PM
  
An example is shown below:
```
{
    "monday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 32400},
                {"type": "open", "value": 54000},
                {"type": "close", "value": 43200},
                {"type": "close", "value": 72000},
              ],
    "tuesday": [
                {"type": "open", "value": 34200},
                {"type": "close", "value": 72000}
               ],
    "wednesday": [],
    "friday": [
                {"type": "open", "value": 75600}
              ],
    "saturday": [
                {"type": "close", "value": 7200},
                {"type": "open", "value": 75600}
                ],
    "sunday": [
                {"type": "close", "value": 7200},
                {"type": "open", "value": 75600}
              ]
}
```
  
### API output
For the above example, the output is
```
Monday: 9 AM - 12 Noon, 3 PM - 8 PM
Tuesday: 9:30 AM - 8 PM
Wednesday: Closed
Friday: 9 PM - 2 AM
Saturday: 9 PM - 2 AM
Sunday: 9 PM - 1 AM
```

### Data Structure
* A nested dataclass (class with `@dataclass` decorator), namely `OpeningHours` comprising `TimeInfo` objects, 
  is used for mapping the JSON data into a Python object.
* `dacite` module is used for the mapping purpose.
* The `TimeInfo` dataclass comprises `type` and `value` attributes, with empty string (= `""`) and -1 as default 
  values.
* The `OpeningHours` class comprises days of the week as attributes. Each day comprises list of `TimeInfo` objects.
    * If a day contains empty list, this implies the restaurant is closed on that day.
    * If a day contains on `TimeInfo` object with default values, this implies that the restaurant has no 
      information on that day.

### Test
* Run test with `pytest`
```
pytest
```
* `flake8` is used for style guide
```
python -m flake8
```
* `mypy` is used for type checking
```
pip install mypy
mypy <path to file>
```

### Curl Example
```
curl -X POST -H "Content-Type: application/json" \
-d @full_example.json \
127.0.0.1:5000/restaurant
```
Response:
```
Monday: Closed
Tuesday: 10 AM - 6 PM
Wednesday: Closed
Thursday: 10 AM - 6 PM
Friday: 10 AM - 1 AM
Saturday: 10 AM - 1 AM
Sunday: 12 PM - 9 PM
```

### Thoughts about JSON structure
Current JSON format is okay for storing and processing the JSON data. Here are my thoughts:

* Use of [dataclasses](https://docs.python.org/3.8/library/dataclasses.html) with 
  [dacite](https://pypi.org/project/dacite/) enables mapping of the specified JSON structure into a nested object.
    * `TimeInfo` Class: 
      * The `{"type": <open / close>>,"value": UNIX time}` is mapped to `TimeInfo` object.
      * `type` and `value` are of datatypes string and integer respectively to match the datatype specified in JSON.
      * The `dacite` module takes care of data type errors in JSON.
      * Default values are specified for `TimeInfo`. Reason for this is explained below
    
    * `OpeningHours` Class:
      * Days of the week defined in JSON structure is mapped to an `OpeningHours` objects.
      * The attributes are defined in the oder monday/tuesday/.../saturday/sunday. 
          * This takes care of an unordered JSON data.
          * [PEP 520](https://www.python.org/dev/peps/pep-0520/) preserves class attribute definition order.
            Hence OpeningHours' `__dict__.keys()` always provide the days in order, which helps in
            evaluating closing time after midnight.
      * Each attribute contains list of `TimeInfo` objects.
        * The JSON data with empty array for a day is translated to an empty list for that day in `OpeningHours`
          class, implying the restaurant is closed on that day. 
        * If a day is missing in the JSON data, the `OpeningHours` object is initialized with a list comprising 
          one `TimeInfo` object with default value. Hence if this condition is met on a day attribute of 
          `OpeningHours` object, the server interprets that no opening timing is provided for that day.
          
* The array of opening hours in JSON structure is easily sorted in ascending order based on its `value` in the server. 
  * The server checks if each opening time is followed by a closing time, either on the same day, 
    or the next day. Otherwise, the server produces an error message.
    
Perhaps an alternative and shorter JSON structure that might be better is this:
```
{
  "friday": [
    {
      "open": 36000
    }
  ],
  "saturday": [
    {
      "close": 3600
    },
    {
      "open": 36000
    }
  ],
  "sunday": [
    {
      "close": 3600
    },
    {
      "open": 43200
    },
    {
      "close": 75600
    }
  ]
}
```
For such structure, the `TimeInfo` class could have defined as follows
```
@dataclass
class TimeInfo:
    open: int = -1
    close: int = -1
```
A similar processing steps, as is used here, could be undertaken to convert the proposal 
JSON data to human-readable opening hours.
