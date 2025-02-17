from enum import Enum
from typing import List
import io

import nsepython as nse
import datetime
import pandas as pd
import numpy as np
import requests

import utils


class NSEIndeces(Enum):
    NIFTY50 = "NIFTY 50"
    NIFTY100 = "NIFTY 100"
    NIFTYMID50 = "NIFTY MIDCAP 50"


_BaseURL = "https://www.niftyindices.com/IndexConstituent/{0}"
_IndexConstituentCSV_URL = {
    NSEIndeces.NIFTY50 : _BaseURL.format("ind_nifty50list.csv"),
    NSEIndeces.NIFTY100 : _BaseURL.format("ind_nifty100list.csv"),
    NSEIndeces.NIFTYMID50 : _BaseURL.format("ind_niftymidcap50list.csv")
}

def get_nfo_expiry_history(underlying, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    start_date = utils.date_to_ddmmyyyy(start_date)
    end_date = utils.date_to_ddmmyyyy(end_date)
    expiry_history = nse.expiry_history(underlying, start_date, end_date)
    # sort ascending
    expiry_history = pd.Series(expiry_history)
    expiry_history = expiry_history.apply(pd.to_datetime, format='%d-%b-%Y').sort_values()
    expiry_history = expiry_history.dt.strftime('%d-%b-%Y').tolist()
    return expiry_history


def get_price_history(underlying: NSEIndeces or str, underlying_type: utils.UnderlyingType, start_date, end_date) -> pd.DataFrame:
    try:
        df_price_history = None

        if underlying_type == utils.UnderlyingType.EQ:
            start_date = utils.date_to_ddmmyyyy(start_date)
            end_date = utils.date_to_ddmmyyyy(end_date)
            df_price_history = nse.equity_history(underlying, "EQ", start_date, end_date)

            df_price_history.rename(columns=
                                    {
                                        "CH_CLOSING_PRICE": "CLOSE",
                                        "mTIMESTAMP": "DATE",
                                        "CH_OPENING_PRICE": "OPEN",
                                        "CH_TRADE_HIGH_PRICE": "HIGH",
                                        "CH_TRADE_LOW_PRICE": "LOW"
                                    },
                                    inplace=True)

        elif underlying_type == utils.UnderlyingType.Index:
            start_date = utils.date_to_ddMMMyyyy(start_date)
            end_date = utils.date_to_ddMMMyyyy(end_date)
            if not type(underlying) is NSEIndeces:  raise  Exception("NSEIndeces expected")
            df_price_history = nse.index_history(underlying.value, start_date, end_date)

            df_price_history.rename(columns={'HistoricalDate': "DATE"}, inplace=True)

        df_price_history["DATE"] = pd.to_datetime(df_price_history["DATE"], format="%d-%b-%Y")
        df_price_history["CLOSE"] = df_price_history["CLOSE"].astype(float)
        df_price_history.sort_values(by='DATE', ascending=True, inplace=True)
        df_price_history['DAILY_RETURN'] = (np.log(df_price_history.CLOSE / df_price_history.CLOSE.shift(1)))
        return df_price_history

    except Exception as e:
        print(f"error getting price history for {underlying}, err: {e}")


def get_index_constituents(index: NSEIndeces) -> List:
    url = _IndexConstituentCSV_URL.get(index)
    req = requests.get(url, headers=nse.niftyindices_headers)
    data = io.StringIO(req.text)
    constituents = pd.read_csv(data)
    return constituents["Symbol"].tolist()
