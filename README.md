## Restaurant's Opening Hours

### Introduction
The purpose of this project is to build an HTTP API that takes a restaurant's opening hours in a specific JSON structure
and converts the hours to a human-readable format.

### Setup
* Clone the project. Note that the python version is 3.8.2.
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