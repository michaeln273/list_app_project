from steam.api import steam_request, urls
from steam.utility import range_input

# Game class, stores properties relevant to the game class as well as
# as well as providing functionality to view certain properties of the object
# By asking for user input
class Game:
  def __init__(self, id):
    self.id = str(id)
    self.fetch()

  def fetch(self):
    response = steam_request(urls["details"], {"appids": self.id})

    if response == None:
      print("Invalid game id")
      return

    details = response[self.id]["data"]

    self.name = details["name"]
    self.description = details["detailed_description"]
    self.short_description = details["short_description"]
    self.website = details["website"]
    self.developers = details["developers"]
    self.publishers = details["publishers"]
    self.price = self._format_price(details.get("price_overview"))
    self.support_url = details["support_info"]["url"]
    self.support_email = details["support_info"]["email"]
    self.release_date = details["release_date"]["date"]

  def _format_price(self, price):
    if not price: return "Free"

    initial = price["initial_formatted"]
    now = price["final_formatted"]

    if initial == now or initial == "":
      return now

    return f"Initially {initial}, now {now}"

  def ask_property(self):
    print("What would you like to view?:")

    names = list(self.__dict__.keys())
    values = list(self.__dict__.values())

    for i, name in enumerate(names):
      print(f"{i + 1}: {name.title().replace('_', ' ')}")

    option = range_input("Enter option here: ", max=len(values)) - 1
    value = values[option]

    if type(value) == list:
      print(f"There are {len(value)} {names[option]}:")

      for item in value:
        print(item)

      return

    print(value)
