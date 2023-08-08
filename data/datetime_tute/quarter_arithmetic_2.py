from datetime import datetime, timedelta

def get_month_ends(start_date, end_date):
    quarter_ends = []
    current_date = start_date.replace(day=1)
    while current_date <= end_date:
        current_month = current_date.month
        current_year = current_date.year
        if current_month == 12:
            next_month = 1
            next_year = current_year + 1
        else:
            next_month = current_month + 1
            next_year = current_year
        next_month_start = datetime(next_year, next_month, 1)
        quarter_end = next_month_start - timedelta(days=1)
        if quarter_end > end_date:
            quarter_end = end_date
        quarter_ends.append(quarter_end)
        current_date = next_month_start
    return quarter_ends

start_date = datetime(2021, 1, 31)
end_date = datetime(2022, 12, 31)
quarter_ends = get_month_ends(start_date, end_date)
[print(i) for i in quarter_ends]

