from steam.user_manager import UserManager
from steam.utility import range_input
import os

def clear_output():
    os.system("clear")

class Format:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

class DisplayManager:
    def __init__(self):
        manager = UserManager("./save.json")
        manager.select_account()
        clear_output()

        user = manager.active_user
        store = manager.store

        self.options = {
            "Shop": [
                ["View steam catalog", store.search],
                ["View recent searches", store.list_recent]
            ],
            "Account": [
                ["Purchase a game", lambda: manager.active_user.purchase_game()],
                ["Play a game", lambda: manager.active_user.play_game()],
                ["Favorite a game", lambda: manager.active_user.favorite_game()],
                ["Unfavorite a game", lambda: manager.active_user.unfavorite_game()],
                ["Delete a game", lambda: manager.active_user.delete_game()],
                ["List your game library", lambda: manager.active_user.list_library()],
                ["View details on a game you own", lambda: manager.active_user.list_game_details()]
            ],
            "Other": [
                ["Get active account name", lambda: print(manager.active_user.username)],
                ["Back to account selector", manager.select_account],
                ["Create a new account", manager.create_user],
                ["Save", self.save],
                ["Save and quit", self.quit]
            ]
        }

        self.user = user
        self.store = store
        self.manager = manager

    def poll_choices(self):
        options = self.options
        
        self.format_header()

        i = 0
        single_choices = []
        for category, choices in options.items():
            print(f"-------{Format.BOLD}{category}{Format.END}-------")
            for choice in choices:
                i += 1
                print(f"{Format.BOLD}{i}{Format.END}: " + choice[0])
                single_choices.append(choice)

            print()

        choice = range_input("Enter choice: ", max=i) - 1
        clear_output()

        self.format_header()
        print(f"Selected prompt: {Format.BOLD}{Format.UNDERLINE}{single_choices[choice][0]}{Format.END}")
        single_choices[choice][1]()

        input("Press enter to continue to options: ")
        clear_output()
        self.poll_choices()
    
    def format_header(self):
        user = self.manager.active_user
        name = user.username
        favorites = user.total_favorites
        play_time = user.total_play_time
        games = len(user.owned_games)

        print(f"Logged in as {Format.BOLD}{name}{Format.END} - ⭐ {favorites}  ⌛ {play_time}  🎮 {games}\n")

    def save(self):
        print("Saved")
        self.manager.save_data()

    def quit(self):
        clear_output()
        self.save()
        exit()

clear_output()
manager = DisplayManager()
manager.poll_choices()