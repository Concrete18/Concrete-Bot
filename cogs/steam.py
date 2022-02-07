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

    def get_game_names(self, steam_id):
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
        else:
            raise Exception

    @staticmethod
    def check_for_shared_games(games):
        '''
        Finds the shared games among the lists entered.
        '''
        shared = set(games[0])
        for game in games:
            shared &= set(game)
        return shared

    def create_game_lists(self, steam_ids):
        '''
        Creates a list containing a list each of the profiles games entered using the get_game_names Function.
        '''
        lists_to_check = []
        if len(steam_ids) > 4:
            self.check_delay = 1
        for id in steam_ids:
            games = self.get_game_names(id)
            lists_to_check.append(games)
        lists_to_check_num = len(lists_to_check)
        if lists_to_check_num == 1:
            return 'Only 1 user is valid'
        elif lists_to_check_num == 0:
            return 'No users are valid'
        final_list = self.check_for_shared_games(lists_to_check)
        if len(final_list) == 0:
            return 'No shared games found.'
        shared_games = ', '.join(final_list)
        result = f'{len(final_list)} shared games found.\n{shared_games}'
        return result

    @commands.command(
        name ='sharedgames',
        aliases=['delete'],
        brief = 'Finds owned games in common using steam id\'s.',
        description='Finds games in common among the libraries of the entered steam users.',
        help=
        '''
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
        result = self.create_game_lists(steam_ids)
        await self.bot_func.split_send(ctx, result, delimiter=',')


def setup(bot):
    bot.add_cog(Steam(bot))
