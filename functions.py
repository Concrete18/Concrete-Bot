import datetime as dt


class bot_functions:

    bot_image = "https://raw.githubusercontent.com/Concrete18/Discord-Bots/master/Images/bot_images.JPG"

    @staticmethod
    def split_text(string, delimiter=" ", limit=2000):
        """
        Returns a list of strings within the set character `limit` without breaking up beyong the `delimiter` point.
        """
        # exits early if string is already within the limit.
        if len(string) <= limit:
            return [string]
        string_split = string.split(delimiter)
        messages = [[]]
        messages_index = 0
        current_len = 0
        delimiter_len = len(delimiter)
        for split in string_split:
            split_len = len(split)
            delimiters_needed = len(messages[messages_index]) * delimiter_len
            if current_len + split_len + delimiters_needed >= limit:
                messages.append([])
                messages_index += 1
                current_len = 0
            messages[messages_index].append(split)
            current_len += split_len
        return [delimiter.join(message) for message in messages]

    @staticmethod
    def print_nonascii(string):
        """
        Prints `string` without ascii.
        """
        encoded_string = string.encode("ascii", "ignore")
        decode_string = encoded_string.decode()
        print(decode_string)

    @staticmethod
    def readable_time_since(seconds):
        """
        Returns time since based on seconds argument in the unit of time that makes the most sense
        rounded to 1 decimal place.
        """
        if isinstance(seconds, dt.datetime):
            seconds = int(dt.datetime.now().timestamp() - seconds.timestamp())
        seconds_in_minute = 60
        seconds_in_hour = 3600
        seconds_in_day = 86400
        seconds_in_month = 2628288
        seconds_in_year = 3.154e7
        # minutes
        if seconds < seconds_in_hour:
            minutes = round(seconds / seconds_in_minute, 1)
            return f"{minutes} minutes"
        # hours
        elif seconds < seconds_in_day:
            hours = round(seconds / seconds_in_hour, 1)
            return f"{hours} hours"
        # days
        elif seconds < seconds_in_month:
            days = round(seconds / seconds_in_day, 1)
            return f"{days} days"
        # months
        elif seconds < seconds_in_year:
            months = round(seconds / seconds_in_month, 1)
            return f"{months} months"
        # years
        else:
            years = round(seconds / seconds_in_year, 1)
            return f"{years} years"
