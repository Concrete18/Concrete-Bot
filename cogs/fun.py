from discord.ext import commands
import discord as ds
from functions import *
import datetime as dt
import random


class Fun(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        self.bot_func = bot_functions()


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
                'Can you make me a Taco?',
                'Who will give me some taco bell?']
            msg = random.choice(not_tuesday)
        await ctx.send(msg)


    @commands.command(
        name='hello',
        brief='Greets Bot and causes the bot to greet you.',
        description='Greets Bot and causes the bot to greet you.',
        aliases=['hi', 'hey'])
    async def say_hello(self, ctx):
        hello = ('Hello', 'Hi', 'Hey', 'Greetings', 'Hi there')
        san = ('', '-san')
        await ctx.send(f'{random.choice(hello)} {ctx.author.mention}{random.choices(san, weights=(60, 25))[0]}!')


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
            self.bot.logger.info(f'{ctx.author} flipped a coin onto it\'s side.')
        elif (result % 2) == 0:
            msg = 'It landed on Heads.'
        else:
            msg = 'It landed on Tails.'
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Fun(bot))
