from logging.handlers import RotatingFileHandler
from discord.ext import commands
import logging as lg
import discord as ds
import json
import sys
import os


# Logging
log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
logger = lg.getLogger(__name__)
logger.setLevel(lg.DEBUG) # Log Level
my_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=2)
my_handler.setFormatter(log_formatter)
logger.addHandler(my_handler)

# secret_key
with open('secret.json') as json_file:
    if sys.platform == 'win32':
        secret_key = json.load(json_file)['config']['discord_dev_key']
    else:
        secret_key = json.load(json_file)['config']['discord_key']

# bot init
intents = ds.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

print('Starting Concrete Bot')

# loads all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(secret_key)
