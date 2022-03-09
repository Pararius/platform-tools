from datetime import datetime, timedelta


def today(date_format: str) -> str:
    return datetime.today().strftime(date_format)


def from_dictionary(
    dictionary: dict,
    fallback_days_ago: int = 1,
    parameter: str = "date",
    date_format: str = "%Y-%m-%d",
) -> str:
    if fallback_days_ago > 0:
        fallback_value = (
            datetime.today() - timedelta(days=fallback_days_ago)
        ).strftime(date_format)
    else:
        fallback_value = today(date_format)

    return dictionary.get(parameter, fallback_value)


def get_date_list(base_date, window, date_fmt="%Y-%m-%d") -> list:
    """
    get_date_list(base_date, window, date_fmt)

    Returns a list of (2 * window + 1) calendar dates centered on base_date

    Input:
        - base_date: str
            the center date for the list, should be a atring that can be parsed to datetime object using the format in date_fmt
        - window: int
            number of days before and after base_date to include in the list
        - date_fmt: str
            a datetime compatible date format. This determines the format of the input as well as the resulting output

    Output:
        - dates: list
            a list of dates centered around base_date
    """
    base = datetime.strptime(base_date, date_fmt)

    date_list = [base + timedelta(days=x) for x in range(-window, window + 1, 1)]

    return [d.strftime(date_fmt) for d in date_list]
