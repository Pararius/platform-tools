from datetime import datetime, timedelta


def today(date_format: str) -> str:
    """
    today(date_format)

    Returns today's date in the given format

    Input:
        - date_format: str
            a datetime compatible date format

    Output:
        - date: str
            today's date in the given format
    """
    return datetime.today().strftime(date_format)


def from_dictionary(
    dictionary: dict,
    fallback_days_ago: int = 1,
    fallback_date_format: str = "%Y-%m-%d",
    key: str = "date",
) -> str:
    """
    from_dictionary(dictionary, fallback_days_ago, fallback_date_format, key)

    Returns a value from a given dictionary with the given key. If the key does not exist a fallback value is used.

    Input:
        - dictionary: dict
            the dictionary where the value should be taken from
        - fallback_days_ago: int
            if the key does not exist, this indicates the number of days to look back as a fallback value
        - fallback_date_format: str
            a datetime compatible date format. This determines the format of the fallback date
        - key: str
            they key to use to look for a value in the dictionary
    Output:
        - date: str
            a date taken from the dictionary or generated using the fallback arguments

    """
    if fallback_days_ago > 0:
        fallback_value = (
            datetime.today() - timedelta(days=fallback_days_ago)
        ).strftime(fallback_date_format)
    else:
        fallback_value = today(fallback_date_format)

    return dictionary.get(key, fallback_value)


def get_date_list(base_date, window, date_format="%Y-%m-%d") -> list:
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
    base = datetime.strptime(base_date, date_format)

    date_list = [base + timedelta(days=x) for x in range(-window, window + 1, 1)]

    return [d.strftime(date_format) for d in date_list]
