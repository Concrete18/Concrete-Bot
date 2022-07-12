from discord.ext import commands
import discord as ds
from functions import *
import datetime as dt
import asyncio, random


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_func = bot_functions()

        # tasks
        self.polls = []
        self.scheduled_messages = []

    @commands.command(name="ping", brief="Fetches latency in milliseconds.")
    async def ping(self, ctx):
        """
        Returns current ping to bot server.
        """
        await ctx.send(f"Current Ping: {round(self.bot.latency * 1000)}ms")

    @commands.command(
        name="servertime", brief="Fetches current date and time for the server."
    )
    async def servertime(self, ctx):
        """
        Sends the current date and time for the server.
        """
        server_time = dt.datetime.now(tz=None).strftime("%A, %d %B, %I:%M %p")
        await ctx.send(f"Current server time: {server_time}")

    @commands.command(
        name="uptime",
        brief="Gets Bot uptime.",
        description="Gets the Bot uptime since it last was started.",
    )
    async def uptime(self, ctx):
        """
        Sends the total time the bot has been running using the readable_time_since function.
        """
        uptime_seconds = dt.datetime.now().timestamp() - self.bot.start_time.timestamp()
        await ctx.send(
            f"Bot Uptime: {self.bot_func.readable_time_since(uptime_seconds)}"
        )

    @commands.command(
        name="membercount",
        brief="Gets the total members and bots in server.",
        description="Gets the total members and bots in server.",
    )
    async def membercount(self, ctx):
        """
        Gets the total members in server and total online/offline.
        """
        all_members = []
        all_bots = []
        for member in ctx.guild.members:
            if member.bot == False:
                all_members.append(member)
            else:
                all_bots.append(member)
        embed = ds.Embed(title="Member and Bot Count", color=ds.Color((0x2ECC71)))
        embed.add_field(name="Total Members", value=len(all_members), inline=True)
        embed.add_field(name="Total Bots", value=len(all_bots), inline=True)
        await ctx.send(embed=embed)

    @commands.command(
        name="schedulemsg",
        aliases=["schedule", "schedmsg"],
        brief="Schedule a message to be sent after a specific number of hours.",
        description="""
        Schedule a message to be sent after a specific number of hours.
        It is sent in the channel the command was typed in.""",
    )
    async def schedulemsg(self, ctx, hours: float, *args):
        """
        Allows scheduling a message to be sent in n hours.
        """
        await ctx.message.delete()
        hours_in_seconds = hours * 60 * 60
        msg = " ".join(args)
        self.scheduled_messages.append((ctx.author, msg))
        # embed message preview
        preview = ds.Embed(
            title=f"Scheduled Message to send in {hours} hours.",
            colour=ds.Colour(0x2ECC71),
        )
        preview.add_field(name=f"Message Contents", value=msg, inline=False)
        await ctx.author.send(embed=preview)
        await asyncio.sleep(hours_in_seconds)
        # embed sent message
        self.scheduled_messages.remove((ctx.author, msg))
        schedule_msg = ds.Embed(
            title=f"{ctx.author} Scheduled Message", colour=ds.Colour(0x2ECC71)
        )
        schedule_msg.add_field(name=f"Message Contents", value=msg, inline=False)
        await ctx.channel.send(embed=schedule_msg)

    @commands.command(
        name="poll",
        brief="Creates a poll that allows voting with reactions.",
        description="Creates a poll that allows voting with reactions and allows entering an end time in hours.",
        aliases=["createpoll", "makepoll"],
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def create_poll(self, ctx, hours: float, question: str, *options):
        if hours > 0:
            hours_in_seconds = hours * 60 * 60
        numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟")
        if len(options) > 10:
            await ctx.send("You can only supply a maximum of 10 options.")
        else:
            embed = ds.Embed(
                title="Poll",
                description=question,
                colour=ctx.author.colour,
                timestamp=dt.datetime.utcnow(),
            )
            fields = [
                (
                    "Options",
                    "\n".join(
                        [
                            f"{numbers[index]} {option}"
                            for index, option in enumerate(options)
                        ]
                    ),
                    False,
                ),
                ("Instructions", "React to cast a vote!", False),
            ]
            if hours > 0:
                close_time = self.bot_func.readable_time_since(hours_in_seconds)
                fields.append(("Poll Close", f"Poll will close in {close_time}", False))
            else:
                fields.append(("Poll Close", f"No end was set.", False))
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            message = await ctx.send(embed=embed)
            for emoji in numbers[: len(options)]:
                await message.add_reaction(emoji)
            self.polls.append((message.channel.id, message.id))
            # wait for set hours
            if hours == 0:
                return
            await asyncio.sleep(hours_in_seconds)
            # removes poll from active polls list
            message = await self.bot.get_channel(message.channel.id).fetch_message(
                message.id
            )
            # vote totaling
            results_dict = {}
            winners = []
            winning_total = 0
            for index, reaction in enumerate(message.reactions):
                total_votes = reaction.count - 1
                results_dict[options[index]] = total_votes
                if total_votes > winning_total:
                    winning_total = total_votes
            for option, votes in results_dict.items():
                if votes == winning_total and votes > 0:
                    winners.append(option)
            # vote result setup
            win_total = len(winners)
            if win_total > 1:
                result = f'There was a tie among {", ".join(winners)} with {winning_total} votes each.'
            elif win_total == 0:
                result = "No one voted."
            else:
                result = f"The most voted choice was {winners[0]} with {winning_total} votes."
            # embed and send
            embed = ds.Embed(
                title="Poll Complete",
                description=question,
                colour=ctx.author.colour,
                timestamp=dt.datetime.utcnow(),
            )
            embed.add_field(name="Results", value=result, inline=inline)
            await message.channel.send(embed=embed)
            self.polls.remove((message.channel.id, message.id))

    @commands.command(
        name="randomchoice",
        aliases=["randchoice", "randompick", "randpick"],
        brief="Type multiple choices separated by spaces in order to have one picked for you randomly.",
        description="Type multiple choices separated by spaces in order to have one picked for you randomly."
        'Surround in " if the choices includes spaces.',
    )
    async def schedulemsg(self, ctx, *choices):
        """
        Allows scheduling a message to be sent in n hours.
        """
        if len(choices) == 0:
            await ctx.send("No choices were given.")
            return
        embed = ds.Embed(
            title=f"Random Choice",
            description=", ".join(choices),
            colour=ds.Colour(0x2ECC71),
        )
        pick = random.choice(choices)
        embed.add_field(name=f"Pick", value=pick, inline=False)
        await ctx.send(embed=embed)

    # wip commands

    @commands.command(
        name="serverstatus", brief="WIP Get server status of Rob's server.", hidden=True
    )
    async def vote(self, ctx):
        """
        TODO add server status function
        """
        status = "Unknown"
        await ctx.send(f"Server Status: {status}")


def setup(bot):
    bot.add_cog(Misc(bot))
