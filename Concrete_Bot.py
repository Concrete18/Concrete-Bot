from discord.ext import commands
import discord as ds
import json
import sys
import os

print('Starting Concrete Bot')

# secret_key
with open('secret.json') as json_file:
    if sys.platform == 'win32':
        secret_key = json.load(json_file)['config']['discord_dev_key']
    else:
        secret_key = json.load(json_file)['config']['discord_key']

# bot init
intents = ds.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# loads all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(secret_key)
