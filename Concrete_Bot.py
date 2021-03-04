from discord.ext import commands
import discord as ds
from functions import *
import datetime as dt
import random
import json
import sys
import os


print('Starting Bot')

class MyBot(commands.Bot):


    def __init__(self):
        # secret_key
        with open('secret.json') as json_file:
            if sys.platform == 'win32':
                self.secret_key = json.load(json_file)['config']['discord_dev_key']
            else:
                self.secret_key = json.load(json_file)['config']['discord_key']

        # bot init
        self.bot_func = bot_functions()
        self.start_time = dt.datetime.now()
        self.loaded_cogs = []


    def set_extensions(self):
        '''
        Loads all cogs by default. Can also be used to reload cogs if action is set not set to 'load'.
        '''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                location = f'cogs.{filename[:-3]}'
                if filename in self.loaded_cogs:
                    bot.reload_extension(location)
                else:
                    bot.load_extension(location)
                    self.loaded_cogs.append(filename)


    @commands.has_any_role('Owner', 'Admin')
    @commands.command(
        name = 'reload',
        brief='Reloads all cogs')
    async def reload_cogs(self, ctx):
        '''
        Reloads all cogs without stopping bot.
        '''
        try:
            self.set_extensions()
        except Exception as error:
            await ctx.send(error)
            await ctx.message.delete()
            return
        await ctx.message.delete()
        msg = 'Cogs have been reloaded.'
        print(msg)
        self.bot_func.logger.info(msg)
        await ctx.send(msg)


    # TODO move to misc without having start_time change every time the cog is reloaded
    @commands.command(
        name = 'uptime',
        brief = 'Gets Bot uptime.',
        description='Gets the Bot uptime since it last was started.')
    async def uptime(self, ctx):
        '''
        Sends the total time the bot has been running using the readable_time_since function.
        '''
        uptime_seconds = dt.datetime.now().timestamp()-self.start_time.timestamp()
        await ctx.send(f'Bot Uptime: {self.bot_func.readable_time_since(uptime_seconds)}')


    async def on_ready(self):
        '''
        Notifies that bot is ready and sets activity to a random topic.

        Possible activity types: playing Streaming listening watching competing
        '''
        self.set_extensions()
        if sys.platform != 'win32':
            channel = bot.get_channel(812394370849570866)
            bot_func.logger.info(f'Logged in as {bot.user}')
        else:
            channel = bot.get_channel(667229260976619561)
        print(f'{bot.user} is ready.')
        # Sends a greeting on on_ready
        greetings = ['I am back online.', 'I seem to be up and working again.', 'Sorry about my outage.']
        greeting = random.choice(greetings)
        await channel.send(greeting)
        # sets discord activity
        # types: playing Streaming listening watching competing
        activity_names = ['Battle Bots', 'Transformers: Battle for Cybertron', 'Factorio', 'Shenzen I/O']
        activity_name = random.choice(activity_names)
        await bot.change_presence(activity=ds.Activity(type = ds.ActivityType.playing, name=activity_name))


bot = MyBot(command_prefix="!", intents=ds.Intents.all(), self_bot=False)
bot.run(bot.secret_key)
