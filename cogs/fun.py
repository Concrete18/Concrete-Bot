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


    @commands.command(
        name = 'rps',
        brief = 'Play Rock Paper Scissors.')
    async def rps(self, ctx, your_move):
        '''
        Rock Paper Scissors Game.
        '''
        your_move = your_move.title()
        cpu_move = random.choice(['Rock', 'Scissors', 'Paper'])
        msg = f'Bot: {cpu_move}\n{ctx.author}: {your_move}.\n'
        cpu_win = f'I win!\n{cpu_move} beats {your_move}'
        cpu_lose = f'I lose...\n{your_move} beats {cpu_move}.'
        if cpu_move == your_move:
            msg += 'We tied.'
        elif cpu_move == 'Rock' and your_move == 'Scissors':
            msg += cpu_win
        elif cpu_move == 'Scissors' and your_move == 'Paper':
            msg += cpu_win
        elif cpu_move == 'Paper' and your_move == 'Rock':
            msg += cpu_win
        else:
            msg += cpu_lose
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Fun(bot))
