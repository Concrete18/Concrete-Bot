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
        self.member_data = {}
        with open('data.json') as json_file:
            self.data = json.load(json_file)
        if os.path.exists('member_data.json'):
            with open('member_data.json') as json_file:
                self.member_data = json.load(json_file)


    def update_activity(self, member):
        member = str(member)
        last_action = str(dt.datetime.now().date())
        if len(self.member_data) != 0:
            if member in self.member_data.keys():
                if self.member_data[member] == last_action:
                    return
        # if sys.platform == 'win32':
        print(f'{member}: New Activity Detected')
        self.member_data[member] = last_action
        with open('member_data.json', 'w') as json_file:
            json.dump(self.member_data, json_file)


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Updates last server action to the current date if an action has not occured yet.
        '''
        if message.author == self.bot.user:  # Ignore messages made by the bot
            return
        self.update_activity(message.author)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''
        Updates last server action to the current date if an action has not occured yet.
        '''
        if before.channel == None and after.channel != None:
            self.update_activity(member)


def setup(bot):
    bot.add_cog(Member_Log(bot))
