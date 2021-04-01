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
        self.member_log_channel = 360587663377432578
        # settings setup
        self.concrete_server = None
        # loads member_data.json
        if os.path.exists('member_data.json'):
            with open('member_data.json') as json_file:
                self.member_data = json.load(json_file)
        else:
            self.member_data = {}


    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''
        Gives new members the "Member" role.
        Make sure the bot role is above the role you are wanting it to assign.
        '''
        msg = f'{member} joined the server'
        print(msg)
        self.bot.logger.info(msg)
        role = member.guild.get_role(self.bot.member_role)
        await member.add_roles(role, reason='New Member')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        '''
        Logs members that left the server.
        '''
        self.bot.logger.info(f'{member} left the server')
        channel = self.get_channel(self.member_log_channel)
        await channel.send(f'{member.mention} left the server')


    # TODO add backup of member_data.json


    @staticmethod
    def return_ascii_only(string):
        encoded_string = string.encode("ascii", "ignore")
        decoded_string = encoded_string.decode().rstrip().lstrip()
        if len(decoded_string.replace(' ', '')) < 3:
            decoded_string = 'Deleted (Too few characters)'
        return decoded_string


    def update_log(self, member, current_date):
        discord_name = self.return_ascii_only(member.name)
        nickname = self.return_ascii_only(member.display_name)
        for item in [discord_name, nickname]:
            if len(item.replace(' ', '')) < 3:
                item = 'Deleted due to unicode'
        self.member_data[str(member.id)] = [discord_name, nickname, current_date]


    async def update_activity(self, member):
        '''
        Updates member in member_data.json with current date if last activity was before today.

        Logging started on 03-03-2021
        '''
        # TODO check repeats from Rob within minutes of each other
        if member.guild.id != self.bot.main_server and member.guild.id != self.bot.test_server:
            return
        current_date = str(dt.datetime.now().date().strftime("%m-%d-%Y"))
        if len(self.member_data) != 0:
            if str(member.id) in self.member_data.keys():
                if current_date != self.member_data[str(member.id)][1]:
                    self.update_log(member, current_date)
                    with open('member_data.json', 'w') as json_file:
                        json.dump(self.member_data, json_file, indent=4)
                    if sys.platform == 'win32':
                        print(f'{member}: New Activity Detected')
        else:
            if os.path.exists('member_data.json'):
                with open('member_data.json') as json_file:
                    self.member_data = json.load(json_file)
                self.update_log(member, current_date)
                with open('member_data.json', 'w') as json_file:
                    json.dump(self.member_data, json_file, indent=4)
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
    @commands.has_guild_permissions(manage_guild=True)
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
        await ctx.send('Today\'s last active members:\n' + result)


    @commands.command(
        name = 'inactive',
        brief='Lists inactive members. Defaults to 60 days.',
        description='''
        Lists inactive members that have not joined a chat or sent a message in a set period of time.
        Defaults to 60 days if a number of days is not entered after the command.
        ''',
        aliases=['inactivemembers'])
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
        await ctx.send(f'Inactive members for the last {days}:\n' + result)


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
        current_date = dt.datetime.now().date().strftime("%m-%d-%Y")
        for member in ctx.guild.members:
            if member.bot == False:
                if str(member.id) not in self.member_data.keys():
                    self.update_log(member, current_date)
                    new_members.append(str(member.display_name))
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
