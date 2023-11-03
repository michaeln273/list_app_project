from steam.utility import int_input, range_input

class User:
    def __init__(self, store, username):
        self.store = store
        self.username = username
        
        self.owned_games = [] # List containing game object along with extra info
        self.total_play_time = 0
        self.total_favorites = 0

    def purchase_game(self):
        game = self.store.select_search()

        if not game:
            print("No game has been purchased")
            return
        
        for owned_game in self.owned_games:
            if owned_game["obj"].id == game.id:
                print(f"You already own {game.name}")
                return
            
        self.owned_games.append({
            "obj": game,
            "play_time": 0,
            "favorited": False
        })

        print(f"Successfully bought {game.name} for {game.price}")

    def play_game(self):
        game = self.list_and_choose("play")
        if game == None: return

        hours = int_input(f"How may hours would you like to play {game['obj'].name} for? ")

        if hours < 1:
            print("You must play more than 0 hours!")
            self.play_game()
            return
        
        game["play_time"] += hours
        self.total_play_time += hours
        print(f"You played for {hours} hours. Total play time: {game['play_time']} hours")

    def favorite_game(self):
        game = self.list_and_choose("favorite")
        if game == None: return
        game_obj = game["obj"]

        if game["favorited"]:
            print(f"You already favorited {game_obj.name}")
            return

        print(f"Favorited {game_obj.name}")
        
        self.total_favorites += 1
        game["favorited"] = True

    def unfavorite_game(self):
        game = self.list_and_choose("unfavorite")
        if game == None: return
        game_obj = game["obj"]

        if not game["favorited"]:
            print(f"You don't have {game_obj.name} as a favorite")
            return
        
        print(f"Unfavorited {game_obj.name}")

        self.total_favorites -= 1
        game["favorited"] = False

    def delete_game(self):
        game = self.list_and_choose("delete")
        if game == None: return

        print(f"Removed {game['obj'].name} from your library")
        self.owned_games.remove(game)

    def swap_game_index(self):
        if len(self.owned_games) < 2:
            print("You must own at least 2 games in order to swap index")
            return

        game_1 = self.list_and_choose("choose to swap? (1)")
        print("------------------------")
        game_2 = self.list_and_choose("choose to swap? (2)")

        if game_1 == game_2:
            print("These games are already at the same index")
            return
        
        games = self.owned_games
        game_1_i = games.index(game_1)
        game_2_i = games.index(game_2)

        games[game_1_i], games[game_2_i] = games[game_2_i], games[game_1_i] 

        print(f"Index swapped, {game_1['obj'].name} is now index {game_2_i + 1} and {game_2['obj'].name} is now index {game_1_i + 1}")

    def list_game_details(self):
        game = self.list_and_choose("view details about")
        if game == None: return

        game["obj"].ask_property()
    
    def list_and_choose(self, action):
        if not self.list_library(): return None

        choice = range_input(f"\nWhich game would you like to {action}? ", max=len(self.owned_games)) - 1
        return self.owned_games[choice]
    
    def list_library(self):
        game_length = len(self.owned_games)
        
        if game_length == 0:
            print("You don't own any games")
            return False
        
        # print(f"You own {game_length} games")

        for i, game in enumerate(self.owned_games):
            print(f"\n{i + 1}: {game['obj'].name}")
            print(f"Price: {game['obj'].price}")
            print(f"Description:\n{game['obj'].short_description}")
            print(f"Your play time: {game['play_time']} hours")
            if game["favorited"]:
                print("⭐ You favorited this game")

        return True