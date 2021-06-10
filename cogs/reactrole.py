from discord.ext import commands
import discord as ds
from functions import *
import json
import os


class ReactRole(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.bot_func = bot_functions()


    @staticmethod
    def check_if_json_exists():
        if not os.path.exists('Logs/reactrole.json'):
            print('It does not exist.\nMaking it now.')
            json_object = json.dumps([], indent = 4)
            with open('Logs/reactrole.json', "w") as outfile:
                outfile.write(json_object)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        '''
        Detects reaction and gives set role in response.
        '''
        if not payload.member.bot:
            with open('Logs/reactrole.json') as react_file:
                data = json.load(react_file)
            for item in data:
                if item['emoji'] == payload.emoji.name:
                    role = ds.utils.get(self.bot.get_guild(payload.guild_id).roles, id=item['role_id'])
                    await payload.member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        '''
        Detects removed reactions and removes the role for the specific reaction if it is in the reactrole.json.
        '''
        with open('Logs/reactrole.json') as react_file:
            data = json.load(react_file)
        for item in data:
            if item['emoji'] == payload.emoji.name:
                role = ds.utils.get(self.bot.get_guild(payload.guild_id).roles, id=item['role_id'])
                await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        '''
        On message delete in the react role channel, the entry for the role reaction in the json will also be deleted.
        '''
        if 'reaction to get the' in message.clean_content:
            print('React Role was deleted.')
            self.bot.logger.info(f'Deleted {print(message.id)} React Role. Check the data from the json.')
            # WIP on message delete, remove react json entry
            # with open('Logs/reactrole.json') as react_file:
            #     data = json.load(react_file)
            # for key, value in data.items():
            #     print(key, value)
            #     if message.channel in value:
                    # dict.pop(key)


    @commands.command(
        name = 'reactrole',
        brief='Creates a Embed that allows for gaining a role by reacting to it.',
        description='Creates a Embed that allows for gaining a role by reacting to it. Clicking again removes the role.',
        help='Mention the role and type the emoji you want to use.')
    @commands.has_permissions(manage_roles=True)
    async def reactrole(self, ctx, emoji, role: ds.Role):
        message = f'Click {emoji} reaction to get the {role.mention} role.'
        msg = await ctx.channel.send(embed=ds.Embed(description=message))
        await msg.add_reaction(emoji)
        self.check_if_json_exists()
        with open('Logs/reactrole.json') as json_file:
            data = json.load(json_file)
        new_react_role = {
            'role_name': role.name,
            'role_id': role.id,
            'emoji': emoji,
            'message_id': msg.id}
        data.append(new_react_role)
        with open('Logs/reactrole.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(ReactRole(bot))
