import datetime as dt


def year(request):
    """Adds a variable with the current year to the template."""
    now_year = dt.datetime.now().year
    return {
        'year': now_year
    }
