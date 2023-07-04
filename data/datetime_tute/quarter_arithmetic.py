import datetime


def floor_dt(dt: datetime.datetime, delta: datetime.timedelta) -> datetime.datetime:
    """
    Largest datetime less than or equal to dt and divisible by delta.

    Examples
    ------------
    >>> import datetime
    >>>
    >>> dt = datetime.datetime.utcnow(); dt
    datetime.datetime(2022, 12, 20, 3, 28, 49, 372246)
    >>> floor_dt(dt, datetime.timedelta(seconds=60))
    datetime.datetime(2022, 12, 20, 3, 28)
    >>> floor_dt(dt, datetime.timedelta(seconds=15))
    datetime.datetime(2022, 12, 20, 3, 28, 45)
    """
    return dt - (dt - datetime.datetime.min) % delta


def quarter_end_datetime(dt: datetime.datetime | datetime.date) -> datetime.datetime:
    """
    Find out earliest quarter end date or datetime strictly after the date or datetime.

    Examples
    ------------
    >>> import datetime
    >>>
    >>> dt = datetime.datetime(2022, 12, 20, 3, 29, 25, 68229)
    >>> quarter_end_datetime(dt)
    datetime.datetime(2022, 12, 31, 0, 0)
    >>> quarter_end_datetime(dt.date())
    datetime.date(2022, 12, 31)


    >>> quarter_end_datetime(dt.replace(month=3))
    datetime.datetime(2022, 3, 31, 0, 0)
    >>> quarter_end_datetime(dt.replace(month=6))
    datetime.datetime(2022, 6, 30, 0, 0)
    >>> quarter_end_datetime(dt.replace(month=9))
    datetime.datetime(2022, 9, 30, 0, 0)

    >>> quarter_end_datetime(datetime.date(2022, 1, 1))
    datetime.date(2022, 3, 31)
    >>> quarter_end_datetime(datetime.date(2022, 3, 31))
    datetime.date(2022, 3, 31)
    """
    if dt.month < 4:
        dt = dt.replace(month=3, day=31)
    elif dt.month < 7:
        dt = dt.replace(month=6, day=30)
    elif dt.month < 10:
        dt = dt.replace(month=9, day=30)
    else:
        dt = dt.replace(month=12, day=31)
    if isinstance(dt, datetime.datetime):
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt


# differences between two dates in number of quarters
def get_quarter_diff(dt1: datetime.datetime, dt2: datetime.datetime) -> int:
    """
    Examples
    ------------
    >>> import datetime
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2022, 9, 30))
    1
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2022, 6, 30))
    2
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2022, 3, 31))
    3
    >>> get_quarter_diff(datetime.datetime(2022, 12, 31), datetime.datetime(2021, 12, 31))
    4
    """
    q1 = (dt1.year - 1) * 4 + (dt1.month - 1) // 3 + 1
    q2 = (dt2.year - 1) * 4 + (dt2.month - 1) // 3 + 1
    return q1 - q2


# find 3 month earlier date if the date is last day of the month
def get_3m_earlier(dt: datetime.datetime) -> datetime.datetime:
    """
    3 month earlier date if the date is last day of the month.

    Examples
    ------------
    >>> import datetime
    >>>
    >>> get_3m_earlier(datetime.datetime(2022, 12, 31))
    datetime.datetime(2022, 9, 30, 0, 0)
    >>> get_3m_earlier(datetime.datetime(2022, 9, 30))
    datetime.datetime(2022, 6, 30, 0, 0)
    >>> get_3m_earlier(datetime.datetime(2022, 6, 30))
    datetime.datetime(2022, 3, 31, 0, 0)
    >>> get_3m_earlier(datetime.datetime(2022, 3, 31))
    datetime.datetime(2021, 12, 31, 0, 0)
    """
    dt = dt + datetime.timedelta(days=1)
    month = dt.month
    if month < 4:
        month = 12 + month - 3
    else:
        month -= 3
    dt = dt.replace(month=month)
    return dt - datetime.timedelta(days=1)


def yearquarter(dt: datetime.datetime | datetime.date) -> str:
    """
    Examples
    ------------
    >>> import datetime
    >>> dt = datetime.datetime(2022, 12, 31, 0, 1, 2, 3)
    >>> dte = dt.date()
    >>> yearquarter(dt)
    '2022 Q4'
    >>> yearquarter(dte)
    '2022 Q4'
    >>> yearquarter(datetime.date(2022,12,31) + datetime.timedelta(days=1))
    '2023 Q1'
    >>> yearquarter(datetime.date(2022,9,30) + datetime.timedelta(days=1))
    '2022 Q4'
    >>> yearquarter(datetime.date(2022,6,30) + datetime.timedelta(days=1))
    '2022 Q3'
    >>> yearquarter(datetime.date(2022,3,31) + datetime.timedelta(days=1))
    '2022 Q2'
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "dt": [datetime.datetime(2022, 12, 31, 0, 1, 2, 3),
    ...            datetime.datetime(2022, 9, 30, 0, 1, 2, 3),
    ...            datetime.datetime(2022, 6, 30, 0, 1, 2, 3),
    ...            datetime.datetime(2022, 3, 31, 0, 1, 2, 3)],
    ...     "dte": [datetime.date(2022, 12, 31),
    ...             datetime.date(2022, 9, 30),
    ...             datetime.date(2022, 6, 30),
    ...             datetime.date(2022, 3, 31)]
    ... })
    >>>
    >>> df["dte"].apply(lambda x: yearquarter(x+datetime.timedelta(days=1)))
    0    2023 Q1
    1    2022 Q4
    2    2022 Q3
    3    2022 Q2
    Name: dte, dtype: object
    >>> df["dt"].apply(lambda x: yearquarter(x+datetime.timedelta(days=1)))
    0    2023 Q1
    1    2022 Q4
    2    2022 Q3
    3    2022 Q2
    Name: dt, dtype: object
    """

    quarter_dt = quarter_end_datetime(dt)
    if isinstance(quarter_dt, datetime.datetime):
        quarter_dte = quarter_dt.date()
    else:
        quarter_dte = quarter_dt

    # to YYYY Qn format
    if quarter_dte.month == 12:
        quarter_str = f"{quarter_dte.year} Q4"
    elif quarter_dte.month == 9:
        quarter_str = f"{quarter_dte.year} Q3"
    elif quarter_dte.month == 6:
        quarter_str = f"{quarter_dte.year} Q2"
    elif quarter_dte.month == 3:
        quarter_str = f"{quarter_dte.year} Q1"
    else:
        raise ValueError(f"Invalid quarter month: {quarter_dte.month}")

    return quarter_str
