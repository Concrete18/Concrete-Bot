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


    # TODO add backup of member_data.json


    async def update_activity(self, member):
        '''
        Updates member in member_data.json with current date if last activity was before today.

        Logging started on 2021-03-03
        '''
        if member.guild.id != self.bot.main_server and member.guild.id != self.bot.test_server:
            return
        current_date = str(dt.datetime.now().date().strftime("%m-%d-%Y"))
        name = member.name
        member_id = str(member.id)

        def update_log():
            self.member_data[member_id] = [name, current_date]
            with open('member_data.json', 'w') as json_file:
                json.dump(self.member_data, json_file, indent=4)

        if len(self.member_data) != 0:
            if member_id in self.member_data.keys():
                if current_date != self.member_data[member_id][1]:
                    update_log()
                    info = f'{member}: New Activity Detected'
                    self.bot.logger.info(info)
                    if sys.platform == 'win32':
                        print(info)
        else:
            if os.path.exists('member_data.json'):
                with open('member_data.json') as json_file:
                    self.member_data = json.load(json_file)
                update_log()
            else:
                msg = 'member_data.json is missing.'
                print(msg)
                if sys.platform == 'win32':
                    channel = self.bot.get_channel(self.bot.bot_commands_test_chan)
                else:
                    channel = self.bot.get_channel(self.bot.admin_chan)
                await channel.send(msg)


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Updates last server action to the current date if an action has not occured on the current day.
        '''
        if message.author != self.bot.user:  # Ignore messages made by the bot
            await self.update_activity(message.author)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''
        Updates last server action to the current date if an action has not occured on the current day.
        '''
        if before.channel == None and after.channel != None:
            await self.update_activity(member)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        '''
        Removes users from member_data when they leave the server.
        '''
        # TODO check if this works
        try:
            self.member_data.pop(str(member.id))
        except Exception as error:
            print(error)
            print('self.member_data is not accesible.')


    @commands.command(
        name = 'active',
        brief='Lists active members for the day.',
        description='Lists active members that have joined a chat or sent a message today.',
        aliases=['activemembers', 'showactivemembers'])
    @commands.has_guild_permissions(manage_messages=True)
    async def showactivemembers(self, ctx, days: int=60):
        '''
        Lists inactive members.
        '''
        active_list = []
        check_date = dt.datetime.now().date()
        for entry, data in self.member_data.items():
            last_active = dt.datetime.strptime(data[1], "%m-%d-%Y").date()
            if last_active == check_date:
                active_list.append(data[0])
        if len(active_list) == 0:
            result = f'No Members have been active today.'
        else:
            result = ', '.join(active_list)
        await ctx.send(result)


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
        if ctx.guild.id != self.bot.main_server and ctx.guild.id != self.bot.test_server:
            return
        new_members = []
        for member in ctx.guild.members:
            if member.bot == False:
                member_id = str(member.id)
                name = str(member)
                current_date = dt.datetime.now().date().strftime("%m-%d-%Y")
                if member_id not in self.member_data.keys():
                    self.member_data[member_id] = [name, current_date]
                    new_members.append(name)
                    print('Added', member)
        with open('member_data.json', 'w') as json_file:
            json.dump(self.member_data, json_file, indent=4)
        new_count = len(new_members)
        if new_count == 1:
            member = 'member'
        else:
            member = 'members'
        result = f'Added {new_count} new {member}.'
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Member_Log(bot))
