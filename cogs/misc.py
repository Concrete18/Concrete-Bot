from discord.ext import commands
import datetime as dt


class Misc(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.start_time = dt.datetime.now()


    @staticmethod
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


    @commands.command(
        name = 'ping',
        brief = 'Fetches latency in milliseconds.',
        description='Fetches latency in milliseconds.')
    async def ping(self, ctx):
        '''
        Returns current ping to bot server.
        '''
        await ctx.send(f'Current Ping: {round(self.bot.latency * 1000)}ms')


    @commands.command(
        name = 'uptime',
        brief = 'Gets Bot uptime.',
        description='Gets the Bot uptime since it last was started.')
    async def uptime(self, ctx):
        '''
        Sends the total time the bot has been running using the readable_time_since function.
        '''
        uptime_seconds = dt.datetime.now().timestamp()-self.start_time.timestamp()
        await ctx.send(f'Bot Uptime: {self.readable_time_since(uptime_seconds)}')


    # wip commands


    @commands.command(
        name = 'roles',
        brief = 'Shows all roles that can be given with giverole command.',
        description='Shows all roles that can be given with giverole command.',
        hidden=True)
    async def roles(self, ctx):
        '''
        TODO add roles function
        '''
        blacklist = ['Owner', 'Admin']
        all_roles = ctx.guild.roles
        for role in all_roles:
            if role.id not in blacklist:
                print(self.bot.get_role(role.id))
        # available_roles = ' ,'.join(all_roles)
        # print(available_roles)
        # await ctx.send(f'Available Roles:\n{available_roles}')


    @commands.command(
        name = 'addrole',
        aliases=['giverole'],
        brief = 'Gives chosen role.',
        description='Gives chosen role if it is one of possible roles. To view roles use /roles command',
        hidden=True)
    async def giverole(self, ctx, time, *args):
        '''
        TODO add addrole and remove function
        '''
        msg = ' '.join(args)
        await ctx.send(f'Sheduled Message for {time}')


    @commands.command(
        name = 'schedulemsg',
        brief = 'Shedule a message to be sent at a specific time.',
        description='Shecule a message to be sent at a specific time in the channel the command was typed in.',
        hidden=True)
    async def schedulemsg(self, ctx, time, *args):
        '''
        TODO add Shedule a message function
        '''
        msg = ' '.join(args)
        await ctx.send(f'Sheduled Message for {time}')


    @commands.command(
        name = 'serverstatus',
        brief = 'WIP Get server status of Rob\'s server.',
        hidden=True)
    async def vote(self, ctx):
        '''
        TODO add server status function
        '''
        status = 'Unknown'
        await ctx.send(f'Server Status: {status}')


    @commands.command(
        name = 'vote',
        brief = 'WIP | Voting system.',
        hidden=True)
    async def vote(self, ctx):
        '''
        TODO add voting command
        '''
        await ctx.send(f'Starting Vote. WIP')


def setup(bot):
    bot.add_cog(Misc(bot))
