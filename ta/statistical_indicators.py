import pandas


def compute_MAs(price_df) -> pandas.DataFrame:

    price_df["50MA"] = price_df['CLOSE'].rolling(window=50).mean()
    price_df["25MA"] = price_df['CLOSE'].rolling(window=25).mean()
    price_df["50EMA"] = price_df['CLOSE'].ewm(span=50).mean()
    price_df["15EMA"] = price_df['CLOSE'].ewm(span=15).mean()



    return price_df


