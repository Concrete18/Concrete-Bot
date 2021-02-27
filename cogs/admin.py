from discord.ext import commands
from functions import *
import discord as ds
import os

class Admin(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.client = ds.Client()
        self.bot_func = bot_functions()


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        info = f'Command: {ctx.command} | Error: {str(error)}'
        print(info)
        self.bot_func.logger.debug(info)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} is missing the required permission for the {ctx.command} command.')
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'{ctx.author.mention} is missing the required role for the {ctx.command} command.')
        else:
            raise(error)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''
        Give new members the "Member" role.
        Make sure the bot role is above the role you are wanting it to assign.
        '''
        msg = f'{member} joined the server'
        print(msg)
        self.bot_func.logger.info(msg)
        role = member.guild.get_role(377683900580888576)
        await member.add_roles(role, reason='New Member')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        '''
        Logs members that left the server.
        '''
        msg = f'{member} left the server'
        print(msg)
        self.bot_func.logger.info(msg)


    @commands.command(
        name ='purge',
        brief='Deletes n messages from newest to oldest.',
        description='Deletes n number of messages from the current channel. This only works for this with the manage messages permission.',
        hidden=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, num: int):
        '''
        Purges n number of messages.
        '''
        # TODO add support to delete all of a specific users messages
        await ctx.channel.purge(limit=int(num) + 1)


    @commands.command(
        name = 'speak',
        aliases=['say'],
        brief = 'Bot says what you type after the command.',
        hidden=True,
        pass_context = True)
    @commands.has_role('Owner')
    async def speak(self, ctx, *args):
        msg = ' '.join(args)
        await ctx.message.delete()
        return await ctx.send(msg)


    @commands.command(
        name ='pid',
        brief='Sends current bot PID.',
        description='Sends current bot PID.',
        hidden=True)
    async def pid(self, ctx):
        '''
        Sends current bot PID.
        '''
        await ctx.send(f'PID: {os.getpid()}')


def setup(bot):
    bot.add_cog(Admin(bot))
