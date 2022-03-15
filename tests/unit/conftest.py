from pathlib import Path

import pytest

from src.currency import Currency
from tests.test_data.config import DATA_FOLDER


@pytest.fixture
def currency_class():
    currency = Currency()
    yield currency


@pytest.fixture
def exchange_data():
    path = Path(DATA_FOLDER + "/gbp_eur_exchange")

    with open(path, "rb") as f:
        xml_data = f.read()

    yield xml_data


@pytest.fixture
def identifier_data():
    path = Path(DATA_FOLDER + "/identifier_data")

    with open(path, "rb") as f:
        xml_data = f.read()

    yield xml_data
