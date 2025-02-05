class CandleStick:
    def __init__(self, data: dict):
        self.open = data["open"]
        self.close = data["close"]
        self.high = data["high"]
        self.low = data["low"]
        self.volume = data["volume"]
        self.date = data["date"]
        self.length = self.high - self.low
        self.bodyLength = abs(self.open - self.close)
        self.lowerWick = self.__get_lower_wick_length()
        self.upperWick = self.__get_upper_wick_length()

    def __repr__(self):
        return (f"CandleStick(open={self.open}, close={self.close},"
                f" high={self.high}, low={self.low}, volume={self.volume}")

    def is_bullish(self):
        return self.open < self.close

    def is_bearish(self):
        return self.open > self.close

    def __get_lower_wick_length(self):
        """Calculate and return the length of lower shadow or wick."""
        return (self.open if self.open <= self.close else self.close) - self.low

    def __get_upper_wick_length(self):
        """Calculate and return the length of upper shadow or wick."""
        return self.high - (self.open if self.open >= self.close else self.close)
    """
    https: // blog.stackademic.com / a - guide - to - identifying - candlestick - patterns - in -python - using - ta - lib - and -custom - formulas - 1
    b6ff4b0670f
    """