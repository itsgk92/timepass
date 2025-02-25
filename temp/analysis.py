import json
import time

import utils
from exchanges import nse_queries
from exchanges.nse_queries import NSEIndeces
from ta.patterns_identifier import CandlePatterns
from utils import UnderlyingType

#today = datetime.datetime.strptime("10-JUN-2024", "%d-%b-%Y")
today = utils.Today
five_sessions_ago = utils.compute_date_from_reference(today, trading_sessions=10)
print(today, five_sessions_ago)

stocks_list = nse_queries.get_index_constituents(NSEIndeces.NIFTY500)
print(f"Analyzing {len(stocks_list)} stocks")
stocks_identified_count = 0

stocks_identified = {
    CandlePatterns.BullishEngulfing.value: [],
CandlePatterns.ThreeWhiteSoldiers.value: []
}

for stock in stocks_list:

    print(f"analyzing {stock}")
    is_pattern_identified = False

    price_history_df = None
    time.sleep(.5)
    price_history_df = nse_queries.get_price_history(stock, UnderlyingType.EQ, five_sessions_ago, today)
    if price_history_df is None:
        continue
    c_open = price_history_df.OPEN
    close = price_history_df.CLOSE
    high = price_history_df.HIGH
    low = price_history_df.LOW

    for pattern_name, pattern_calculator in backend.ta.patterns_identifier.bullish_computers.items():
        price_history_df[pattern_name] = pattern_calculator(c_open, high, low, close)

    price_history_df["DATE"] = price_history_df["DATE"].dt.strftime('%Y-%m-%d')
    BullishEngulfing = price_history_df.loc[price_history_df[CandlePatterns.BullishEngulfing.value] > 0]
    if len(BullishEngulfing) != 0:
         is_pattern_identified = True
         stocks_identified[CandlePatterns.BullishEngulfing.value].append((BullishEngulfing["DATE"].tolist(), stock))
         print(CandlePatterns.BullishEngulfing.value, BullishEngulfing["DATE"].tolist(), stock)

    ThreeWhiteSoldiers = price_history_df.loc[price_history_df[CandlePatterns.ThreeWhiteSoldiers.value] > 0]
    if len(ThreeWhiteSoldiers)  != 0:
        is_pattern_identified = True
        stocks_identified[CandlePatterns.ThreeWhiteSoldiers.value].append((ThreeWhiteSoldiers["DATE"].tolist(), stock))
        print(CandlePatterns.ThreeWhiteSoldiers.value, ThreeWhiteSoldiers["DATE"].tolist(), stock)

    if is_pattern_identified:
        stocks_identified_count += 1


print(f"Identified {stocks_identified_count}: {json.dumps(stocks_identified)}")
