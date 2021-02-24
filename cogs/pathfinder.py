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


    @staticmethod
    def parseArgs(self, *inputStrings):
        seperator = ""
        inputString = seperator.join(inputStrings)
        inputString = inputString.replace(",", "")
        inputString = inputString.replace(" ", "")
        inputString = inputString.replace("k", "000")
        try:
            gold = re.search('[0-9][0-9]*[gG]', inputString).group(0)
            gold = gold.rstrip('g')
            gold = int(gold)
        except:
            gold = 0
            pass
        try:
            silver = re.search('[0-9][0-9]*[sS]', inputString).group(0)
            silver = silver.rstrip('s')
            silver = int(silver)
        except:
            silver = 0
            pass
        try:
            copper = re.search('[0-9][0-9]*[cC]', inputString).group(0)
            copper = copper.rstrip('c')
            copper = int(copper)
        except:
            copper = 0
            pass
        try:
            plat = re.search('[0-9][0-9]*[pP]', inputString).group(0)
            plat = plat.rstrip('p')
            plat = int(plat)
        except:
            plat = 0
            pass
        try:
            way = re.search('[0-9][0-9]*way', inputString).group(0)
            way = way.rstrip('way')
            way = int(way)
        except:
            way = 4
            pass
        return [plat, gold, silver, copper, way]


    @commands.command()
    async def groupsplit(self, ctx, *args):  # Old way copper=0, silver=0, gold=0, plat=0
        coinTuple = self.parseArgs(*args)
        plat = coinTuple[0]
        gold = coinTuple[1]
        silver = coinTuple[2]
        copper = coinTuple[3]
        way = coinTuple[4]

        goldtotal = (copper / 100) + (silver / 10) + gold + (plat * 10)
        goldsplit = goldtotal / way
        silverleft = goldsplit * 10 % 10
        copperleft = silverleft * 10 % 10
        await ctx.channel.send(str(way) + ' Way Split Gold: ' + (str(int(goldsplit))) +
                            '  Silver: ' + (str(int(silverleft)) + '  Copper: ' + (str(int(copperleft)))))
        print(goldtotal)
        print(silverleft)
        print(copperleft)


def setup(bot):
    bot.add_cog(Pathfinder(bot))
