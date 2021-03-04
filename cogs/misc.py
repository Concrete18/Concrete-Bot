from discord.ext import commands
import discord as ds
from functions import *
from typing import Optional
import datetime as dt
import asyncio


class Misc(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.bot_func = bot_functions()


    @commands.command(
        name = 'ping',
        brief = 'Fetches latency in milliseconds.',
        description='Fetches latency in milliseconds.')
    async def ping(self, ctx):
        '''
        Returns current ping to bot server.
        '''
        await ctx.send(f'Current Ping: {round(self.bot.latency * 1000)}ms')


    @commands.command(
        name = 'membercount',
        brief = 'Gets total members in server and total online/offline.',
        description='Gets total members in server and total online/offline.')
    async def membercount(self, ctx):
        '''
        Gets total members in server and total online/offline.
        '''
        all_members = []
        all_bots = []
        for member in ctx.guild.members:
            if member.bot == False:
                all_members.append(member)
            else:
                all_bots.append(member)
        embed=ds.Embed(
            title='Member and Bot Count',
            color=ds.Color((0x2ecc71)))
        embed.add_field(name='Total Members', value=len(all_members), inline=True)
        embed.add_field(name='Total Bots', value=len(all_bots), inline=True)
        await ctx.send(embed=embed)


    # wip commands


    @commands.command(
        name='createpoll',
        aliases=['mkpoll', 'makepoll'])
    @commands.has_permissions(manage_guild=True)
    async def create_poll(self, ctx, hours: float, question: str, *options):
        hours_in_seconds = hours * 60 * 60
        close_time = self.bot_func.readable_time_since(hours_in_seconds)
        numbers = (
            '1️⃣', '2⃣', '3⃣', '4⃣', '5⃣',
		    '6⃣', '7⃣', '8⃣', '9⃣', '🔟')
        if len(options) > 10:
            await ctx.send('You can only supply a maximum of 10 options.')
        else:
            embed = ds.Embed(
                title='Poll',
                description=question,
                colour=ctx.author.colour,
                timestamp=dt.datetime.utcnow())
            fields = [
                ('Options', '\n'.join([f'{numbers[index]} {option}' for index, option in enumerate(options)]), False),
                ('Instructions', 'React to cast a vote!', False),
                ('Poll Close', f'Poll will close in {close_time}', False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            message = await ctx.send(embed=embed)
            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)
            self.polls.append((message.channel.id, message.id))
            # wait for set hours
            await asyncio.sleep(hours_in_seconds)
            message = await self.bot.get_channel(message.channel.id).fetch_message(message.id)
            # TODO make it check for ties
            most_voted = max(message.reactions, key=lambda r: r.count)
            await message.channel.send(f'The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!')
            self.polls.remove((message.channel.id, message.id))


    async def get_avail_roles(self, ctx):
        '''
        Returns a list of available roles that are not in a blacklist.
        '''
        blacklist = []
        blacklist = ['Owner', 'Admin', 'Active Member']
        avail_roles = []
        all_roles = ctx.guild.roles
        for role in all_roles:
            print(str(role.id))
            if str(role) not in blacklist:
                avail_roles.append(str(role))
        return avail_roles


    @commands.command(
        name = 'roles',
        brief = 'Shows all roles that can be given with giverole command.',
        description='Shows all roles that can be given with giverole command.',
        hidden=True)
    async def roles(self, ctx):
        '''
        TODO roles function
        '''
        avail_roles = self.get_avail_roles(ctx)
        available_roles = ' ,'.join(avail_roles)
        print(available_roles)
        await ctx.send(f'Available Roles:\n{available_roles}')


    @commands.command(
        name = 'addrole',
        aliases=['giverole'],
        brief = 'Gives chosen role.',
        description='Gives chosen role if it is one of possible roles. To view roles use /roles command',
        hidden=True)
    async def addrole(self, ctx, role: ds.Role):
        '''
        TODO addrole function
        '''
        print(role)
        role_info = ds.utils.get(role)
        await ctx.author.add_roles(role_info)
        await ctx.send(f'Added Role: {str(role)}')


    @commands.command(
        name = 'removerole',
        aliases=['remrole'],
        brief = 'Removes chosen role.',
        description='Removes chosen role. To view roles use /roles command',
        hidden=True)
    async def removerole(self, ctx, time, *args):
        '''
        TODO removerole function
        '''
        msg = ' '.join(args)
        await ctx.send(f'Sheduled Message for {time}')


    @commands.command(
        name = 'schedulemsg',
        brief = 'Shedule a message to be sent at a specific time.',
        description='Shecule a message to be sent at a specific time in the channel the command was typed in.',
        hidden=True)
    async def schedulemsg(self, ctx, time, *args):
        '''
        TODO add Schedule a message function
        '''
        msg = ' '.join(args)
        await ctx.send(f'Sheduled Message for {time}')


    @commands.command(
        name = 'serverstatus',
        brief = 'WIP Get server status of Rob\'s server.',
        hidden=True)
    async def vote(self, ctx):
        '''
        TODO add server status function
        '''
        status = 'Unknown'
        await ctx.send(f'Server Status: {status}')


def setup(bot):
    bot.add_cog(Misc(bot))
