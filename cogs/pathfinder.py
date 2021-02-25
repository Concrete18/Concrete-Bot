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
        description='Splits Plat, Gold, Silver and Copper coints for as large of a party as needed.')
    async def groupsplit(self, ctx, *args):
        '''
        Gives a group coin split divided by any number.
        '''
        # parses args
        coins = {'p': 0, 'g': 0, 's': 0, 'c': 0, 'way': 0}
        for coin in coins:
            for arg in args:
                if coin in arg.lower():
                    coins[coin] = int(arg.rstrip(coin))
                elif arg.isdigit():
                    coins['way'] = int(arg)
        amounts = f'Plat: {coins["p"]} | Gold: {coins["g"]} | Silver: {coins["s"]} | Copper: {coins["c"]}'
        entered = f'Entered {coins["way"]} Way Split: {amounts}'
        await ctx.channel.send(entered)
        # create split
        goldtotal = (coins['c'] / 100) + (coins['s'] / 10) + coins['g'] + (coins['p'] * 10)
        goldsplit = int(goldtotal / coins['way'])
        silverleft = int(goldsplit * 10 % 10)
        copperleft = int(silverleft * 10 % 10)
        # shows results
        result = f'Gold: {goldsplit}\nSilver: {silverleft}\nCopper: {copperleft}'
        await ctx.channel.send(result)


def setup(bot):
    bot.add_cog(Pathfinder(bot))
