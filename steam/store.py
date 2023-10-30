from steam.api import steam_request, urls
from steam.game import Game
from steam.utility import range_input, choice_input

sort_names = ["price", "date", "title length"]
sort_funcs = [
    lambda game: game.get("price") and game["price"]["final"] or 0,
    lambda game: game["id"],
    lambda game: len(game["name"]),
]

class Store:
    def __init__(self):
        self.recently_viewed = []

    def search(self):
        query = input("Enter search query: ")
        response = steam_request(urls["search"], {"term": query})

        ask_filter = input("Would you like to sort the results? (y/n) ").lower()
        sort_name = None
        if ask_filter == "y":
            sorting_by = choice_input("Would you like to sort by", sort_names) - 1
            sort = sort_funcs[sorting_by]
            sort_name = sort_names[sorting_by]

            # sorting_from = 1 and least to greatest or -1 and greatest to least
            sorting_from = choice_input(f"Would you like to sort from", ["least to greatest", "greatest to least"])
            sorting_from = 1 if 2 else -1

            response["items"].sort(key=lambda x: sort(x) * sorting_from)

        print(f"Search results for term '{query}'{f' sorting by {sort_name}' if sort_name else ''}")

        if len(response["items"]) == 0:
            print("No results found")
            return
        
        for i, game in enumerate(response["items"]):
            print(f"{i + 1}: {game['name']}")
            self.recently_viewed.append(game['name'])

        return response["items"]
    
    def select_search(self):
        items = self.search()
        if not items: return

        option = input("Which game would you like to select? (x to cancel, y to requery): ").lower()

        if option == "x":
            return
        
        if option == "y":
            return self.select_search()
        
        option = int(option) - 1
        return Game(items[option]["id"])

    def list_recent(self):
        if len(self.recently_viewed) == 0:
            print("No recent searches")
            return
        
        print("Recently searches:")
        
        for i, game in enumerate(self.recently_viewed):
            print(f"{i + 1}: {game}")