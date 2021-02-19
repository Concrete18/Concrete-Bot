from logging.handlers import RotatingFileHandler
from discord.ext import commands
import discord as ds
import datetime as dt
import logging as lg
import random
import sys
import os

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
current_pid = os.getpid()
if sys.platform != 'win32':
    logger.info(f'Discord Bot PID is {current_pid}.')
with open('pid.txt', "w") as file:
    file.write(str(current_pid))
# var init
jojo_run_cooldown = 4
last_jojo_run = dt.datetime.now()-dt.timedelta(hours=jojo_run_cooldown)
# bot init
bot = commands.Bot(command_prefix='/')
client = ds.Client()


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


@commands.has_permissions(manage_messages=True)
@bot.command(
    name = 'purge',
    help = 'Deletes n number of messages.',
    brief='deletes n messages from newest to oldest.')
async def purge(ctx, num: int):
    '''
    Purges n number of messages.
    '''
    # TODO add support to delete user messages instead of a number of messages
    num = int(num) + 1
    await ctx.channel.purge(limit=num)


@bot.command(
    name = 'roll',
    help = 'Roll dice WIP',
    brief='Roll dice with the NdN format.',
    description='Roll dice with the NdN format. Example: 2d6 for 2 6 sided dice.')
async def roll(ctx, dice: str):
    '''
    Rolls a dice in NdN format.
    '''
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!\nExample: 2d6 for 2 6 sided dice.')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    # TODO add sum
    # result = f'{rolls} | Sum:'
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


# wip commands
# @bot.command(
#     name = 'serverstatus',
#     help = 'WIP Get server status of Rob\'s server.')
# async def vote(ctx):
#     '''
#     TODO add server status function
#     '''
#     status = 'Unknown'
#     await ctx.send(f'Server Status: {status}')


# @bot.command(
#     name = 'vote',
#     help = 'WIP | Voting system.')
# async def vote(ctx):
#     '''
#     TODO add voting command
#     '''
#     await ctx.send(f'Starting Vote. WIP')


# @bot.command(
#     name ='sharedgames',
#     help = 'WIP | Finds games in commmon among up to 4 accounts using steam id\'s.')
# async def sharedgames(ctx, id_1, id_2, id_3='', id_4=''):
#     '''
#     TODO finish shared game checker command
#     '''
#     msg = f'Your ID is {id_1}'
#     await ctx.send(msg)


bot.run(passcode)
