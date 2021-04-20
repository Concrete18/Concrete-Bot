from discord.ext import commands
import discord as ds
from functions import *
import datetime as dt
import json, sys, os


class Member_Log(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        self.bot_func = bot_functions()
        self.member_log_channel = 360587663377432578
        # settings setup
        self.concrete_server = None
        # loads member_data.json
        if os.path.exists('Logs/member_data.json'):
            with open('Logs/member_data.json') as json_file:
                self.member_data = json.load(json_file)
        else:
            self.member_data = {}


    @staticmethod
    def ascii_only(string):
        '''
        Returns ascii characters only.
        '''
        encoded_string = string.encode("ascii", "ignore")
        decoded_string = encoded_string.decode().rstrip().lstrip()
        if len(decoded_string.replace(' ', '')) < 3:
            decoded_string = 'Deleted (Too few characters)'
        return decoded_string


    def update_log(self, member, current_date, activity_type='None'):
        discord_name = self.ascii_only(member.name)
        nickname = self.ascii_only(member.display_name)
        for item in [discord_name, nickname]:
            if len(item.replace(' ', '')) < 3:
                item = 'Deleted due to unicode'
        self.member_data[str(member.id)] = {
            'discord_name':discord_name,
            'nickname':nickname,
            'activity_type':activity_type,
            'last_active':current_date}


    def update_json(self):
        '''
        Writes self.member_data to member_data.json.
        '''
        with open('Logs/member_data.json', 'w') as json_file:
            json.dump(self.member_data, json_file, indent=4)


    async def update_activity(self, member, activity_type):
        '''
        Updates member in member_data.json with current date if last activity was before today.

        Logging started on 03-03-2021
        '''
        if member.guild.id != self.bot.main_server and member.guild.id != self.bot.test_server:
            return
        current_date = str(self.convert_date(dt.datetime.now().date()))
        if len(self.member_data) != 0:
            if str(member.id) in self.member_data.keys():
                if current_date != self.member_data[str(member.id)]['last_active']:
                    self.update_log(member, current_date, activity_type,)
                    self.update_json()
            else:
                self.update_log(member, current_date, activity_type,)
                self.update_json()
        else:
            if os.path.exists('Logs/member_data.json'):
                with open('Logs/member_data.json') as json_file:
                    self.member_data = json.load(json_file)
                self.update_log(member, current_date, activity_type)
                self.update_json()
            else:
                msg = 'member_data.json is missing.'
                print(msg)
                if sys.platform == 'win32':
                    channel = self.bot.get_channel(self.bot.bot_commands_test_chan)
                else:
                    channel = self.bot.get_channel(self.bot.admin_chan)
                await channel.send(msg)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''
        Sends welcome message as a direct message.
        Gives new members the "Member" role.
        Logs user join in main bot log.
        (Make sure the bot role is above the role you are wanting it to assign.)
        '''
        if member.guild.id == self.bot.main_server:
            # Sends welcome message to new member.
            embed = ds.Embed(
                title=f'Welcome to {self.bot.server_name}!',
                description=f'Owned and run by Concrete',
                colour=ds.Colour(0xf1c40f))
            features = '''
            React based role assignment.
            Intelligent chat bot within bot-commands.
            RPG Currency splitter for multiplayer parties.
            Shared Steam Game finder with support for more than just to users.
            Taco and much more.
            '''
            embed.add_field(name='Features', value=features, inline=False)
            help_msg = 'Use a / before all commands to properly use them.\nFor help with using the commands. Use /help'
            embed.add_field(name='Help', value=help_msg, inline=False)
            await member.send(embed=embed)
            # logs new member
            self.bot.logger.info(f'{member} joined the server')
            # posts in member log channel
            channel = self.bot.get_channel(self.member_log_channel)
            await channel.send(f'{member.mention} joined the server')
            # adds member role
            role = member.guild.get_role(self.bot.member_role)
            await member.add_roles(role, reason='New Member')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        '''
        Logs members that left the server and removes users from member_data.
        '''
        if member.guild.id == self.bot.main_server:
            # logs leaving member
            self.bot.logger.info(f'{member} left the server')
            # posts in member log channel
            channel = self.bot.get_channel(self.member_log_channel)
            await channel.send(f'{member.mention} left the server')
            self.member_data.pop(str(member.id))
            self.update_json()


    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Updates last server action to the current date if an action has not occurred  on the current day.
        '''
        if message.author != self.bot.user:  # Ignore messages made by the bot
            await self.update_activity(message.author, 'text')


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''
        Updates last server action to the current date if an action has not occurred  on the current day.
        '''
        if before.channel == None and after.channel != None:
            await self.update_activity(member, 'voice')


    @staticmethod
    def convert_date(date):
        if type(date) == str:
            return dt.datetime.strptime(date, "%m-%d-%Y").date()
        else:
            return date.strftime("%m-%d-%Y")


    @commands.command(
        name = 'active',
        brief='Lists active members for the day.',
        description='Lists active members that have joined a chat or sent a message today.',
        aliases=['activemembers', 'showactivemembers'])
    @commands.has_guild_permissions(manage_guild=True)
    async def showactivemembers(self, ctx):
        '''
        Lists active members.
        '''
        active_list = []
        check_date = dt.datetime.now().date()
        for data in self.member_data.values():
            last_active = self.convert_date(data['last_active'])
            if last_active == check_date:
                if 'Deleted' in data['nickname']:
                    active_list.append(data['discord_name'])
                else:
                    active_list.append(data['nickname'])
        if len(active_list) == 0:
            result = f'No Members have been active today.'
        else:
            result = ', '.join(active_list)
        await ctx.send('Today\'s active members:\n' + result)


    @commands.command(
        name ='inactive',
        brief='Lists inactive members. Defaults to 60 days.',
        description='''
        Lists inactive members that have not joined a chat or sent a message in a set period of time.
        Defaults to 60 days if a number of days is not entered as an argument  after the command.
        ''',
        aliases=['inactivemembers'])
    @commands.has_guild_permissions(manage_messages=True)
    async def showinactivemembers(self, ctx, days: int=60):
        '''
        Lists inactive members.
        '''
        inactive_list = []
        check_date = dt.datetime.now().date() - dt.timedelta(days=int(days))
        for data in self.member_data.values():
            last_active = self.convert_date(data['last_active'])
            if last_active < check_date:
                if 'Deleted' in data['nickname']:
                    inactive_list.append(data['discord_name'])
                else:
                    inactive_list.append(data['nickname'])
        if len(inactive_list) == 0:
            result = f'No Members have been inactive for over {days} days.'
        else:
            result = ', '.join(inactive_list)
        await ctx.send(f'Inactive members for the last {days} days:\n' + result)


    @commands.command(
        name='updatemembers',
        brief='Adds missing members to member_data.')
    @commands.has_guild_permissions(manage_messages=True)
    async def update_member_data(self, ctx):
        '''
        Adds members to self.member_data if they are not already in it.
        '''
        if ctx.guild.id != self.bot.main_server and ctx.guild.id != self.bot.test_server:
            return
        new_members = []
        current_date = self.convert_date(dt.datetime.now().date())
        for member in ctx.guild.members:
            if member.bot == False:
                if str(member.id) not in self.member_data.keys():
                    self.update_log(member, current_date)
                    new_members.append(str(member.display_name))
        self.update_json()
        new_count = len(new_members)
        if new_count == 1:
            member = 'member'
        else:
            member = 'members'
        result = f'Added {new_count} new {member}.'
        self.bot.logger.info(result)
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Member_Log(bot))
