from discord.ext import commands
import discord as ds
from logging.handlers import RotatingFileHandler
import logging as lg
import os
import datetime as dt

with open('concrete_key.txt') as file:
    passcodefile = file.read()
current_pid = os.getpid()
with open('pid.txt', "w") as file:
    file.write(str(current_pid))

# Logging
log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
logger = lg.getLogger(__name__)
logger.setLevel(lg.DEBUG) # Log Level
my_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2)
my_handler.setFormatter(log_formatter)
logger.addHandler(my_handler)
# Other
logger.info(f'Discord Bot PID is {current_pid}.')

bot = commands.Bot(command_prefix='/')
client = ds.Client()


@bot.event
async def on_ready():
    print(f'{bot.user} is ready.')
    logger.info(f'Logged in as {bot.user}')
    await bot.change_presence(activity = ds.Activity(type = ds.ActivityType.watching, name = 'Bot Basic Training'))


@bot.event
async def on_message(message):
    jojo_run_cooldown = 4
    last_jojo_run = dt.datetime.now()
    responses = {
    'this is the best server':'Damn Right it is!',
    'hello there':'Ahh, general kenobi',}
    jojo = [
        'oh my god',
        'Oh? You\'re aproaching me?']
    if message.author == client.user:  # Ignore messages made by the bot
        return
    if message.content.lower() in responses:
        await message.channel.send(responses[message.content.lower()])
    if message.content.lower() in jojo:
        if last_jojo_run-dt.timedelta(hours=jojo_run_cooldown) <= set_date <= now:
        last_jojo_run = dt.datetime.now()
        await message.channel.send('Is that a Jojo reference?')
    await bot.process_commands(message)  # so command instances will still get called


@bot.command(name = 'purge', help = 'Purges n messages.')
async def purge(ctx, num):
    '''
    TODO add purge function
    '''
    await ctx.send(f'Purging {num} messages.')
    num += 1


@bot.command(name = 'vote', help = 'Voting system.')
async def vote(ctx):
    '''
    TODO add voting command
    '''
    await ctx.send(f'Starting Vote. WIP')


@bot.command(name = 'ping', help = 'Fetches latency.')
async def ping(ctx):
    '''
    Returns current ping to bot server.
    '''
    await ctx.send(f'Current Ping: {round(bot.latency * 1000)}ms')


@bot.command(name = 'Shared game checker', help = 'Finds games in commmon among up to 4 accounts using steam id\'s.')
async def test(ctx, id_1, id_2, id_3, id_4):
    '''
    TODO finish shared game checker command
    '''
    msg = f'Your ID is {id_1}'
    await ctx.send(msg)


bot.run(passcodefile)
