import datetime
import dateutil.relativedelta
import enum


class UnderlyingType(enum.Enum):
    EQ = 1
    Index = 2


def compute_date_from_reference(reference_date: datetime, months: int) -> datetime:
    return reference_date + dateutil.relativedelta.relativedelta(months=months)


def date_to_ddmmyyyy(date: datetime) -> str:
    return date.strftime("%d-%m-%Y")


def date_to_ddMMMyyyy(date: datetime) -> str:
    return date.strftime("%d-%b-%Y")

