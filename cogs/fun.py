from discord.ext import commands
import discord as ds
from logging.handlers import RotatingFileHandler
import logging as lg
import datetime as dt
import random
import json


class Fun(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        # settings setup
        with open('data.json') as json_file:
            self.data = json.load(json_file)  # TODO add periodic reload of data.json
        self.responses = self.data['responses']
        self.jojo_lines = self.data['jojo']
        self.jojo_run_cooldown = self.data['settings']['jojo_run_cooldown']
        self.last_jojo_run = dt.datetime.now()-dt.timedelta(hours=self.jojo_run_cooldown)
        self.client = ds.Client()
        # Logging
        log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
        self.logger = lg.getLogger(__name__)
        self.logger.setLevel(lg.DEBUG) # Log Level
        my_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2)
        my_handler.setFormatter(log_formatter)
        self.logger.addHandler(my_handler)



    # TODO add birthday task


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        On message reaction.
        '''
        if message.author == self.client.user:  # Ignore messages made by the bot
            return
        # specific responses
        if message.content.lower() in self.responses:
            await message.channel.send(self.responses[message.content.lower()])
        # jojo refrences
        if message.content.lower() in self.jojo_lines:
            if self.last_jojo_run+dt.timedelta(hours=self.jojo_run_cooldown) <= dt.datetime.now():
                self.last_jojo_run = dt.datetime.now()
                await message.channel.send('Is that a Jojo reference?')
            else:
                print('Jojo reference detected but cooldown active.')
                self.logger.info(f'{message.author} made a jojo reference while it was on cooldown.')


    @commands.command(
        name = 'flip',
        aliases=['flipcoin'],
        brief = 'Flip a coin.',
        description='Flips a coin. Who knows what result will be.')
    async def flip(self, ctx):
        '''
        Flips a coin. Heads or Tails.
        '''
        result = random.randint(1, 6000+1)
        if result == 1:
            msg = '...... It landed on its side. There is a 1 in 6000 chance of that happening.'
            print(msg)
            self.logger.info(f'{ctx.author} flipped a coin onto it\'s side.')
        elif (result % 2) == 0:
            msg = 'It landed on Heads.'
        else:
            msg = 'It landed on Tails.'
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Fun(bot))
