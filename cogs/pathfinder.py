from discord.ext import commands
import random
import re

class Pathfinder(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name = 'roll',
        aliases=['r'],
        brief='Roll dice with the NdN format.',
        description='Example: 2d6 for 2 6 sided dice. Gives the sum of the numbers and a list of all of the numbers')
    async def roll(self, ctx, dice: str):
        '''
        Rolls a dice in NdN format.
        '''
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
        If you do not specify a split of the gold then it will default to 4.

        Example:

        /groupsplit 12gold 14copper 20silver 8gold
        /groupsplit 12g14c20s8g

        The above 2 command detects 20 gold, 14 copper, and 20 silver. Spaces and full coin names are optional.
        This works the same way.

        You should notice that it can accept more then one set of each type of coin in case you want to add 438 gold
        from selling some items plus the 1250 award for the quest.
        ''')
    async def groupsplit(self, ctx, *args):
        '''
        Gives a group coin split divided by any number.
        '''
        # parses args
        combined=''.join(args)
        combined = combined.replace("platinum", "p")
        combined = combined.replace("gold", "g")
        combined = combined.replace("silver", "s")
        combined = combined.replace("copper", "c")
        args = re.findall(r'\d+\w?', combined)
        coins = {'p': 0, 'g': 0, 's': 0, 'c': 0, 'way': 4}
        for coin in coins:
            for arg in args:
                if coin in arg.lower():
                    coins[coin] += int(arg.rstrip(coin))
                elif arg.isdigit():
                    coins['way'] = int(arg)
        amounts = f'Plat: {coins["p"]} | Gold: {coins["g"]} | Silver: {coins["s"]} | Copper: {coins["c"]}'
        entered = f'Entered {coins["way"]} Way Split: {amounts}'
        await ctx.channel.send(entered)
        # create split
        goldtotal = (coins['c'] / 100) + (coins['s'] / 10) + coins['g'] + (coins['p'] * 10)
        goldsplit = goldtotal / coins['way']
        silverleft = goldsplit * 10 % 10
        copperleft = silverleft * 10 % 10
        extraCopper = round((copperleft - int(copperleft)) * coins['way'])
        # shows results
        # TODO use .join to create same format as entered amount when showing split
        result = f'Split {coins["way"]} ways:'
        if int(goldsplit) > 0:
            result += f' {int(goldsplit)} Gold'
        if int(silverleft) > 0:
            result += f' {int(silverleft)} Silver'
        if int(copperleft) > 0:
            result += f' {int(copperleft)} Copper'
        if extraCopper > 0:
            result += f' with {extraCopper} unsplit Copper'
        await ctx.channel.send(result)


def setup(bot):
    bot.add_cog(Pathfinder(bot))
