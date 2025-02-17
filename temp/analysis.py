import datetime
import time

import ta.patterns_identifier
import utils
from exchanges import nse_queries
from exchanges.nse_queries import NSEIndeces
from utils import UnderlyingType
import numpy as np

#today = datetime.datetime.strptime("10-JUN-2024", "%d-%b-%Y")
today = utils.Today
five_sessions_ago = utils.compute_date_from_reference(today, trading_sessions=5)
print(today, five_sessions_ago)

nifty_50_stocks = nse_queries.get_index_constituents(NSEIndeces.NIFTY100)
print(len(nifty_50_stocks))
i = 0
for stock in nifty_50_stocks:
    time.sleep(1)
    five_day_history = nse_queries.get_price_history(stock , UnderlyingType.EQ, five_sessions_ago, today)
    c_open = five_day_history.OPEN
    close = five_day_history.CLOSE
    high = five_day_history.HIGH
    low = five_day_history.LOW

    for reversal_pattern in ta.patterns_identifier.bullish_reversal.values():
        pattern = reversal_pattern(c_open, high, low, close)
        out = pattern.sum()
        if out != 0:
            i+=1
            print(str(reversal_pattern), stock, out)

print(i)
