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
        with open('data.json') as json_file:
            self.data = json.load(json_file)
        # loads member_data.json
        if os.path.exists('member_data.json'):
            with open('member_data.json') as json_file:
                self.member_data = json.load(json_file)
        else:
            self.member_data = {}


    def update_activity(self, member):
        '''
        Updates member in member_data.json with current date if last activity was before today.

        Logging started on 2021-03-03
        '''
        if member.guild.id != 172069829690261504 and member.guild.id != 665031048941404201:
            return
        member_id = str(member.id)
        name = member.name
        current_date = str(dt.datetime.now().date().strftime("%m-%d-%Y"))
        print(name, current_date)
        if len(self.member_data) != 0:
            if member_id in self.member_data.keys():
                print(f'Skipped {name}')
                return
        if sys.platform == 'win32':
            print(f'{member}: New Activity Detected')
        self.member_data[member_id] = [name, current_date]
        with open('member_data.json', 'w') as json_file:
            json.dump(self.member_data, json_file, indent=4)


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Updates last server action to the current date if an action has not occured on the current day.
        '''
        if message.author != self.bot.user:  # Ignore messages made by the bot
            self.update_activity(message.author)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''
        Updates last server action to the current date if an action has not occured on the current day.
        '''
        if before.channel == None and after.channel != None:
            self.update_activity(member)


    @commands.command(
        name = 'showinactivemembers',
        brief='Lists inactive members. Defaults to 60 days.',
        description='''
        Lists inactive members that have not joined a chat or sent a message in a set period of time.
        Defaults to 60 days if a number of days is not entered after the command.
        ''',
        aliases=['inactivemembers', 'inactive'])
    @commands.has_guild_permissions(manage_messages=True)
    async def showinactivemembers(self, ctx, days: int=60):
        '''
        Lists inactive members.
        '''
        inactive_list = []
        check_date = dt.datetime.now().date() - dt.timedelta(days=int(days))
        for entry, data in self.member_data.items():
            # FIXME wont work
            last_active = dt.datetime.strptime(data[1], "%m-%d-%Y").date()
            if last_active < check_date:
                inactive_list.append(data[0])
        if len(inactive_list) == 0:
            result = f'No Members have been inactive for over {days} days.'
        else:
            result = ', '.join(inactive_list)
        await ctx.send(result)


    @commands.command(
        name = 'updatemembers')
    @commands.has_guild_permissions(manage_messages=True)
    async def update_member_data(self, ctx):
        '''
        Adds members to self.member_data if they are not already in it.
        '''
        print('Updating member_data')
        if ctx.guild.id != 172069829690261504 and ctx.guild.id != 665031048941404201:
            return
        for member in ctx.guild.members:
            if member.bot == False:
                member_id = str(member.id)
                name = str(member)
                current_date = dt.datetime.now().date().strftime("%m-%d-%Y")
                if member_id not in self.member_data.keys():
                    self.member_data[member_id] = [name, current_date]
                    print('Added', member)
        with open('member_data.json', 'w') as json_file:
            json.dump(self.member_data, json_file, indent=4)


def setup(bot):
    bot.add_cog(Member_Log(bot))