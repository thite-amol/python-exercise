from pathlib import Path
from unittest import mock

import pytest
from requests.models import Response

from tests.test_data.config import DATA_FOLDER


def mocked_exchange_data(*args, **kwargs):
    path = Path(DATA_FOLDER + "/gbp_eur_exchange")

    with open(path, "rb") as f:
        xml_data = f.read()

    response = Response()
    response.status_code = 200
    response._content = xml_data

    return response


def mocked_identifier_data(*args, **kwargs):
    path = Path(DATA_FOLDER + "/identifier_data")

    with open(path, "rb") as f:
        xml_data = f.read()

    response = Response()
    response.status_code = 200
    response._content = xml_data

    return response


@mock.patch("requests.get", side_effect=mocked_exchange_data)
def test_get_exchange_rate(mocked_get, currency_class):
    data = currency_class.get_exchange_rate("GBP")

    assert data.loc[data["TIME_PERIOD"] == "1999-01", "OBS_VALUE"].values[0] == 0.7029125
    assert data.loc[data["TIME_PERIOD"] == "2022-01", "OBS_VALUE"].values[0] == 0.83503380952381


@mock.patch("requests.get", side_effect=mocked_identifier_data)
def test_get_raw_data(mocked_get, currency_class):
    data = currency_class.get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")

    assert data.loc[data["TIME_PERIOD"] == "1999-01", "OBS_VALUE"].values[0] == 1427.66666666667


@pytest.mark.parametrize(
    "identifier,target_currency,expected_result",
    [
        pytest.param("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", None, 1427.66666666667),
        pytest.param("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP", 1003.5247458333357),
    ],
)
def test_get_data(
    mocker, currency_class, exchange_data, identifier_data, identifier, target_currency, expected_result
):
    mocker.patch.object(currency_class, "get_exchange_rate", return_value=exchange_data)

    mocker.patch.object(currency_class, "get_raw_data", return_value=identifier_data)

    data = currency_class.get_data(identifier, target_currency)
    assert data.loc[data["TIME_PERIOD"] == "1999-01", "OBS_VALUE"].iloc[0] == expected_result
