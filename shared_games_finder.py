import requests
import time

class Shared_Games:


    def __init__(self):
        with open('api_key.txt') as f:
            self.api_key = f.read()


    def get_steam_id(self, vanity_url):
        base_url = f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={self.api_key}&vanityurl={vanity_url}&url_type=1'
        print(base_url)


    def get_game_names(self, steam_id):
        '''
        Gets names of games owned by the entered Steam ID.
        '''
        base_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.api_key}&steamid={steam_id}&include_played_free_games=0&format=json&include_appinfo=1'
        data = requests.get(base_url)
        if data.status_code == requests.codes.ok:
            game_list = []
            data
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
        # TODO add a way to get info without steam id
        lists_to_check = []
        for id in steam_ids:
            if len(id) == 17:
                games = self.get_game_names(id)
                lists_to_check.append(games)
        lists_to_check_num = len(lists_to_check)
        if lists_to_check_num == 1:
            return 'Only 1 user is valid'
        elif lists_to_check_num == 0:
            return 'No users are valid'
        final_list = self.check_for_shared_games(lists_to_check)
        shared_games = ', '.join(final_list)
        result = f'{len(final_list)} shared games found.\n\n{shared_games}'
        return result


if __name__ == "__main__":
    App = Shared_Games()
    # App.get_steam_id('https://steamcommunity.com/id/PathieZ')
    # input()
    overall_start = time.perf_counter() # start time for checking elaspsed runtime
    print(App.create_game_lists(['76561197982626192', '76561198088659293', '76561198093285176', '76561198084087457']))
    overall_finish = time.perf_counter() # stop time for checking elaspsed runtime
    elapsed_time = round(overall_finish-overall_start, 2)
    print(elapsed_time)
