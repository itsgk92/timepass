import talib

op = df['CH_OPENING_PRICE'].astype(float)
hi = df['CH_TRADE_HIGH_PRICE'].astype(float)
lo = df['CH_TRADE_LOW_PRICE'].astype(float)
cl = df['CH_CLOSING_PRICE'].astype(float)

df['DOJI'] = talib.CDLDOJI(op, hi, lo, cl)