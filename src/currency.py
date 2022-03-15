import typing as t

import pandas as pd
import requests
from lxml import etree


class Currency:
    def __init__(self):
        self.domain = "https://sdw-wsrest.ecb.europa.eu/service/data/"

    def get_exchange_rate(self, source: str, target: str = "EUR") -> pd.DataFrame:
        """
        Function to fetch the exchange rate data from the API and convert it to a pandas
        DataFrame, with columns TIME_PERIOD and OBS_VALUE, corresponding to values of
        generic:ObsDimension and generic:ObsValue tags from the XML.

        Parameters
        ----------
         source : str
            source currency name
         target : str
            target currency name

        Returns
        -------
        pd.DataFrame
            pandas dataframe with TIME_PERIOD and OBS_VALUE column

        """
        data_url = self.domain + f"EXR/M.{source}.{target}.SP00.A?detail=dataonly"
        r = requests.get(data_url)

        # @TODO exception handling with test cases
        data = None
        if r.status_code == 200:
            data = self.parse_xml(r.content)

        df = pd.DataFrame.from_dict(data)
        df = df.astype({"OBS_VALUE": float})

        return df

    def get_raw_data(self, identifier: str) -> pd.DataFrame:
        """
        Function to fetch the currency rate data from the API and convert it to a pandas DataFrame.

        Parameters
        ----------
         identifier : str
            currency identifier string example "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"

        Returns
        -------
        pd.DataFrame
            pandas dataframe with TIME_PERIOD and OBS_VALUE column

        """
        data_url = self.domain + f"BP6/{identifier}?detail=dataonly"

        data = None
        r = requests.get(data_url)

        if r.status_code == 200:
            data = self.parse_xml(r.content)

        df = pd.DataFrame.from_dict(data)

        # change to numpy float
        df = df.astype({"OBS_VALUE": float})

        return df

    def get_data(self, identifier: str, target_currency: t.Optional[str] = None) -> pd.DataFrame:
        """
        This method provides currency price with/without exchange rate. if the target currency is None
        then this method will return raw values.
        Parameters
        ----------
         identifier : str
            currency identifier string example "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"
         target_currency : str
            target currency name

        Returns
        -------
        pd.DataFrame
            pandas dataframe with TIME_PERIOD and OBS_VALUE column
        """

        raw_data = self.get_raw_data(identifier)

        if target_currency is None:
            return raw_data

        # get the source currency
        identifiers = str(identifier).split(".")
        exchange_rate = self.get_exchange_rate(target_currency, identifiers[12])

        # left join
        raw_data["OBS_VALUE"] *= raw_data["TIME_PERIOD"].map(exchange_rate.set_index("TIME_PERIOD")["OBS_VALUE"])

        return raw_data

    @staticmethod
    def parse_xml(xml_data: str) -> dict:
        """
        This method provides currency price with/without exchange rate. if the target currency is None
        then this method will return raw values.
        Parameters
        ----------
         xml_data : str
            XML data to parse

        Returns
        -------
        dict
            dictionary with  TIME_PERIOD and OBS_VALUE index
        """

        # @TODO exception handling with test cases
        xtree = etree.XML(xml_data)

        obs_dimension = xtree.xpath(
            "/message:GenericData/message:DataSet/generic:Series/generic:Obs/generic:ObsDimension/@value",
            namespaces=xtree.nsmap,
        )
        obs_values = xtree.xpath(
            "/message:GenericData/message:DataSet/generic:Series/generic:Obs/generic:ObsValue/@value",
            namespaces=xtree.nsmap,
        )

        # ordered dictionary
        return {"TIME_PERIOD": obs_dimension, "OBS_VALUE": obs_values}


if __name__ == "__main__":
    obj = Currency()
    #     # data = obj.get_exchange_rate("GBP")
    #     # data = obj.get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
    #     # obj.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")
    data = obj.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")
