from enum import Enum

import talib

class CandlePatterns(Enum):
    BullishEngulfing = "BullishEngulfing"
    InvertedHammer = "InvertedHammer"
    MorningDogiStar = "MorningDogiStar"
    ThreeWhiteSoldiers = "ThreeWhiteSoldiers"

bullish_computers = \
    {
        "Hammer": talib.CDLHAMMER,
        "MorningStar": talib.CDLMORNINGSTAR,
        CandlePatterns.MorningDogiStar.value: talib.CDLMORNINGDOJISTAR,
        CandlePatterns.InvertedHammer.value: talib.CDLINVERTEDHAMMER,
        CandlePatterns.BullishEngulfing.value: talib.CDLENGULFING,
        CandlePatterns.ThreeWhiteSoldiers.value:  talib.CDL3WHITESOLDIERS
    }

bearish = \
    {

    }
