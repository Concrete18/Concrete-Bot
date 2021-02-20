# import requests
import requests
import time

class Shared_Games:


    def __init__(self):
        with open('api_key.txt') as f:
            self.api_key = f.read()


    def Get_Game_Names(self, steam_id):
        '''
        Gets names of games owned by the entered Steam ID.
        '''
        base_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.api_key}&steamid={steam_id}&include_played_free_games=0&format=json&include_appinfo=1'
        data = requests.get(base_url)
        if data.status_code == requests.codes.ok:
            game_list = []
            for item in data.json()['response']['games']:
                game_name = item['name']
                game_list.append(game_name)
            return game_list
        else:
            return 'error'


    @staticmethod
    def Check_For_Shared_Games(lists_to_check):
        '''
        Finds the shared games among the lists entered.
        '''
        list_num = len(lists_to_check)
        final_list = []
        if list_num == 2:
            final_list = set(lists_to_check[0]) & set(lists_to_check[1])
        if list_num == 3:
            final_list = set(lists_to_check[0]) & set(lists_to_check[1]) & set(lists_to_check[2])
        if list_num == 4:
            final_list = set(lists_to_check[0]) & set(lists_to_check[1]) & set(lists_to_check[2]) & set(lists_to_check[3])
        if list_num == 5:
            final_list = set(lists_to_check[0]) & set(lists_to_check[1]) & set(lists_to_check[2]) & set(lists_to_check[3]) & set(lists_to_check[4])
        if list_num == 6:
            final_list = set(lists_to_check[0]) & set(lists_to_check[1]) & set(lists_to_check[2]) & set(lists_to_check[3]) & set(lists_to_check[4]) & set(lists_to_check[5])
        return final_list


    def Create_Game_Lists(self, steam_ids):
        '''
        Creates a list containing a list each of the profiles games entered using the Get_Game_Names Function.
        '''
        lists_to_check = []
        user_check_count = 0
        for id in steam_ids:
            if len(id) == 17:
                games = self.Get_Game_Names(id)
                if games != 'error':
                    lists_to_check.append(self.Get_Game_Names(id))
                    user_check_count += 1
        if user_check_count == 1:
            return 'Only 1 user is valid'
        elif user_check_count == 0:
            return 'No users are valid'
        final_list = self.Check_For_Shared_Games(lists_to_check)
        shared_games = ', '.join(final_list)
        result = f'{len(final_list)} shared games found.\n{shared_games}'
        return result


if __name__ == "__main__":
    App = Shared_Games()
    overall_start = time.perf_counter() # start time for checking elaspsed runtime
    print(App.Create_Game_Lists(['76561197982626192', '76561198088659293', '76561198093285176', '76561198084087457']))
    overall_finish = time.perf_counter() # stop time for checking elaspsed runtime
    elapsed_time = round(overall_finish-overall_start, 2)
    print(elapsed_time)
