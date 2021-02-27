from discord.ext import commands
import discord as ds
from functions import *
import datetime as dt
import random
import json
import sys
import os


print('Starting Bot')

# secret_key
with open('secret.json') as json_file:
    if sys.platform == 'win32':
        secret_key = json.load(json_file)['config']['discord_dev_key']
    else:
        secret_key = json.load(json_file)['config']['discord_key']

# bot init
intents = ds.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
bot_func = bot_functions()

# loads all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# @bot.has_guild_permissions(manage_messages=True)  # TODO fix permissions
@bot.command(
    name = 'reload',
    brief='Reloads all cogs',
    hidden=True)
async def reload_cogs(ctx):
    '''
    Reloads all cogs without stopping bot.
    '''
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.reload_extension(f'cogs.{filename[:-3]}')
    await ctx.message.delete()
    msg = 'Cogs have been reloaded.'
    print(msg)
    bot_func.logger.info(msg)


start_time = dt.datetime.now()
@bot.command(
    name = 'uptime',
    brief = 'Gets Bot uptime.',
    description='Gets the Bot uptime since it last was started.')
async def uptime(ctx):
    '''
    Sends the total time the bot has been running using the readable_time_since function.
    '''
    uptime_seconds = dt.datetime.now().timestamp()-start_time.timestamp()
    await ctx.send(f'Bot Uptime: {bot_func.readable_time_since(uptime_seconds)}')


@bot.event
async def on_ready():
    if sys.platform != 'win32':
        channel = bot.get_channel(812394370849570866)
        bot_func.logger.info(f'Logged in as {bot.user}')
    else:
        channel = bot.get_channel(667229260976619561)
    print(f'{bot.user} is ready.')
    # Sends a greeting on on_ready
    greetings = ['I am back online.', 'I seem to be up and working again.', 'Sorry about my outage.\nI am back.']
    greeting = random.choice(greetings)
    await channel.send(greeting)
    # sets discord activity
    # types: playing Streaming listening watching competing = 5
    activity_name = 'Battle Bots'
    await bot.change_presence(activity=ds.Activity(type = ds.ActivityType.playing, name=activity_name))


bot.run(secret_key)
