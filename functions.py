def readable_time_since(seconds):
    '''
    Returns time since based on seconds argument in the unit of time that makes the most sense
    rounded to 1 decimal place.
    '''
    seconds_in_minute = 60
    seconds_in_hour = 3600
    seconds_in_day = 86400
    seconds_in_month = 2628288
    seconds_in_year = 3.154e+7
    # minutes
    if seconds < seconds_in_hour:
        minutes = round(seconds / seconds_in_minute, 1)
        return f'{minutes} minutes'
    # hours
    elif seconds < seconds_in_day:
        hours = round(seconds / seconds_in_hour, 1)
        return f'{hours} hours'
    # days
    elif  seconds < seconds_in_month:
        days = round(seconds / seconds_in_day, 1)
        return f'{days} days'
    # months
    elif seconds < seconds_in_year:
        months = round(seconds / seconds_in_month, 1)
        return f'{months} months'
    # years
    else:
        years = round(seconds / seconds_in_year, 1)
        return f'{years} years'
