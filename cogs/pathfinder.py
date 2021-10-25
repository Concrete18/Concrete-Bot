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
        Rolls a dice in NdN format. + and DL, KH are optional.
        '''
        drop_lowest = 0
        keep_highest = 0
        dice = dice.lower()
        pattern = r"^\d+[d]\d+([+]\d+)?(kh)?(dl)?([+]\d+)?$"
        if re.match(pattern, dice):
            if 'dl' in dice:
                dice = dice.replace('dl','')
                drop_lowest = 1
            if 'kh' in dice:
                dice = dice.replace('kh','')
                keep_highest = 1
            main_roll = str(dice).split('+')
            rolls, limit = map(int, main_roll[0].split('d'))
            int_list = []
            lowest_roll = 1000
            highest_roll = 0
            for _ in range(rolls):
                roll = random.randint(1, limit)
                if roll > highest_roll:
                    highest_roll = roll
                if roll < lowest_roll:
                    lowest_roll = roll
                int_list.append(roll)
            dice_sum = sum(int_list)
            if '+' in dice:
                result = f'Sum: {dice_sum+int(main_roll[1])}\nRolls: {", ".join(map(str, int_list))} + {main_roll[1]}'
            else:
                result = f'Sum: {dice_sum}\nRolls: {", ".join(map(str, int_list))}'
            if drop_lowest:
                result += f'\nFinal Roll: {dice_sum - lowest_roll}'
            if keep_highest:
                result += f'\nHighest: {highest_roll}'
            await ctx.send(result)
        else:
            await ctx.send('Format has to be in NdN or NdN+N!\nExample:\n2d6 or 2d6+4')

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
        '''
    )
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
