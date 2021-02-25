from discord.ext import commands
import discord as ds
from logging.handlers import RotatingFileHandler
import logging as lg
import os

class Admin(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        # Logging
        log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
        self.logger = lg.getLogger(__name__)
        self.logger.setLevel(lg.DEBUG) # Log Level
        my_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2)
        my_handler.setFormatter(log_formatter)
        self.logger.addHandler(my_handler)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        info = f'Command: {ctx.command} | Error: {str(error)}'
        print(info)
        self.logger.debug(info)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} is missing the required permission for the {ctx.command} command.')
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'{ctx.author.mention} is missing the required role for the {ctx.command} command.')
        else:
            raise(error)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''
        Give new members the "Member" role.
        Make sure the bot role is above the role you are wanting it to assign.
        '''
        msg = f'{member} joined the server'
        print(msg)
        self.logger.info(msg)
        role = member.guild.get_role(377683900580888576)
        await member.add_roles(role, reason='New Member')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        '''
        Logs members that left the server.
        '''
        msg = f'{member} left the server'
        print(msg)
        self.logger.info(msg)


    @commands.command(
        name ='purge',
        brief='Deletes n messages from newest to oldest.',
        description='Deletes n number of messages from the current channel. This only works for this with the manage messages permission.',
        hidden=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, num: int):
        '''
        Purges n number of messages.
        '''
        # TODO add support to delete all of a specific users messages
        await ctx.channel.purge(limit=int(num) + 1)


    @commands.command(
        name = 'speak',
        aliases=['say'],
        brief = 'Bot says what you type after the command.',
        hidden=True,
        pass_context = True)
    @commands.has_role('Owner')
    async def speak(self, ctx, *args):
        msg = ' '.join(args)
        await ctx.message.delete()
        return await ctx.send(msg)


    @commands.command(
        name ='pid',
        brief='Sends current bot PID.',
        description='Sends current bot PID.',
        hidden=True)
    async def pid(self, ctx):
        '''
        Sends current bot PID.
        '''
        await ctx.send(f'PID: {os.getpid()}')


def setup(bot):
    bot.add_cog(Admin(bot))
