from discord.ext import commands
from logging.handlers import RotatingFileHandler
import logging as lg
import datetime as dt


class Misc(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        # Logging
        log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
        self.logger = lg.getLogger(__name__)
        self.logger.setLevel(lg.DEBUG) # Log Level
        my_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2)
        my_handler.setFormatter(log_formatter)
        self.logger.addHandler(my_handler)


    @commands.command(
        name = 'ping',
        brief = 'Fetches latency in milliseconds.',
        description='Fetches latency in milliseconds.')
    async def ping(self, ctx):
        '''
        Returns current ping to bot server.
        '''
        await ctx.send(f'Current Ping: {round(self.bot.latency * 1000)}ms')


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
