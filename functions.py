import datetime as dt

class bot_functions:

    bot_image = 'https://raw.githubusercontent.com/Concrete18/Discord-Bots/master/Images/bot_images.JPG'


    @staticmethod
    async def split_string(ctx, string):
        '''
        Sends a split string in half if it is over 2000 characters.
        '''
        if len(string) <= 2000:
            await ctx.send(string)
        elif len(string) > 4000:
            await ctx.send('Output is too large.')
        else:
            middle = len(string)//2
            await ctx.send(string[0:middle])
            await ctx.send(string[middle:])


    @staticmethod
    def print_nonascii(string):
        encoded_string = string.encode("ascii", "ignore")
        decode_string = encoded_string.decode()
        print(decode_string)


    @staticmethod
    def readable_time_since(seconds):
        '''
        Returns time since based on seconds argument in the unit of time that makes the most sense
        rounded to 1 decimal place.
        '''
        if isinstance(seconds, dt.datetime):
            seconds = dt.datetime.now().timestamp()-seconds.timestamp()
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
