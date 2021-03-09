from discord.ext import commands
import discord as ds
from logging.handlers import RotatingFileHandler
import logging as lg
from functions import *
import datetime as dt
import asyncio
import random
import json
import sys
import os


class MyBot(commands.Bot):

    # Logging
    log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
    logger = lg.getLogger(__name__)
    logger.setLevel(lg.DEBUG) # Log Level
    my_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2)
    my_handler.setFormatter(log_formatter)
    logger.addHandler(my_handler)

    # var init
    start_time = dt.datetime.now()
    loaded_cogs = []

    # number ID's
    main_server = 172069829690261504
    test_server = 665031048941404201
    member_role = 377683900580888576
    admin_chan = 369644679370768385
    bot_commands_chan = 812394370849570866
    bot_commands_test_chan = 667229260976619561

    # secret_key
    with open('secret.json') as json_file:
        if sys.platform == 'win32':
            secret_key = json.load(json_file)['config']['discord_dev_key']
        else:
            secret_key = json.load(json_file)['config']['discord_key']

    def __init__(self):
        print('Starting Bot')
        super().__init__(command_prefix="/", intents=ds.Intents.all(), case_insensitive=True)


    def set_extensions(self):
        '''
        Loads all cogs by default. Can also be used to reload cogs if action is set not set to 'load'.
        '''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                location = f'cogs.{filename[:-3]}'
                if filename in self.loaded_cogs:
                    self.reload_extension(location)
                else:
                    self.load_extension(location)
                    self.loaded_cogs.append(filename)


    async def set_random_activity(self):
        '''
        Setsa random discord activity.
        Types: playing Streaming listening watching competing
        '''
        activity_names = [
            'Battle Bots', 'Transformers: Battle for Cybertron', 'Factorio', 'Shenzen I/O',
            'HAL 9000 Simulator', 'Skynet', 'The Matrix'
        ]
        activity_name = random.choice(activity_names)
        await self.change_presence(activity=ds.Activity(type = ds.ActivityType.playing, name=activity_name))


    async def send_random_greeting(self, channel):
        '''
        Sends a greeting on on_ready
        '''
        greetings = ['I am back online.', 'I seem to be up and working again.', 'Sorry about my outage.']
        greeting = random.choice(greetings)
        await channel.send(greeting)


    async def on_ready(self):
        '''
        Notifies that bot is ready and sets activity to a random topic.

        Possible activity types: playing Streaming listening watching competing
        '''
        self.set_extensions()
        print(f'{self.user} is ready.')
        if sys.platform != 'win32':
            channel_id = self.bot_commands_chan
            self.logger.info(f'Logged in as {self.user}')
        else:
            channel_id = self.bot_commands_test_chan
        channel = self.get_channel(channel_id)
        await self.send_random_greeting(channel)
        await self.set_random_activity()


    @classmethod
    async def setup(cls):
        bot = cls()
        try:
            await bot.start(bot.secret_key)
        except KeyboardInterrupt:
            # TODO check for unifinished polls or unsent scheduled msgs
            await bot.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MyBot.setup())
