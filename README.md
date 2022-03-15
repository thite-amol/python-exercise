# Currency exchange lib

## Problem statement
Currency conversion is one of the basic operations in the finance field - first step in any data transformation is normalizing the currency of the data to be processed. This library uses statistical data warehouse to consume currency exchange data and provide exchange rate for targeted curency.

## How to use it
### Production setup
1. Create and activate python virtual environment with pyhton version >= 3.8. Please check the [Link](https://docs.python.org/3/library/venv.html) for more information
2. Install packages by executing command `pip install -r requirements.txt`

### Available methods
1. `get_data(identifier, target_currency)` This method provides the curency echange data if target currancy is provided otherwise return raw data
2. `get_raw_data(self, identifier` Provides raw currency data
3. `get_exchange_rate(source, target)` Provides exchange data for the targeted currency

### Usage example
```
    obj = Currency()
    exchange_data = obj.get_exchange_rate("GBP")
```
This will generate below result

| TIME_PERIOD   |  OBS_value    |
| ------------- |--------------:|
| 1999-01       | 0.702913      |
| 1999-02       | 0.688505      |

```
    obj = Currency()
    raw_data = obj.get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
```
This will generate below result

| TIME_PERIOD   |  OBS_value    |
| ------------- |--------------:|
| 1999-01       | 1427.666667   |
| 1999-02       | 379.666667    |


```
    obj = Currency()
    converted_data = obj.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")
```
This will generate below result

| TIME_PERIOD   |  OBS_value    |
| ------------- |--------------:|
| 1999-01       | 1003.52546    |
| 1999-02       | 261.402399    |



### Development server setup
1. Create and activate python virtual environment with pyhton version >= 3.8. Please check the [Link](https://docs.python.org/3/library/venv.html) for more information
2. Install packages by executing command `pip install -r requirements-dev.txt`
3. Install Precommit hooks `pip install pre-commit && pre-commit install && pre-commit install --install-hooks`
