from datetime import datetime, timedelta


def today() -> str:
    return datetime.today().strftime("%Y-%m-%d")


def from_request_or_use_yesterday(request_json: dict, parameter: str = "date") -> str:
    return request_json.get(
        parameter, (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    )


def get_date_list(base_date, window, date_fmt="%Y-%m-%d") -> list:
    """
    THIS FUNCTION IS DEPRECATED: import from datetime module

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
