import nsepython as nse
import datetime
import pandas as pd
import numpy as np

import utils


def get_nfo_expiry_history(underlying, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    start_date = utils.date_to_ddmmyyyy(start_date)
    end_date = utils.date_to_ddmmyyyy(end_date)
    expiry_history = nse.expiry_history(underlying, start_date, end_date)
    # sort ascending
    expiry_history = pd.Series(expiry_history)
    expiry_history = expiry_history.apply(pd.to_datetime, format='%d-%b-%Y').sort_values()
    expiry_history = expiry_history.dt.strftime('%d-%b-%Y').tolist()
    return expiry_history


def get_price_history(underlying, underlying_type: utils.UnderlyingType, start_date, end_date) -> pd.DataFrame:

    df_price_history = None

    if underlying_type == utils.UnderlyingType.EQ:
        start_date = utils.date_to_ddmmyyyy(start_date)
        end_date = utils.date_to_ddmmyyyy(end_date)
        df_price_history = nse.equity_history(underlying, "EQ", start_date, end_date)

        df_price_history.rename(columns={'CH_CLOSING_PRICE': "CLOSE", "mTIMESTAMP": "DATE"}, inplace=True)


    elif underlying_type == utils.UnderlyingType.Index:
        start_date = utils.date_to_ddMMMyyyy(start_date)
        end_date = utils.date_to_ddMMMyyyy(end_date)
        df_price_history = nse.index_history("NIFTY 50", start_date, end_date)

        df_price_history.rename(columns={'HistoricalDate': "DATE"}, inplace=True)

    df_price_history["DATE"] = pd.to_datetime(df_price_history["DATE"])
    df_price_history["CLOSE"] = df_price_history["CLOSE"].astype(float)
    df_price_history.sort_values(by='DATE', ascending=True, inplace=True)
    df_price_history['DAILY_RETURN'] = (np.log(df_price_history.CLOSE / df_price_history.CLOSE.shift(1)))
    return df_price_history
