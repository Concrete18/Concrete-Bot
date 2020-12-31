from discord.ext import commands
from discord import Client
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
client = Client()
bot = commands.Bot(command_prefix='/')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}.')
    logger.info(f'We have logged in as {client.user}.')


@client.event
async def on_message(message):
    responses = {
    'this is the best server':'Damn Right it is!',
    'hello there':'Ahh general kenobi',
            }
    jojo = [
        'oh my god', 'Oh? You\'re approaching me?'
        ]
    if message.author == client.user:
        return
    if message.content.lower() in responses:
        await message.channel.send(responses[message.content.lower()])
    if message.content.lower() in jojo:
        await message.channel.send('Is that a Jojo reference?')


@bot.command(pass_context=True)
@commands.has_any_role('Admin', 'Moderator')
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        logger.info(f'Messages purged by {ctx.author.mention}.')

# TODO add games in common checker

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


client.run(passcodefile)
