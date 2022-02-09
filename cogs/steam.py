from discord.ext import commands
import discord as ds
from functions import *
import requests, json, time, re


class Steam(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.bot_func = bot_functions()
        with open('secret.json') as json_file:
            self.api_key = json.load(json_file)['config']['steam_key']
        self.check_delay = 0


    def get_steam_id(self, vanity_url):
        '''
        Gets a users Steam ID via their `vanity_url`.
        '''
        base_url = r'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
        url = rf'{base_url}?key={self.api_key}&vanityurl={vanity_url}'
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            data = response.json()
            if 'steamid' in data['response'].keys():
                return data['response']['steamid']
        return False

    def get_owned_names(self, steam_id):
        '''
        Gets names of games owned by the entered Steam ID.
        '''
        if self.check_delay:
            time.sleep(1)
        base_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        url_end = f'?key={self.api_key}&steamid={steam_id}&include_played_free_games=0&format=json&include_appinfo=1?l=english'
        data = requests.get(base_url + url_end)
        if data.status_code == requests.codes.ok:
            if 'games' in data.json()['response'].keys():
                game_list = []
                for item in data.json()['response']['games']:
                    game_name = item['name']
                    game_list.append(game_name)
                return game_list
        return False

    @staticmethod
    def check_for_shared_games(games_list):
        '''
        Finds the shared games among the lists entered.
        '''
        base_list = set(games_list[0])
        for game_list in games_list:
            base_list &= set(game_list)
        return base_list

    def create_game_lists(self, steam_ids):
        '''
        Creates a list containing a list each of the profiles games entered using the get_owned_names Function.
        '''
        game_lists = []
        valid_users = []
        if len(steam_ids) > 4:
            self.check_delay = 1
        for id in steam_ids:
            games = self.get_owned_names(id)
            if games:
                game_lists.append(games)
                valid_users.append(id)
        return game_lists, valid_users

    @commands.command(
        name ='getsteamid',
        aliases=['steamid'],
        brief ='Finds your Steam ID using your vanity url from your steam profile.',
        help='''Enter your full steam profile pages address or just the customized username.
        Example: https://steamcommunity.com/id/concretesurfer/
        '''
    )
    async def getsteamid(self, ctx, vanity_url):
        '''
        Finds your Steam ID using your vanity url from your steam profile.
        '''
        # checks if vanity_url is a full url or just the custom username
        # https://steamcommunity.com/id/concretesurfer/
        url = 'https://steamcommunity.com/id/'
        if url in vanity_url:
            pattern = r'https://steamcommunity.com/id/(.*)/'
            vanity_url = re.findall(pattern, vanity_url)[0]
        steam_id = self.get_steam_id(vanity_url)
        if steam_id:
            await ctx.send(f'Your Steam ID is {steam_id}')
        else:
            await ctx.send(f'No Steam ID was found.')

    @commands.command(
        name ='sharedgames',
        brief ='Finds owned games in common among steam users.',
        description='Finds games in common among the libraries of the entered steam users.',
        help='''You can enter your username from your vanity url or use your steam id.
        \nExample: /sharedgames caseygamealot gaming4fun 12312312\nSteam Id\'s must be 17 characters long.
        '''
    )
    async def sharedgames(self, ctx, *users):
        '''
        Finds games in common among the libraries of the entered steam id's.
        '''
        steam_ids = []
        valid_users = []
        for user in users:
            if user.isnumeric() and len(user) == 17:
                # adds user if it is likely already a steam id
                if user not in steam_ids:
                    steam_ids.append(user)
            elif type(user) is str:
                # gets steam id using vanity username
                steam_id = self.get_steam_id(user)
                if steam_id and steam_id not in steam_ids:
                    steam_ids.append(steam_id)
        # info embed
        embed = ds.Embed(
            title='Shared Games Finder',
            description=f'Finding shared Steam games between {len(users)} users',
            colour=ds.Colour(0xf1c40f))
        game_lists, valid_users = self.create_game_lists(steam_ids)
        # checks if enough data was found to properly complete the command
        total_game_lists = len(game_lists)
        if total_game_lists == 1:
            await ctx.send(f'Only {valid_users[0]} is valid\nCheck on other users info to be sure it is accurate.')
            return
        elif total_game_lists == 0:
            await ctx.send('No users are valid. Make sure you have the correct information.')
            return
        shared_games_list = self.check_for_shared_games(game_lists)
        if len(shared_games_list) == 0:
            await ctx.send('No shared games found.')
            return
        # sends info about what games are being shown
        shared_games = ', '.join(shared_games_list)
        messages = self.bot_func.split_text(shared_games, delimiter=',')
        embed.add_field(name=f'Valid Users', value=", ".join(valid_users), inline=False)
        await ctx.send(embed=embed)
        for message in messages:
            await ctx.send(message)


def setup(bot):
    bot.add_cog(Steam(bot))
