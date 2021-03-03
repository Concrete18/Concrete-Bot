from discord.ext import commands
import discord as ds
from functions import *
import datetime as dt
import json
import sys
import os


class Member_Log(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        self.bot_func = bot_functions()
        # settings setup
        self.concrete_server = None
        self.member_data = {}
        with open('data.json') as json_file:
            self.data = json.load(json_file)


    @commands.Cog.listener()
    async def on_ready(self):
        '''
        Adds members to self.member_data if they are not already in it.
        '''
        if os.path.exists('member_data.json'):
            with open('member_data.json') as json_file:
                self.member_data = json.load(json_file)
        if sys.platform != 'win32':
            guild_id = 172069829690261504
        else:
            guild_id = 665031048941404201
        self.concrete_server = await self.bot.fetch_guild(guild_id)
        for member in self.concrete_server.members:
            # FIXME prints nothing
            print(member)
            if member not in self.member_data.keys():
                self.member_data[member] = 'no activity since 2021-03-02'
        with open('member_data.json', 'w') as json_file:
            json.dump(self.member_data, json_file, indent=4)


    def update_activity(self, member):
        '''
        Updates member in member_data.json with current date if last activity was before today.

        Logging started on 2021-03-02
        '''
        member = str(member)
        last_action = str(dt.datetime.now().date())
        if len(self.member_data) != 0:
            if member in self.member_data.keys():
                if self.member_data[member] == last_action:
                    return
        if sys.platform == 'win32':
            print(f'{member}: New Activity Detected')
        self.member_data[member] = last_action
        with open('member_data.json', 'w') as json_file:
            json.dump(self.member_data, json_file, indent=4)


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Updates last server action to the current date if an action has not occured yet.
        '''
        if message.author == self.bot.user:  # Ignore messages made by the bot
            return
        if str(message.guild) == 'Concrete Jungle':
            self.update_activity(message.author)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''
        Updates last server action to the current date if an action has not occured yet.
        '''
        if str(member.guild) == 'Concrete Jungle':
            if before.channel == None and after.channel != None:
                self.update_activity(member)


    @commands.command(
        name = 'showinactivemembers',
        aliases=['inactivemembers', 'inactive'])
    @commands.has_guild_permissions(manage_messages=True)
    async def showinactivemembers(self, ctx, days: int):
        '''
        Lists inactive members.
        '''
        print(dt.datetime.now().date() - dt.timedelta(days=int(days)))
        inactive_list = []
        for name, last_active in self.member_data:
            # FIXME wont work
            if last_active < dt.datetime.now().date() - dt.timedelta(days=int(days)):
                inactive_list.append(name)
        if len(inactive_list) == 0:
            result = f'No Members have been inactive for over {days} days.'
        else:
            result = ', '.join(inactive_list)
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Member_Log(bot))
