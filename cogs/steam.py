from discord.ext import commands
from functions import *
import requests, json, time


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
        if len(steam_ids) > 4:
            self.check_delay = 1
        for id in steam_ids:
            games = self.get_owned_names(id)
            if games:
                game_lists.append(games)
        return game_lists

    @commands.command(
        name ='sharedgames',
        brief = 'Finds owned games in common among steam users.',
        description='Finds games in common among the libraries of the entered steam users.',
        help='''
        You can enter your username from your vanity url or use your steam id.
        You can find your steam id using steamidfinder.com if prefered.
        \nExample: /sharedgames caseygamealot gaming4fun 12312312\nSteam Id\'s must be 17 characters long.
        '''
    )
    async def sharedgames(self, ctx, *users):
        '''
        Finds games in common among the libraries of the entered steam id's.
        '''
        steam_ids = []
        all_vanity = True
        valid_users = []
        for user in users:
            if user.isnumeric() and len(user) == 17:
                # adds user if it is likely already a steam id
                if user not in steam_ids:
                    steam_ids.append(user)
                    valid_users.append(user)
                    all_vanity = False
            elif type(user) is str:
                # gets steam id using vanity username
                steam_id = self.get_steam_id(user)
                if steam_id and steam_id not in steam_ids:
                    steam_ids.append(steam_id)
                    valid_users.append(user)
        # deletes message if all users are not given as vanity username
        if not all_vanity:
            await ctx.message.delete()
        await ctx.send(f'Finding shared Steam games for the following valid users:\n{", ".join(valid_users)}')
        game_lists = self.create_game_lists(steam_ids)
        # checks if enough data was found to properly complete the command
        total_game_lists = len(game_lists)
        if total_game_lists == 1:
            await ctx.send('Only 1 user is valid')
        elif total_game_lists == 0:
            await ctx.send('No users are valid')
        shared_games_list = self.check_for_shared_games(game_lists)
        if len(shared_games_list) == 0:
            await ctx.send('No shared games found.')
        shared_games = ', '.join(shared_games_list)
        message = f'{len(shared_games_list)} shared games found.\n{shared_games}'
        messages = self.bot_func.split_text(message, delimiter=',')
        for message in messages:
            await ctx.send(message)


def setup(bot):
    bot.add_cog(Steam(bot))
