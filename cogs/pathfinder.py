from discord.ext import commands
import discord as ds
from functions import *
import random, re

class RPG(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.testing = 0
        self.bot_func = bot_functions()


    @commands.command(
        name = 'roll',
        aliases=['r'],
        brief='Roll dice with the NdN format.',
        description='Example: 2d6 for 2 6 sided dice. Gives the sum of the numbers and a list of all of the numbers')
    async def roll(self, ctx, dice: str):
        '''
        Rolls a dice in NdN format.
        '''
        # TODO add + option for stuff like 5d4+4
        try:
            rolls, limit = map(int, str(dice).split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!\nExample: 2d6 for 2 6 sided dice.')
            return
        int_list = []
        for _ in range(rolls):
            int_list.append(random.randint(1, limit))
        result = f'Sum: {sum(int_list)}\nRolls: {", ".join(map(str, int_list))}'
        await ctx.send(result)


    @commands.command(
        name = 'groupsplit',
        aliases=['gsplit', 'lootsplit'],
        brief='Splits Plat, Gold, Silver and Copper n ways.',
        description='Splits Plat, Gold, Silver and Copper coins for as large of a party as needed.',
        help='''
        Just use the /groupsplit then type your totals of Plat, Gold, Silver and Copper in any order.
        If you do not specify a split using (n)way, the split will default to 4.

        Example:

        /groupsplit 12gold 14copper 20silver 8gold 5way
        /groupsplit 12g14c20s8g5

        The above 2 command detects 20 gold, 14 copper, and 20 silver. Spaces and full coin names are optional.
        This works the same way and both are a 5 way split.

        You should notice that it can accept more then one set of each type of coin in case you want to add 438 gold
        from selling some items plus the 1250 award for the quest.
        ''')
    async def groupsplit(self, ctx, *args):
        '''
        Gives a group coin split divided by any number.

        For testing

        command:

        /gsplit 10g 56p 12gold 152s 83copper 7

        answer:

        Split 7 Way
        Gold 85
        Silver 4
        Copper 3
        Extra Copper 2
        '''
        # parses args
        combined=''.join(args)
        for word in ('lat', 'latinum', 'old', 'ilver', 'opper', 'way', 'w'):
            combined = combined.replace(word, '')
        args = re.findall(r'\d+\w?', combined)
        coins = {'p': 0, 'g': 0, 's': 0, 'c': 0, 'way': 4}
        for coin in coins:
            for arg in args:
                if coin in arg.lower():
                    coins[coin] += int(arg.rstrip(coin))
                elif arg.isdigit():
                    coins['way'] = int(arg)
        amounts = f'Platinum: {coins["p"]} | Gold: {coins["g"]} | Silver: {coins["s"]} | Copper: {coins["c"]}'
        # create gold split
        goldtotal = (coins['c'] / 100) + (coins['s'] / 10) + coins['g'] + (coins['p'] * 10)
        goldsplit = goldtotal / coins['way']
        silverleft = goldsplit * 10 % 10
        copperleft = silverleft * 10 % 10
        extraCopper = round((copperleft - int(copperleft)) * coins['way'])
        # shows results via embed
        embed = ds.Embed(
            title='Party Gold Splitter',
            description=f'Entered totals: {amounts}',
            colour=ds.Colour(0xf1c40f))
        embed.add_field(name=f'Split', value=f'{coins["way"]} Way', inline=False)
        if int(goldsplit) > 0:
            embed.add_field(name='Gold', value=f'{int(goldsplit)}', inline=True)
        if int(silverleft) > 0:
            embed.add_field(name='Silver', value=f'{int(silverleft)}', inline=True)
        if int(copperleft) > 0:
            embed.add_field(name='Copper', value=f'{int(copperleft)}', inline=True)
        if int(extraCopper) > 0:
            embed.add_field(name='Extra Copper', value=f'{int(extraCopper)}', inline=False)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(RPG(bot))
