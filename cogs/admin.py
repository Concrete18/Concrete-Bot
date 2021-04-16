from discord.ext import commands
import discord as ds
from logging.handlers import RotatingFileHandler
import logging as lg
from functions import *
import sys, os, tarfile

class Admin(commands.Cog):

    # error Logging
    log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
    error_logger = lg.getLogger(__name__)
    error_logger.setLevel(lg.DEBUG) # Log Level
    my_handler = RotatingFileHandler('Logs/error.log', maxBytes=5*1024*1024, backupCount=2)
    my_handler.setFormatter(log_formatter)
    error_logger.addHandler(my_handler)


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        self.bot_func = bot_functions()


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            info = f'{ctx.author.mention} is missing the required permission for the {ctx.command} command.'
            await ctx.send(info)
            self.bot.logger.info(info)
        if isinstance(error, commands.NotOwner):
            info = f'{ctx.author.mention} is not the owner. The {ctx.command} command is only usable for the owner.'
            await ctx.send(info)
            self.bot.logger.info(info)
        elif isinstance(error, commands.MissingAnyRole):
            info = f'{ctx.author.mention} has none of the required roles for the {ctx.command} command.'
            await ctx.send(info)
            self.bot.logger.info(info)
        elif isinstance(error, commands.MissingRole):
            info = f'{ctx.author.mention} is missing the required role for the {ctx.command} command.'
            await ctx.send(info)
            self.bot.logger.info(info)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('Command does not exist.')
        elif isinstance(error, TimeoutError):
            self.bot.logger.info('Internet Outage Detected')
    #     if sys.platform != 'win32':
    #         if isinstance(error, commands.BadArgument):
    #             msg = f'{ctx.command} was given incorrect argument.'
    #             await ctx.send(msg)
    #             self.error_logger.info(msg)
    #         elif isinstance(error, commands.CommandInvokeError):
    #             msg = f'{ctx.command} was given incorrect argument.'
    #             await ctx.send(msg)
    #             self.error_logger.info(msg)
    #         elif isinstance(error, commands.ModuleNotFoundError):
    #             print(str(error))
    #         else:
    #             info = f'Command: {ctx.command} | Error: {str(error)}'
    #             print(info)
    #             self.error_logger.info(info)
    #             raise(error)


    @commands.command(
        name ='purge',
        brief='Deletes n messages from newest to oldest.',
        description='Deletes n number of messages from the current channel. This only works for this with the manage messages permission.')
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, num: int=5):
        '''
        Purges n number of messages.
        '''
        # TODO add support to delete all of a specific users messages
        await ctx.channel.purge(limit=int(num) + 1)


    @commands.command(
        name = 'reload',
        brief='Reloads all cogs')
    @commands.has_guild_permissions(manage_guild=True)
    async def reload_cogs(self, ctx):
        '''
        Reloads all cogs without stopping bot.
        '''
        try:
            self.bot.set_extensions()
        except Exception as error:
            await ctx.send(error)
            await ctx.message.delete()
            return
        await ctx.message.delete()
        msg = 'Cogs have been reloaded.'
        print(msg)
        self.bot.logger.info(msg)
        await ctx.send(msg)


    @commands.command(
        name = 'speak',
        aliases=['say'],
        brief = 'Bot says what you type after the command.',
        hidden=True,
        pass_context = True)
    @commands.is_owner()
    async def speak(self, ctx, *args):
        msg = ' '.join(args)
        await ctx.message.delete()
        return await ctx.send(msg)


    @commands.command(
        name = 'changeactivity',
        aliases=['changegame'],
        brief = 'Change the bot\'s current game with an admin command.',
        pass_context = True)
    @commands.has_guild_permissions(manage_guild=True)
    async def changeactivity(self, ctx, *activity):
        '''
        Change Bot Activty.
        '''
        activity = ' '.join(activity)
        await self.bot.change_presence(activity=ds.Activity(type = ds.ActivityType.playing, name=activity))
        await ctx.message.delete()


    @commands.command(
        name ='backup',
        brief='Backs up log files and sends attaches them to a message.')
    @commands.is_owner()
    async def backup(self, ctx):
        '''
        Backs up log files and sends attaches them to a message.
        TODO finish this function
        '''
        area = ctx.message.channel
        source_dir = os.path.join(self.bot.script_dir, 'Logs')
        file_name = 'Log_Backup.tar'
        with tarfile.open(file_name, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        file = os.path.join(self.bot.script_dir, file_name)
        # await ctx.send_file(area, file, filename="Log Backup",content="Message test")
        await ctx.send(file=ds.File(file))
        os.remove(file)


    @commands.command(
        name ='pid',
        brief='Sends current bot PID.',
        description='Sends current bot PID.')
    @commands.is_owner()
    async def pid(self, ctx):
        '''
        Sends current bot PID.
        '''
        await ctx.send(f'PID: {os.getpid()}')


def setup(bot):
    bot.add_cog(Admin(bot))
