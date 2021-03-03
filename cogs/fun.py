from discord.ext import commands
import discord as ds
from functions import *
import datetime as dt
import random
import json


class Fun(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        self.bot_func = bot_functions()
        # settings setup
        with open('data.json') as json_file:
            self.data = json.load(json_file)
        self.responses = self.data['responses']
        self.jojo_lines = self.data['jojo']
        self.jojo_run_cooldown = self.data['settings']['jojo_run_cooldown']
        self.last_jojo_run = dt.datetime.now()-dt.timedelta(hours=self.jojo_run_cooldown)
        # poll
        self.polls = []


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        On message reaction.
        '''
        if message.author == self.bot.user:  # Ignore messages made by the bot
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
                self.bot_func.logger.info(f'{message.author} made a jojo reference while it was on cooldown.')


    @commands.command(
        name = 'refresh',
        brief = 'Refreshes responses data',
        hidden=True)
    @commands.has_role('Owner')
    async def refresh(self, ctx):
        with open('data.json') as json_file:
            self.data = json.load(json_file)
        self.responses = self.data['responses']
        self.jojo_lines = self.data['jojo']
        await ctx.message.delete()
        print('Responses have been reloaded.')


    async def complete_poll(self, channel_id, message_id):
        message = await self.bot.get_channel(channel_id).fetch_message(message_id)
        most_voted = max(message.reactions, key=lambda r: r.count)
        await message.channel.send(f'The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!')
        self.polls.remove((message.channel.id, message.id))


    @commands.command(
        name = 'taco',
        brief='Taco',
        description='Taco',
        help='Taco',
        aliases=['givetaco', 'maketaco'])
    async def taco(self, ctx):
        '''
        Command for PathieZ
        '''
        if dt.datetime.today().weekday() == 1:
            rand_small = "{:,}".format(random.randrange(1, 8))
            rand_big = "{:,}".format(random.randrange(20000, 50000))
            is_tuesday = [
                'Fine, I will get you a taco.... What is your address. I am finding the number for delivery.',
                f'It is actually Taco Tuesday, give me {rand_small} to {rand_big} business days to find you a taco.',
                'Busy this Tuesday, ask next Tuesday',
                'Sorry, out of taco\'s. Would Nachos suffice?... Nevermind, out of those too.']
            msg = random.choice(is_tuesday)
        else:
            not_tuesday = [
                'It is not even Taco Tuesday.... Are you addicted to taco\'s or something?',
                'Taco, hahahaha',
                'Yo quiero Taco Bell!',
                'Can you make me a Taco?']
            msg = random.choice(not_tuesday)
        await ctx.send(msg)


    @commands.command(
        name='hello',
        aliases=['hi', 'Hey'])
    async def say_hello(self, ctx):
        hello = ('Hello', 'Hi', 'Hey', 'Greetings', 'Hi there')
        san = ('', '-san')
        await ctx.send(f'{random.choice(hello)} {ctx.author.mention}{random.choices(san, weights=(60, 20))[0]}!')


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
            self.bot_func.logger.info(f'{ctx.author} flipped a coin onto it\'s side.')
        elif (result % 2) == 0:
            msg = 'It landed on Heads.'
        else:
            msg = 'It landed on Tails.'
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Fun(bot))
