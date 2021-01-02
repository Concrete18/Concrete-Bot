from discord.ext import commands
import discord as ds
from logging.handlers import RotatingFileHandler
import logging as lg
import os

with open('concrete_key.txt') as file:
    passcodefile = file.read()
current_pid = os.getpid()
with open('pid.txt', "w") as file:
    file.write(str(current_pid))

# Logging
log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
logger = lg.getLogger(__name__)
logger.setLevel(lg.DEBUG) # Log Level
my_handler = RotatingFileHandler('Roku.log', maxBytes=5*1024*1024, backupCount=2)
my_handler.setFormatter(log_formatter)
logger.addHandler(my_handler)
# Other
logger.info(f'Discord Bot PID is {current_pid}.')
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print(f'{bot.user} is ready.')
    logger.info(f'Logged in as {bot.user}')
    await bot.change_presence(activity = ds.Activity(type = ds.ActivityType.watching, name = 'Bot How To\'s'))


# @client.event
# async def on_message(message):
#     responses = {
#     'this is the best server':'Damn Right it is!',
#     'hello there':'Ahh general kenobi',
#             }
#     jojo = [
#         'oh my god', 'Oh? You\'re approaching me?'
#         ]
#     if message.author == client.user:
#         return
#     if message.content.lower() in responses:
#         await message.channel.send(responses[message.content.lower()])
#     if message.content.lower() in jojo:
#         await message.channel.send('Is that a Jojo reference?')

# TODO add games in common checker


@bot.command(name = 'ping', help = 'Fetches latency.')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(name = 'Shared game checker', help = 'Finds games in commmon among up to 4 accounts using steam id\'s.')
# TODO add games in common checker
async def test(ctx, id):
    await ctx.send(f'Your ID is {id}')


bot.run(passcodefile)
