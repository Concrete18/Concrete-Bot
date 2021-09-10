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
    my_handler = RotatingFileHandler('Logs/bot.log', maxBytes=5*1024*1024, backupCount=2)
    my_handler.setFormatter(log_formatter)
    logger.addHandler(my_handler)

    # var init
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    start_time = dt.datetime.now()
    loaded_cogs = []

    # server_vars
    server_name = 'Concrete Jungle'
    first_run = 1

    # main server ID's
    main_server = 172069829690261504
    member_role = 377683900580888576
    admin_chan = 369644679370768385
    bot_commands_chan = 812394370849570866
    bot_test_chan_main = 794003088427974696
    # test server ID's
    bot_commands_test_chan = 667229260976619561
    test_server = 665031048941404201

    # secret_key
    with open('secret.json') as json_file:
        if sys.platform == 'win32':
            secret_key = json.load(json_file)['config']['discord_dev_key']
        else:
            secret_key = json.load(json_file)['config']['discord_key']


    def __init__(self):
        print('\nStarting Bot')
        super().__init__(command_prefix="/", case_insensitive=True, intents=ds.Intents.all())


    def set_extensions(self):
        '''
        Loads all cogs by default. Can also be used to reload cogs if action is set not set to 'load'.
        '''
        for file in os.scandir('./cogs'):
            if file.name.endswith('.py'):
                location = f'cogs.{file.name[:-3]}'
                if file.name in self.loaded_cogs:
                    self.reload_extension(location)
                else:
                    try:
                        self.load_extension(location)
                    except commands.ExtensionAlreadyLoaded:
                        self.logger.info(f'{location} is already loaded.')
                    except commands.ExtensionNotFound:
                        self.logger.info(f'{location} not found')
                    self.loaded_cogs.append(file.name)


    async def set_random_activity(self):
        '''
        Sets a random discord activity.
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
        greetings = ['I am back online. I bet it was another power outage.', 'Sorry about my outage.']
        greeting = random.choice(greetings)
        await channel.send(greeting)


    async def on_ready(self):
        '''
        Notifies that bot is ready and sets activity to a random topic.

        Possible activity types: playing Streaming listening watching competing
        '''
        self.set_extensions()
        print(f'Startup completed on {self.start_time.strftime("%A, %d %B, %I:%M %p")}')
        print(f'{self.user} is ready\n')
        if self.first_run:
            pass
            # WIP send message about system bing back up again
            # user = await client.get_user_info('136589810025496576')
            # await user.send('Internet or Power is back.')
            # self.first_run = 0
        else:
            print('Restarted Bot')
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
        await bot.start(bot.secret_key)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(MyBot.setup())
    except KeyboardInterrupt:
        print('\nShutting Down Concrete Bot')
