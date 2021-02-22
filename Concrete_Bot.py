from logging.handlers import RotatingFileHandler
from discord import channel,Intents
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

intents = Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
client = ds.Client()
Shared = Shared_Games()

print('Starting Concrete Bot')


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


async def split_string(ctx, string):
    '''
    Sends a split string in half if it is over 2000 characters.
    '''
    if len(string) <= 2000:
        await ctx.send(string)
    elif len(string) > 4000:
        await ctx.send('Output is too large.')
    else:
        middle = len(string)//2
        await ctx.send(string[0:middle])
        await ctx.send(string[middle:])


@bot.event
async def on_ready():
    if sys.platform != 'win32':
        logger.info(f'Logged in as {bot.user}')
    print(f'{bot.user} is ready.\n')
    await bot.change_presence(activity = ds.Activity(type = ds.ActivityType.watching, name = 'Bot Basic Training'))


@bot.event
async def on_command_error(ctx, error):
    logger.debug(str(error))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} is missing the required permission.')
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.send(f'{ctx.author.mention} is missing the required role.')
    else:
        raise(error)


@bot.event
async def on_member_join(member):
    '''
    Give new members the "Member" role.
    '''
    logger.info(f'{member} joined the server')
    print(f'New member joined named: {member}.')
    role = member.guild.get_role(377683900580888576)
    await member.add_roles(role, reason='New Member')


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
        'oh my god', 'oh my god!','ohhh myyy godddd', 'ohhh myyy godddd!!!',
        'oh? You\'re aproaching me?',
        'you truly are the lowest scum in history',
        'diooo', 'diooo!', 'diooo', 'dioo!',
        'za warudo',
        'my name is yoshikage kira',
        'yare yare']
    if message.content.lower() in jojo:
        if last_jojo_run+dt.timedelta(hours=jojo_run_cooldown) <= dt.datetime.now():
            last_jojo_run = dt.datetime.now()
            await message.channel.send('Is that a Jojo reference?')
        else:
            print('Jojo reference detected but cooldown active.')
    await bot.process_commands(message)  # so command instances will still get called


@bot.command(
    name = 'ping',
    brief = 'Fetches latency in milliseconds.',
    description='Fetches latency in milliseconds.')
async def ping(ctx):
    '''
    Returns current ping to bot server.
    '''
    await ctx.send(f'Current Ping: {round(bot.latency * 1000)}ms')


@bot.command(
    name = 'purge',
    brief='Deletes n messages from newest to oldest.',
    description='Deletes n number of messages from the current channel. This only works for this with the manage messages permission.')
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
    result = f'Sum: {sum(int_list)}\nRolls: {", ".join(map(str, int_list))}'
    await ctx.send(result)


@bot.command(
    name = 'flip',
    brief = 'Flip a coin.',
    description='Flips a coin. Who knows what result will be.')
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
    brief = 'Gets Bot uptime.',
    description='Gets the Bot uptime since it last was started.')
async def uptime(ctx):
    '''
    Sends the total time the bot has been running using the readable_time_since function.
    '''
    uptime_seconds = dt.datetime.now().timestamp()-start_time.timestamp()
    await ctx.send(f'Bot Uptime: {readable_time_since(uptime_seconds)}')


@bot.command(
    name ='sharedgames',
    brief = 'Finds owned games in commmon using steam id\'s.',
    description='Finds games in commmon among the libraries of the entered steam id\'s.',
    help='You can use steamidfinder.com to find the steam id\'s.\nExample: /sharedgames 21312313 123123123 12312312\nSteam Id\'s must be 17 characters long.')
async def sharedgames(ctx, *steam_ids):
    '''
    Finds games in commmon among the libraries of the entered steam id's.
    '''
    # TODO use proper delete command
    await ctx.message.delete()
    await ctx.send(f'Finding shared games from {len(steam_ids)} steam id\'s.')
    result = Shared.create_game_lists(steam_ids)
    await split_string(ctx, result)


@commands.has_any_role('Mcdonald\'s CIEIO', 'Owner')
@bot.command(
    name = 'speak',
    brief = 'speaks what I you type after the command.',
    hidden=True,
    pass_context = True)
async def speak(ctx, *args):
    mesg = ' '.join(args)
    await ctx.message.delete()
    # await bot.delete_message(ctx.message)
    return await ctx.send(mesg)


# wip commands


@bot.command(
    name = 'serverstatus',
    brief = 'WIP Get server status of Rob\'s server.',
    hidden=True)
async def vote(ctx):
    '''
    TODO add server status function
    '''
    status = 'Unknown'
    await ctx.send(f'Server Status: {status}')


@bot.command(
    name = 'vote',
    brief = 'WIP | Voting system.',
    hidden=True)
async def vote(ctx):
    '''
    TODO add voting command
    '''
    await ctx.send(f'Starting Vote. WIP')


bot.run(passcode)
