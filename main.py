# all(i in player.inventory for i in nadeRequest)

# Player classes --start--

class playerBase:
  def __init__(self, name):
    self.name = name
    self.inventory = []
    self.money = int(16000)
    self.alive = True

  def find(self, inputWeaponName):
    weaponName = (str(inputWeaponName)).lower()
    if weaponName in self.inventory:
      return True
    else:
      return False

class CT(playerBase):
  def __init__(self, name):
    super().__init__(name)
    self.inventory.append('usp')
    self.team = 'ct'

class T(playerBase):
  def __init__(self, name):
    super().__init__(name)
    self.inventory.append('glock')
    self.team = 't'

# Player classes --end-- 
# Function for printing available commands --start-- 

def printCommands():
  print("Available commands ~ ")

  print(" k <alivePlayerName> <deadPlayerName> <weaponName>")
  print("  Kill command. Specify which player kills which and with what weapon.")

  print(" b <playerName> <weaponName>")
  print("  Buy command. Specify the buying player and the bought weapon.")

  print(" pp")
  print("  Print players list.")

  print(" pwl")
  print("  Print weapons list.")

  print(" pwp <weaponName>")
  print("  Print weapon price. Specify the weapon name.")

  print(" pc")
  print("  Print commands. I.e. print this list")

  print(" e")
  print("  End round.")

# Function for printing available commands --end--  
# Guns and equipment related stuff --start--  

weapons = {"cz":500, "deagle":700, "dual":300, "57":500, "glock":200, "p2000":200, "p250":300, "r8":600, "tec9":500, "usp":200, "mag7":1300, "nova":1050, "sawedoff":1100, "xm":2000, "m249":5200, "negev":1700, "mac10":1050, "mp5":1500, "mp7":1500, "mp9":1250, "p90":2350, "bizon":1400, "ump":1200, "ak":2700, "aug":3300, "famas":2050, "galil":1800, "m4a1":2900, "m4a4":3100, "sg":3000, "awp":4750, "g3sg1":5000, "scar":5000, "ssg":1700, "flash":200, "smoke":300, "he":300, "molotov":400, "decoy":50, "incendiary":600, "zeus":200, "dkit":400, "kevlar":650, "kevlarhelm":1000}

weaponsSecondaries = (list(weapons.keys()))[0:10]
weaponsPrimaries = (list(weapons.keys()))[10:34]
weaponsCTnotBuy = ['glock', 'tec9', 'sawedoff', 'mac10', 'ak', 'galil', 'sg', 'g3sg1', 'molotov']
weaponsTnotBuy = ['57', 'p2000', 'usp', 'mag7', 'mp9', 'aug', 'famas', 'm4a1', 'm4a4', 'scar', 'incendiary', 'dkit']
weaponsBuyOnlyOnce = ['smoke', 'he', 'molotov', 'decoy', 'incendiary', 'zeus', 'dkit', 'kevlar']

def printPrice(inputWeaponName):
  name = (str(inputWeaponName)).lower()
  print(f"{name} price ~ {weapons[name]}")

def printWeaponsList():
  print("Weapons list ~")
  for key, value in weapons.items():
    print(f"{key} : {value}")

# Guns and equipment related stuff --end--  
# Creation of CT and T objects --start--

def createPlayers():

  playersNamesCT = list(set(input("Enter CT players' names > ").split(", ")))
  playersNamesT = list(set(input("Enter T players' names > ").split(", ")))

  if len((playersNamesCT + playersNamesT)) > len(set((playersNamesCT + playersNamesT))):
    return False

  global players
  players = []

  for i in playersNamesCT:
    x = CT(playerBase(i))
    players.append(x)

  for i in playersNamesT:
    x = T(playerBase(i))
    players.append(x)

  return True

def printPlayers():

  print(f"CT players ~")
  for i in players:
    if i.team == "ct":
      print(f" {i.name.name.capitalize()} : {i.money}")
      print(f"  {i.inventory}")
  
  print(f"T players ~")
  for i in players:
    if i.team == "t":
      print(f" {i.name.name.capitalize()} : {i.money}")
      print(f"  {i.inventory}")

