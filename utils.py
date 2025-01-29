import datetime
import dateutil.relativedelta
import enum


class UnderlyingType(enum.Enum):
    EQ = 1
    Index = 2


def get_volatility_cone_windows(underlying_type: UnderlyingType):
    if underlying_type == UnderlyingType.EQ:
        return [5, 10, 20, 30, 45, 60, 90]
    elif underlying_type == UnderlyingType.Index:
        return [3, 6, 10, 20, 30, 60]


def compute_date_from_reference(reference_date: datetime, months: int = 0, days: int = 0) -> datetime:
    return reference_date + dateutil.relativedelta.relativedelta(months=months, days=days)


def date_to_ddmmyyyy(date: datetime) -> str:
    return date.strftime("%d-%m-%Y")


def date_to_ddMMMyyyy(date: datetime) -> str:
    return date.strftime("%d-%b-%Y")

