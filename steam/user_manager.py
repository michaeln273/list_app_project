from steam.user import User
from steam.store import Store
from steam.game import Game
from steam.utility import range_input
import json

min_user_len = 3
max_user_len = 20

class UserManager:
    def __init__(self, save_location):
        self.store = Store()
        self.users = []
        self.active_user = None
        
        self.save_location = save_location
        self.load_data()

    def save_data(self):
        serialized = {}

        for user in self.users:
            serialized[user.username] = [
                [],
                user.total_play_time,
                user.total_favorites
            ]
            
            for game in user.owned_games:
                serialized[user.username][0].append([
                    game["obj"].id,
                    game["play_time"],
                    game["favorited"]
                ])

        with open(self.save_location, "w") as save:
            json.dump(serialized, save)

    def load_data(self):
        parsed = {}
        
        with open(self.save_location, "r") as save:
            try:
                parsed = json.load(save)
            except ValueError as e:
                pass

        for username, properties in parsed.items():
            user = User(self.store, username)
            
            user.owned_games = []
            for game in properties[0]:
                user.owned_games.append({
                    "obj": Game(game[0]),
                    "play_time": game[1],
                    "favorited": game[2]
                })

            user.total_play_time = properties[1]
            user.total_favorites = properties[2]
            
            self.users.append(user)

    def create_user(self):
        username = input(f"Enter username ({min_user_len} min chars, {max_user_len} max chars): ")

        user_len = len(username)
        if user_len < min_user_len or user_len > max_user_len:
            print("Does not meet username requirements, try again")
            self.create_user()
            return
        
        for user in self.users:
            if user.username == username:
                print("This username is already taken, choose another one")
                self.create_user()
                return
        
        user = User(self.store, username)
        self.users.append(user)

        print(f"Created user with username {username}")

        return user

    def select_account(self):
        choice = self.list_and_choose("select")
        user = None
        
        if choice == None:
            print("Creating account")
            user = self.create_user()
        else:
            user = self.users[choice]

        self.active_user = user

        print(f"Set {user.username} to the active user")

    def delete_account(self):
        choice = self.list_and_choose("delete")
        if choice == None: return

        print(f"Removed {self.users[choice].username}")
        self.users.pop(choice)

    def list_and_choose(self, action):
        if not self.list_users(): return None

        choice = range_input(f"Which account would you like to {action}? ", max=len(self.users)) - 1
        return choice
    
    def list_users(self):
        if len(self.users) == 0:
            print("There are no accounts")
            return False
        
        for i, user in enumerate(self.users):
            print(f"{i + 1} - {user.username}:")
            print(f"Total play time: {user.total_play_time}")
            print(f"Total games owned: {len(user.owned_games)}")
            print(f"Total favorites: {user.total_favorites}\n")

        return True