# Creation of CT and T objects --end--
# Round logic --start--

def round(inputRoundNumber):
  roundNumber = inputRoundNumber 
  action = input(f"Input round nº {roundNumber} action > ").split(" ")

  if 'k' == str(action[0]):
    print("k1")

  elif 'b' == str(action[0]):
    buy(action[1], action[2])

  elif 'pp' == str(action[0]):
    printPlayers()

  elif 'pwl' == str(action[0]):
    printWeaponsList()

  elif 'pwp' == str(action[0]):
    printPrice(str(action[1]))

  elif 'pc' == str(action[0]):
    printCommands()

  elif 'e' == str(action[0]):
    return True

  else:
    print("Unknown command ~ ")

  return False

def buy(inputPlayerName, inputWeaponName):

  playerName = str(inputPlayerName).lower()
  weaponName = str(inputWeaponName).lower()

  # Check for mistakes in input playerName and weaponName
  if weaponName in weapons and any(i.name.name == playerName for i in players):
    print("weapon and player exist") # Success message

    player = next((x for x in players if x.name.name == playerName)) # Player exists, so we can fetch its object

    price = weapons.get(inputWeaponName) # Weapon exists, so we can get its price

    # Now we need to check if the player can actually buy the weapon
    # Depends on the player's current inventory, team, and money  
    # If the player belongs to a team, they will not be able to buy certain weapons. Let's check that after figuring out if the player has enough money to buy the weapon

    # Checking price
    if player.money >= price:

      print("money check") # Success message

      # Checking team restrictions
      if (weaponName in weaponsCTnotBuy and player.team == "ct") or (weaponName in weaponsTnotBuy and player.team == "t"):
        print("team restriction fail") # Error message

      else:

        print("team restriction check successful (can buy)") # Success message

        # This means that the player can buy a weapon
        # Now we need to check if the player already owns such gun or already owns a gun of the same category. There are also some restrictions regarding flashbangs and kevlar vest/helmets
        # Let's first check if the weapon is a primary, secondary, flashbang, or kevlar/helm

        if weaponName in weaponsPrimaries:

          print("primary check") # Success message

          for i in player.inventory:
            if i in weaponsPrimaries:
              player.inventory.remove(i)

          print("buy successful") # Success message
          player.money = player.money - price
          player.inventory.append(weaponName)

        elif weaponName in weaponsSecondaries:

          print("secondary check") # Success message

          for i in player.inventory:
            if i in weaponsSecondaries:
              player.inventory.remove(i)

          print("buy successful") # Success message
          player.money = player.money - price
          player.inventory.append(weaponName)

        elif weaponName == 'flash':

          print("flash check") # Success message

          # Rule here is that a player can have a maximum of two flashes

          flashcount = int(0)

          for i in player.inventory:
            if i == "flash":
              flashcount += 1

          if flashcount < 2 or flashcount == 0:
            print("buy successful") # Success message
            player.money = player.money - price
            player.inventory.append(weaponName)

          else:
            print("buy unsuccessful") # Error message

        elif weaponName == 'kevlarhelm':

          print("kevlarhelm check") # Success message

          # If player already owns a 'kevlar' and that vest is in perfect state, 'kevlarhelm' price will be 350, not 1000. Requires further input from the user

          for i in player.inventory:
            if i == "kevlar":
              kevlarInPerfectState = input(f"Is {playerName}'s kevlar in perfect state? (y/n) > ").lower()

              if kevlarInPerfectState == "y":
                price = 350
                
              print("buy successful") # Success message
              player.money = player.money - price
              player.inventory.append(weaponName)

        else:
          if weaponName in player.inventory and weaponName not in weaponsBuyOnlyOnce:
            player.inventory.remove(weaponName)
            print("buy successful") # Success message
            player.money = player.money - price
            player.inventory.append(weaponName)
          elif: 


    else:
      print("player does not have enough money") # Error message

  else:
    print("weapon or player not exist") # Error message

# Round logic --end--
# Main process --start--

end = False
firstTimeExec = False

while end == False:

  while firstTimeExec == False:
    firstTimeExec = createPlayers()

  end = round(10)

# Main process --end--
