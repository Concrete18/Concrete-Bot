from discord.ext import commands
import discord as ds
from functions import *
import json


class ReactRole(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.bot_func = bot_functions()


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass
        else:
            with open('reactrole.json') as react_file:
                data = json.load(react_file)
                for item in data:
                    if item['emoji'] == payload.emoji.name:
                        role = ds.utils.get(self.bot.get_guild(payload.guild_id).roles, id=item['role_id'])
                        await payload.member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for item in data:
                if item['emoji'] == payload.emoji.name:
                    role = ds.utils.get(self.bot.get_guild(
                        payload.guild_id).roles, id=item['role_id'])
                    await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


    @commands.command(
        name = 'reactrole',
        brief='Creates a Embed that allows for gaining a role by reacting to it.',
        description='Creates a Embed that allows for gaining a role by reacting to it. Clicking again removes the role.',
        help='Creates a Embed that allows for gaining a role by reacting to it. Clicking again removes the role.')
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def reactrole(self, ctx, emoji, role: ds.Role, *, message):
        if message == None:
            message = f'React to the {emoji} to get the {role.name} role.'
        emb = ds.Embed(description=message)
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)
        with open('reactrole.json') as json_file:
            data = json.load(json_file)
            new_react_role = {
                'role_name': role.name,
                'role_id': role.id,
                'emoji': emoji,
                'message_id': msg.id}
            data.append(new_react_role)
        with open('reactrole.json', 'w') as f:
            json.dump(data, f, indent=4)


def setup(bot):
    bot.add_cog(ReactRole(bot))
