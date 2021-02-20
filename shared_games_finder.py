# import requests
from logging import exception
import requests
import time

class Shared_Games:


    def __init__(self):
        with open('api_key.txt') as f:
            self.api_key = f.read()


    def get_game_names(self, steam_id):
        '''
        Gets names of games owned by the entered Steam ID.
        '''
        base_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.api_key}&steamid={steam_id}&include_played_free_games=0&format=json&include_appinfo=1'
        data = requests.get(base_url)
        if data.status_code == requests.codes.ok:
            print('good data for', steam_id)
            game_list = []
            for item in data.json()['response']['games']:
                game_name = item['name']
                game_list.append(game_name)
            return game_list
        else:
            print('404')
            raise Exception


    @staticmethod
    def check_for_shared_games(games):
        '''
        Finds the shared games among the lists entered.
        '''
        list_num = len(games)
        shared = []
        if list_num == 2:
            shared = set(games[0]) & set(games[1])
        if list_num == 3:
            shared = set(games[0]) & set(games[1]) & set(games[2])
        if list_num == 4:
            shared = set(games[0]) & set(games[1]) & set(games[2]) & set(games[3])
        if list_num == 5:
            shared = set(games[0]) & set(games[1]) & set(games[2]) & set(games[3]) & set(games[4])
        if list_num == 6:
            shared = set(games[0]) & set(games[1]) & set(games[2]) & set(games[3]) & set(games[4]) & set(games[5])
        return shared


    def create_game_lists(self, steam_ids):
        '''
        Creates a list containing a list each of the profiles games entered using the get_game_names Function.
        '''
        lists_to_check = []
        for id in steam_ids:
            print('given id', id)
            if len(id) == 17:
                print('accepted id', id)
                try:
                    games = self.get_game_names(id)
                    lists_to_check.append(games)
                except Exception:
                    pass
                print()
        lists_to_check_num = len(lists_to_check)
        print()
        if lists_to_check_num == 1:
            return 'Only 1 user is valid'
        elif lists_to_check_num == 0:
            return 'No users are valid'
        final_list = self.check_for_shared_games(lists_to_check)
        shared_games = ', '.join(final_list)
        result = f'{len(final_list)} shared games found.\n{shared_games}'
        return result


if __name__ == "__main__":
    App = Shared_Games()
    overall_start = time.perf_counter() # start time for checking elaspsed runtime
    print(App.create_game_lists(['76561197982626192', '76561198088659293', '76561198093285176', '76561198084087457']))
    overall_finish = time.perf_counter() # stop time for checking elaspsed runtime
    elapsed_time = round(overall_finish-overall_start, 2)
    print(elapsed_time)
