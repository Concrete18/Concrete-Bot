from logging.handlers import RotatingFileHandler
from discord import channel
from discord.ext import commands
import discord as ds
import datetime as dt
import logging as lg
import random
import sys
import os
from shared_games_finder import Shared_Games

# Logging
log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
logger = lg.getLogger(__name__)
logger.setLevel(lg.DEBUG) # Log Level
my_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2)
my_handler.setFormatter(log_formatter)
logger.addHandler(my_handler)
# passcode
with open('passcode.txt') as file:
    passcode = file.read()
# pid info
if sys.platform != 'win32':
    logger.info(f'Discord Bot PID is {os.getpid()}.')
# var init
jojo_run_cooldown = 4
last_jojo_run = dt.datetime.now()-dt.timedelta(hours=jojo_run_cooldown)
start_time = dt.datetime.now()
# bot init
bot = commands.Bot(command_prefix='/')
client = ds.Client()

print('Starting Bot')


def readable_time_since(seconds):
    '''
    Returns time since based on seconds argument in the unit of time that makes the most sense
    rounded to 1 decimal place.
    '''
    seconds_in_minute = 60
    seconds_in_hour = 3600
    seconds_in_day = 86400
    seconds_in_month = 2628288
    seconds_in_year = 3.154e+7
    # minutes
    if seconds < seconds_in_hour:
        minutes = round(seconds / seconds_in_minute, 1)
        return f'{minutes} minutes'
    # hours
    elif seconds < seconds_in_day:
        hours = round(seconds / seconds_in_hour, 1)
        return f'{hours} hours'
    # days
    elif  seconds < seconds_in_month:
        days = round(seconds / seconds_in_day, 1)
        return f'{days} days'
    # months
    elif seconds < seconds_in_year:
        months = round(seconds / seconds_in_month, 1)
        return f'{months} months'
    # years
    else:
        years = round(seconds / seconds_in_year, 1)
        return f'{years} years'


@bot.event
async def on_ready():
    if sys.platform != 'win32':
        logger.info(f'Logged in as {bot.user}')
    print(f'{bot.user} is ready.')
    await bot.change_presence(activity = ds.Activity(type = ds.ActivityType.watching, name = 'Bot Basic Training'))


@bot.event
async def on_member_join(member):
    '''
    Give new members the "Member" role.
    '''
    logger.info(f'{member} joined the server')
    print(f'New member joined named: {member}.')
    # TODO fix add role function
    await member.add_roles('Member', reason='New Member', atomic=True)


@bot.event
async def on_member_remove(member):
    '''
    Logs members that left the server.
    '''
    logger.info(f'{member} left the server')


@bot.event
async def on_message(message):
    global last_jojo_run
    if message.author == client.user:  # Ignore messages made by the bot
        return
    # random responses
    responses = {
    'this is the best server':'Damn Right it is!',
    'hello there':'Ahh, general kenobi',}
    if message.content.lower() in responses:
        await message.channel.send(responses[message.content.lower()])
    # jojo refrences
    jojo = [
        'oh my god', 'ohhh myyy godddd', 'ohhh myyy godddd!!!',
        'oh? You\'re aproaching me?',
        'you truly are the lowest scum in history',
        'diooo0!', 'diooo!', 'diooo', 'dioo!',
        'za warudo',
        'my name is yoshikage kira',
        'yare yare']
    if message.content.lower() in jojo:
        if last_jojo_run+dt.timedelta(hours=jojo_run_cooldown) <= dt.datetime.now():
            last_jojo_run = dt.datetime.now()
            await message.channel.send('Is that a Jojo reference?')
        else:
            print('Jojo reference detected but cooldown active.')
    # for testing
    # if message.content.lower() == 'new join':
    #     await message.author.add_roles('Member', reason='New Member', atomic=True)
    await bot.process_commands(message)  # so command instances will still get called


@bot.command(
    name = 'ping',
    help = 'Fetches latency in milliseconds.')
async def ping(ctx):
    '''
    Returns current ping to bot server.
    '''
    await ctx.send(f'Current Ping: {round(bot.latency * 1000)}ms')


@bot.command(
    name = 'purge',
    help = 'Deletes n number of messages.',
    brief='deletes n messages from newest to oldest.')
@commands.has_guild_permissions(manage_messages=True)
async def purge(ctx, num: int):
    '''
    Purges n number of messages.
    '''
    # TODO add support to delete user messages instead of a number of messages
    try:
        num = int(num) + 1
        await ctx.channel.purge(limit=num)
    except:
        user = 'Unknown'
        logger.info(f'{user} User tried to use purge command.')


@bot.command(
    name = 'roll',
    help = 'Roll dice',
    brief='Roll dice with the NdN format.',
    description='Example: 2d6 for 2 6 sided dice. Gives the sum of the numbers and a list of all of the numbers')
async def roll(ctx, dice: str):
    '''
    Rolls a dice in NdN format.
    '''
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!\nExample: 2d6 for 2 6 sided dice.')
        return
    int_list = []
    for _ in range(rolls):
        int_list.append(random.randint(1, limit))
    result = f'Sum: {sum(int_list)} | {", ".join(map(str, int_list))}'
    await ctx.send(result)


@bot.command(
    name = 'flip',
    help = 'Flip a coin.')
async def vote(ctx):
    '''
    Flips a coin. Heads or Tails.
    '''
    result = random.randint(1, 6000+1)
    if result == 1:
        msg = '...... It landed on its side. There is a 1 in 6000 chance of that happening.'
    elif (result % 2) == 0:
        msg = 'It landed on Heads.'
    else:
        msg = 'It landed on Tails.'
    await ctx.send(msg)


@bot.command(
    name = 'uptime',
    help = 'Gets Bot uptime.')
async def uptime(ctx):
    '''
    Sends the total time the bot has been running.
    TODO add uptime function
    '''
    uptime_seconds = dt.datetime.now().timestamp()-start_time.timestamp()
    await ctx.send(f'Bot Uptime: {readable_time_since(uptime_seconds)}')


# wip commands

@bot.command(
    name ='sharedgames',
    help = 'Finds games in commmon among up to 6 accounts using steam id\'s.')
async def sharedgames(ctx, id_1='', id_2='', id_3='', id_4='', id_5='', id_6=''):
    '''
    TODO finish shared game checker command
    '''
    App = Shared_Games()
    steam_ids = [id_1, id_2, id_3, id_4, id_5, id_6]
    result = App.Create_Game_Lists(steam_ids)
    print(result)
    await ctx.send(result)


@bot.command(
    name = 'speak',
    help = 'speaks what I you type after the command.',
    hidden=True)
@commands.has_any_role('Mcdonald\'s CIEIO', 'Owner')
async def speak(ctx, message):
    '''
    TODO add speak
    '''
    await channel.delete_message(message)
    print(message)
    await ctx.send(f'Message: {message}')


@bot.command(
    name = 'serverstatus',
    help = 'WIP Get server status of Rob\'s server.',
    hidden=True)
async def vote(ctx):
    '''
    TODO add server status function
    '''
    status = 'Unknown'
    await ctx.send(f'Server Status: {status}')


@bot.command(
    name = 'vote',
    help = 'WIP | Voting system.',
    hidden=True)
async def vote(ctx):
    '''
    TODO add voting command
    '''
    await ctx.send(f'Starting Vote. WIP')


bot.run(passcode)
