from discord.ext import commands
import discord as ds
from functions import *
from typing import Optional
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
        await message.channel.send(f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!")
        self.polls.remove((message.channel.id, message.id))


    @commands.command(name="createpoll", aliases=["mkpoll"])
    @commands.has_permissions(manage_guild=True)
    async def create_poll(self, ctx, hours: int, question: str, *options):
        numbers = (
            "1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")
        if len(options) > 10:
            await ctx.send("You can only supply a maximum of 10 options.")
        else:
            embed = ds.Embed(title="Poll",
                        description=question,
                        colour=ctx.author.colour,
                        timestamp=dt.datetime.utcnow())
            fields = [
                ("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                    ("Instructions", "React to cast a vote!", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            message = await ctx.send(embed=embed)
            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)
            self.polls.append((message.channel.id, message.id))
            self.bot.scheduler.add_job(
                self.complete_poll, "date",
                run_date=dt.datetime.now()+dt.timedelta(seconds=hours),
                args=[message.channel.id, message.id])


    @commands.command(
        name = 'taco',
        aliases=['givetaco', 'maketaco'])
    async def taco(self, ctx):
        '''
        Command for PathieZ
        '''
        if dt.datetime.today().weekday() == 1:
            is_tuesday = [
                'Fine, I will get you a taco.... What is your address. I am finding the number for deliviery.',
                'It is actually Taco tuesday so give me 3 to 35,956 bussines days to find you a taco.'
                'Busy this Tuesday, ask next Tuesday']
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
