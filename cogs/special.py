from discord.ext import commands
import discord as ds
from functions import *
import subprocess, sys, os


class Special(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        self.bot_func = bot_functions()


    @commands.command(
        name ='roku',
        brief='Changes Grandmom\'s TV to ABC.')
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx):
        '''
        Changes Grandmoms TV to ABC.
        '''
        script = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Roku-Control/Instant_Set_to_ABC.py"
        if os.path.exists(script):
            subprocess.run([sys.executable, script], cwd=os.path.dirname(script))
            await ctx.send('Roku Channel Change was stasrted.')
        else:
            await ctx.send('Path does not exist anymore.')


def setup(bot):
    bot.add_cog(Special(bot))
