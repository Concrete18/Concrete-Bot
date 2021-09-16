from discord.ext import commands
import discord as ds
from functions import *
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
    async def rps(self, ctx, player_move):
        '''
        Rock Paper Scissors Game.
        '''
        if player_move.lower() in ['spock', 'lizard']:
            await ctx.channel.send('We only play with Rock, Paper and Scissors here.')
            return
        if player_move.lower() not in ['rock', 'paper', 'scissors']:
            await ctx.channel.send('Invalid gesture, please use Rock, Paper or Scissors.')
            return
        # player
        player_name = ctx.author.display_name
        player_move = player_move.title()
        # bot
        bot_name = self.bot.bot_name
        cpu_move = random.choice(['Rock', 'Scissors', 'Paper'])
        # result check
        cpu_win = f'{cpu_move} beats {player_move}\nI win!'
        cpu_lose = f'{player_move} beats {cpu_move}.\nI lose...'
        result = ''
        if cpu_move == player_move:
            result = 'We tied.'
        elif cpu_move == 'Rock' and player_move == 'Scissors':
            result = cpu_win
        elif cpu_move == 'Scissors' and player_move == 'Paper':
            result = cpu_win
        elif cpu_move == 'Paper' and player_move == 'Rock':
            result = cpu_win
        else:
            result = cpu_lose
        # shows results via embed
        embed = ds.Embed(
            title='Rock Paper Scissors',
            description=f'Match results between {bot_name} and {player_name}',
            colour=ds.Colour(0xf1c40f))
        embed.add_field(name=f'{bot_name} Played', value=f'{cpu_move}', inline=True)
        embed.add_field(name=f'{player_name} Played', value=f'{player_move}', inline=True)
        embed.add_field(name='Winner', value=result, inline=False)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
