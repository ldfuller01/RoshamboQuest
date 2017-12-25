# https://repl.it/MixQ

import random
from time import sleep

# Make sure to include *look at inventory* or something related in each room
end = 0
list_complete = False

inventory = ["grocery list"]
item_descriptions = {
  "grocery list" : {
    "toamato" : False,
    "bacon" : False,
    "dozen eggs" : False,
    "oranges" : False,
    "rotisserie chicken" : False,
    "banana" : False,
    "blue berries" : False,
    "watermelon" : False,
    "apple" : False
  }
  # "item" : "description",
  # etc.
}
rooms_visited = [1]
next_room = 1


# Directional Lists and Other Response Lists
north = ["go north", "north", "n"]
south = ["go south", "south", "s"]
west = ["go west", "west", "w"]
east = ["go east", "east", "e"]
_help = ["help", "help me", "guide", "help koob", "koob help", "help me koob", "koob help me", "talk to koob", "talk to book"]
_map = ["open map", "map", "show map", "look at map", "check map"]


# When user enters inapplicable response, i.e. "climb tree" when there is no tree there.
unknown_responses = ["Huh? I'm not sure what you mean.", "You must be seeing things; try something else."]


# Prints with empty line above and below text; this is intentional.
map_legend = """
'-' = Unexplored
'o' = Explored
'X' = Current location
"""


# '0,0' = top left corner; '0,1' = far left on second row
map_coords = {
  '4,0' : 18,
  '5,0' : 15,
  '1,1' : 34,
  '4,1' : 17,
  '5,1' : 14,
  '0,2' : 33,
  '1,2' : 32,
  '3,2' : 26,
  '4,2' : 16,
  '5,2' : 13,
  '0,3' : 31,
  '1,3' : 30,
  '2,3' : 27,
  '3,3' : 25,
  '5,3' : 11,
  '6,3' : 12,
  '1,4' : 29,
  '2,4' : 28,
  '3,4' : 24,
  '5,4' : 10,
  '6,4' : 9,
  '1,5' : 21,
  '2,5' : 20,
  '3,5' : 19,
  '4,5' : 4,
  '5,5' : 5,
  '6,5' : 6,
  '2,6' : 22,
  '4,6' : 1,
  '6,6' : 8,
  '7,6' : 7,
  '2,7' : 23,
  '4,7' : 2,
  '4,8' : 3
}

#--------------------------------------
#----- True is "locked", False is "unlocked" -----
#--------------------------------------
locked_doors = {
  "2" : True,
  "fridge" : True,
  "chest" : True,
  "rock" : True,
  "silver key" : True,
  "fishing man" : True,
  "ent" : True,
  "leprechaun" : True,
  "blue berries" : True,
  "dead bodies" : True,
  "giant stone scissors" : True,
  "banana" : True,
  "silver lock" : True, # fridge = golden lock
  "old man dialogue" : True,
  "coffee cup" : True,
  "bus" : True,
  "water fountain" : True,
  "stone bird" : True,
  "lumberjack_bonemeal" : True,
  "lumberjack_pancakes" : True,
  "lumberjack_pickaxe" : True,
  "leaf lump" : True,
  "stone fist" : True,
  "????????? encouragement" : True,
  "mountain man" : True,
  "dwarf" : True,
  "goat hair cut" : True,
  "nut hole" : True,
}

#-----------------------------------------------------------
#----- Dictionary of every single obtainable item and their state -----
#-----------------------------------------------------------
items_taken = {
  "koob" : False,
  "golden key" : False,
  "tomato" : False,
  "magic paper" : False,
  "bacon" : False,
  "key" : False,
  "silver key" : False,
  "dozen eggs" : False,
  "worm" : False,
  "blank leaf" : False,
  "cane stick" : False,
  "fishing pole cane" : False,
  "leprechaun" : False,
  "points" : False,
  "pills" : False,
  "blue berries" : False,
  "pancakes" : False,
  "bonemeal" : False,
  "banana" : False,
  "nireal book" : False,
  "cup" : False,
  "square" : False,
  "pistol" : False,
  "oranges" : False,
  "pickaxe" : False,
  "grass" : False,
  "cup of water" : False,
  "rotisserie chicken" : False,
  "watermelon" : False,
  "magic scissors" : False,
  "apple" : False,
  "green cap" : False,
  "ice picks" : False,
  "magic rock" : False,
  "river rock cane" : False,
  "sign post" : False,
  "shovel" : False,
  "scissors" : False,
}


# Gives user a map of visited and unvisited locations.
def display_map(current_room):
  for y in range(9):
    print()
    for x in range(8):
      if str(x) + "," + str(y) in map_coords:
        if map_coords[str(x) + ',' + str(y)] == current_room:
          print("X",end=" ")
        elif map_coords[str(x) + "," + str(y)] in rooms_visited:
          print("O",end=" ")
        else:
          print("-",end=" ")
      else:
        print("-",end=" ")

        
# ----- Delayed Text
def roll_text(text):
  for c in text:
    print(c, end='')
    sleep(0.01)
  print("\n")

# This is entirely for the Cane fragments
def acquire_cane(item_name):
  items_taken[item_name] = True
  roll_text("Item collected: 1/3 of Cane.")
  fragments = 0
  frag_names = []
  for item in inventory:
    if "cane" in item:
      fragments += 1
      frag_names.append(item)

  if fragments < 2:
    inventory.append(item_name)
    item_descriptions[item_name] = "One third of the Cane."
    roll_text("You now have " + str(fragments) + "/3 of the Cane.")
  else:
    for frag in frag_names:
      inventory.remove(frag)
    inventory.append("cane")
    roll_text("You have completed the Cane!")


# Function for Book Guide. Book's name is Koob.
def guide(current_room): # All strings MUST be in brackets, or random.choice will only select one letter at a time.
  room_dialogue = {
    1 : ["That arch looks fancy, although I have no idea who made it...", "You need help? Stop asking me then! There's a perfectly good bush to the right there..."],
    2 : ["Help you get past paper? No can do, I'm paper too, so I can't go telling you that you need to cut a hole in it to get, past... Oops."],
    3 : ["I don't think I can help you beside telling you need a key, which is obvious. I mean, I've never been outside of my world..."],
    4 : ["It's the chest I was stuck in! Man, I was in there for hours, some person with a hood locked me in there, not that I could do anything sitting on a table anyways...", "Hey, I think the person who locked me up dropped something in that bush over there."],
    5 : ["I don't know what you need help with... I mean there's a path to the north and some trees to the east, maybe you can even go west from where you found me."],
    6 : ["You may want to see to getting those nuts from the ground, it could be a useful experience.", "Perhaps there is something in that tree, and don't worry, you won't fall, I think..."],
    7 : ["Hmmmmmmm, I wonder what you should do with the eggs the mother bird left.... I WONDER???", "I bet you you can't fall out of the tree! You know why you'll lose the bet? Cause it's not programmed in the game, HAH!"],
    8 : ["I don't know what the prophecy means when it says \"achieve\", but I think it means you need scissors for something.", "Oh if you didn't know, you can use the roots to climb back up. I hope you knew that.", "Aww man, I hate this place, someone brought me here and dragged me along the wall."],
    9 : ["Hey, instead of helping you, you should help me. Ask them what it's like when you're turned to paper.", "If you help that Ent perhaps he'll give you something VERY important in return."],
    10 : ["Hey, you should walk across the rope bridge! Cause, uhh, I need to see my dealer...", "I think that angler needs help, or maybe he just wants everyone to leave him alone because they're all annoying. Or he's just asleep, I wanna bet he's sleeping."],
    11 : ["I think you'll find good things at the end of that rainbow, wait nevermind, I hear chuckling.", "Man it sure is windy, it feels like it's coming from that cave over there in the rocky hill. Wait, did I spoil your exploration? Oops, sorry..."],
    12 : ["I think you can take that gold, I mean nobody else is here to use it, besides that chuckling midget...", "That midget looks like he could take a nap, perhaps some pills would help?"],
    13 : ["I feel like something's watching us, some all seeing eye perhaps? I wonder if we can talk to it...?"],
    14 : ["Man, wish I could eat things, cause those pancakes look good, good enough for a lumber jack!", "That throne looks fit for a king, like me! Or a greedy midget I guess..."],
    15 : ["That banana looks real nice.", "Just talk to the Goblin already! Not like he's gona bite you..."],
    16 : ["Paths are usually made for people to follow."],
    17 : ["You know how to play roshambo right? Or have you not heard of it? You just need a rock ok... But it has to be a fancy rock.", "Man, don't I feel sorry for those lumps, they probably had to be here a looooooooooooooooooooooooong time, but not longer than me!"],
    18 : ["Hey, that golden key isn't gaurded by antyhing. ... What I'm saying is that you can straight up take it!", "That book... I don't like it, now don't try making me jealous either, I'll just fly away."],
    19 : ["If you don't intend to dig up that patch, move on out of here! I'm getting bored...", "You should get a giant spoon, scoop up that patch of loose dirt, and eat it! Or whatever you find, but dirt can be good for you."],
    20 : ["I don't think I can help you with this one, that old man, I've never seen him before...", "That old man looks weird... You should go talk to him! Cause I don't want to!"], 
    21 : ["Hey, that cup of java, or used to be java, you should use it for something.", "Look at that dumb square just sitting there, I think you should take him, ruin his fun. *Deeply Chuckles*"],
    22 : ["Eww, an old smells stinky... You should go in it, but you have to be holding the stupid square. I don't why, it's really stupid."],
    23 : ["You see those oranges, yeah, you can take those if you wanted.", "Woah, now that's my kind of weapon, a B23R pistol, bummer though, we have to have 1000 points..."],
    24 : ["You see that weirdo dwarf over their?"],
    25 : ["Mmm, that water looks very tasty. If only you had some kind of container which could help you carry some of that water with you.", "Grass. Such green beautiful nature goodness. Oh, look, all that happiness is right there in a bag over there!"],
    26 : ["This bird looks trapped in its stone bonds. If only it could find some magical escape to freedom."],
    27 : ["If there's a fork in the road, take it. I mean, if there's another path take that too, but forks can be pretty useful too..."],
    28 : ["That lumberjack's axe looks so sharp, it looks like he could split another tool with it!", "This lumberjack looks very hungry. If you ask me, he looks like a breakfast kind of guy."],
    29 : ["That green cap is begging to be taken. Really, if the dead person who owned it cared about it, they'd be buried with it!", "Oh look, an apple tree. Apples are very tasty."],
    30 : ["Where does that rope go? No one knows! But *you* would know if you climbed it.", "Sometimes, your hair just gets too long and you need a good ol' haircut."],
    31 : ["GOOOAAATTTS!!! They really seem to eat everything, but they also seem to really like grass.", "When I'm having trouble sleeping, I sure love me some sleeping pills."],
    32 : ["I love playing rock-paper-scissors, and that stone fist looks like it's playing a Rock.", "Hmm, what could possibly be in that lump of snow?", "You see the top of the mountain right? Maybe we could climb up there with a pickaxe split in half. WEIRD?! Well sorry for throwing ideas out there..."],
    33 : ["Who is this hooded figure?... What does it want?... I can't talk to it, but you can!", "Hey, *spssst*, these may be spoilers, but I think she wants some food..."],
    34 : ["Man, this view up here sure is beautiful. Except there's a small man in the way of it all. Talk to that guy and get him out of my way!"]
  }
  
  roll_text(random.choice(room_dialogue[current_room]))


# Here is the function for displaying the players inventory
def backpack():
  roll_text("Backpack : ")
  if len(inventory):
    for item in inventory:
      print(item.title())

  else:
    roll_text("There are some dust bunnies, but nothing else... At all... ")

  
# ------------------
# ----- Room 1 -----
# ------------------
def _01():
  if locked_doors["goat hair cut"]:
  	roll_text("You see a large stone gate to the north of you with groomed bushes on either side. It leads into a dark forest.")
  else:
    roll_text("You see a large stone gate to the north of you with groomed bushes on either side, although, there is now a goat munching on the left bush.")
  
  sleep(0.5)
  while True:
    answer = input(">").lower()
    
    if answer in north or answer in ["enter forest", "enter dark forest", "walk into forest", "go into forest"]:
      next_room = 4
      break
    elif answer in east:
      roll_text("There's a spooky infinite abyss over there, you shouldn't go there!")
    elif answer in south:
      next_room = 2
      break
    elif answer in west:
      roll_text("You hit your face on a brick wall trying to go west. Perhaps try another direction.")

    elif answer in ["look at right bush", "check right bush", "search right bush"] and not items_taken["tomato"]:
      roll_text("You find a tomato growing from the right bush.")
      locked_doors["tomato"] = False
    
    elif answer in ["look at right bush", "check right bush", "search right bush"]:
      roll_text("What do you mean tomato? There's no tomato.")

    elif answer in ["look at left bush"]:
      roll_text("There's nothing special about this bush...")

    elif answer in ["look at bushes", "look at bush"]:
      roll_text("There are two bushes, and they're too far apart to look at side by side...")

    elif answer in ["look at gate", "look at stone gate", "look at large stone gate"]:
      roll_text("The stone arch acts as a gateway into the mysterious forest, weird symbols engraved on the front of it.")

    elif answer in ["look at words", "look at engraved words", "look at weird symbols", "look at engraved symbols", "look at symbols"]:
      roll_text("You look closer at the symbols on the gate, although you can't read them.")
    
    #take tomato actions
    elif answer in ["take tomato", "pick up tomato", "pick tomato"] and not items_taken["tomato"] and not locked_doors["tomato"]:
      roll_text("You rip the tomato off of the bush, stuffing it in your backpack. It's still intact for some reason.")
      items_taken["tomato"] = True
      inventory.append("tomato")
      roll_text("*You have acquired Tomato*")
      roll_text("You have checked off Tomato from the grocery list.")
    
    elif answer in ["take tomato", "pick up tomato", "pick tomato"]:
      roll_text("You already have a tomato, too many can be too acidic!")
      
    
    elif answer == "":
      print()
    
    #look at goat action
    elif answer in ["look at goat"] and not locked_doors["goat hair cut"] and locked_doors["????????? encouragement"] and items_taken["magic rock"]:
      roll_text("The goat is just standing there eating the bus, although it does look a bit more civilized in a way.")
    
    elif answer in ["look at goat"]:
      roll_text("It's just a goat eating a bush, nothing abnormal about him.")
    
    #talk to goat action
    elif answer in ["talk to goat"] and not locked_doors["goat hair cut"] and locked_doors["????????? encouragement"] and items_taken["magic rock"]:
      roll_text("Goat : Hmm? You actually want to talk to me? What a pleasant surprise, there aren't many people now a days who actually attempt to talk to us animals.")
      sleep(.5)
      roll_text("Goat : Well anyways, I give you my thanks for checking in on me after I ran out of the barber. Oh, I bet you want to know why I'm eating this bush instead of the other?")
      roll_text("Goat : The reason behind it is that that bush is a tomato bush, which, I utterly despise. I mean tomatos are just fine, it's the bush I hate! They're just so un-natural!")
      sleep(1)
      roll_text("Goat : Well, again, thanks for checking in on me.")
      sleep(2)
      roll_text("????????? : Oh also, you know that one kid in your school that's always alone and looking down at the ground? Perhaps you can go say hi to them, acknowledgement is all they're looking for.")
      roll_text("????????? : Why am I asking you to do such a task? Well, you decided to talk to a goat, so why not a person?")
      
      locked_doors["????????? encouragement"] = False
    
    elif answer in ["talk to goat"] and not locked_doors["goat hair cut"]:
      roll_text("Goat : ~BBEEHHEEHH~")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
    	if items_taken["koob"]:
    		guide(1)
    	else:
    		roll_text("You don't need help in the first room, do you??")
    
    # Map command
    elif answer in _map:
      if items_taken["koob"]:
      	display_map(1)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()
    
		# If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

  
# ------------------
# ----- Room 2 -----
# ------------------
def _02():
  roll_text("You see a giant magical paper wall blocking your way. You have no idea how to get around it.")
    
  while True:
    answer = input(">").lower()
        
    # If player wants to travel in a direction
    if answer in north:
      next_room = 1
      break
        
    elif answer in south and not locked_doors["2"]:
      next_room = 3
      break

    elif answer in south:
      roll_text("The magical paper wall prevents you from traveling further...")
        
    elif answer in west:
      roll_text("You're too horrified of the paper wall to walk along side it.")
          
    elif answer in east:
      roll_text("You're too afraid that the paper will eat your right ear.")
        
    # If player wants to use items
    elif answer in ["use magic scissors on paper wall", "use magic scissors"] and "magic scissors" in inventory and not items_taken["magic paper"]:
      locked_doors["2"] = False
      roll_text("You have cut a door sized hole in the paper wall.")
      inventory.append("magic paper")
      items_taken["magic paper"] = True
      roll_text("You have aquired Magic Paper.")
        
    # If the player has already used an item here
    elif answer in ["use magic scissors on paper wall", "use magic scissors"] and "magic scissors" in inventory:
      roll_text("You've already cut a hole in the paper wall, haven't you already caused it enough pain?")
        
    # If you need help from Koob, cause why not?
    elif answer in _help and items_taken["koob"] == True:
      guide(2)
      
    # Map command
    elif answer in _map:
      if items_taken["koob"]:
      	display_map(2)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()
    
		# If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))
          
  return inventory, next_room, locked_doors, items_taken


# ------------------
# ----- Room 3 -----
# ------------------
def _03():
  if locked_doors["fridge"]:
    roll_text("You approach a mini fridge in what seems like a pure white plain. In the mini fridge window you see a package of bacon, although quite sadly, the fridge has a golden padlock on it.")
  else:
    if items_taken["bacon"]:
      roll_text("You approach a mini fridge in what seems like a pure white plain; an unlocked golden padlock hangs on it. In the mini fridge window you see some crumbs and empty shelves, but no bacon. RIP.")
    else:
      roll_text("You approach a mini fridge in what seems like a pure white plain; an unlocked golden padlock hangs on it. In the mini fridge window you see a package of bacon. Tasty, tasty bacon...")
  
  while True:
    answer = input(">").lower()
    
    if answer in north:
      next_room = 4
      break
    elif answer in east:
      roll_text("Looks like there's endless whiteness over there. Probably not worth going that way.")
    elif answer in south:
      next_room = 2
      break
    elif answer in west:
      roll_text("Oh no, the wind is too strong, and you are too lazy to walk against it!")
    
    elif answer in ["open fridge", "unlock fridge", "open mini fridge", "unlock mini fridge", "open minifridge", "unlock minifridge"]:
      if locked_doors["fridge"]:
        if "golden key" in inventory:
          locked_doors["fridge"] = False
          inventory.remove("golden key")
          roll_text("You opened the fridge.")
          if not items_taken["bacon"]:
          	roll_text("You see the bacon inside of the fridge. It calls your name...")
        else:
          roll_text("Looks like you'll need a golden key for that golden lock there.")
      else:
        if items_taken["bacon"]:
          roll_text("You see empty shelves in the fridge. Alas, the bacon has been taken.")
        else:
          roll_text("You see the bacon inside of the fridge. It calls your name...")
    
    elif answer in ["take bacon", "get bacon", "grab bacon", "pick up bacon"]:
      if items_taken["bacon"]:
        roll_text("What bacon? There's no bacon here.")
      else:
        items_taken["bacon"] = True
        inventory.append("bacon")
        item_descriptions["bacon"] = "Tasty, tasty bacon."
        item_descriptions["grocery list"]["bacon"] = True
        roll_text("You took the bacon from the fridge.")
        sleep(0.25)
        roll_text("Grocery list item complete: Bacon!")
    
    elif answer in ["look at fridge", "look at minifridge"]:
      if locked_doors["fridge"]:
        roll_text("The fridge has a golden padlock on it. You can see the bacon inside.")
      else:
        if items_taken["bacon"]:
          roll_text("The golden padlock on the fridge is open, and there is no bacon inside the fridge.")
        else:
          roll_text("The golden padlock on the fridge is open. You see the bacon in there...")


    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(3)
      else:
        roll_text("You're in the middle of nowhere. It's not like there's some book here to help you.")
    
    # Map command
    elif answer in _map:
      if items_taken["koob"]:
        display_map(3)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))
    
  return inventory, next_room, locked_doors, items_taken
    
  
# ------------------
# ----- Room 4 -----
# ------------------
def _04():
  if locked_doors["chest"]:
  	roll_text("You find a small table with a locked chest on top. There's also a stone under the table and a bush to the left of the table.")
  else:
    roll_text("You find a small table with a open chest on top. There's also a stone under the table and a bush to the left of the table.")
  
  while True:
    answer = input(">").lower()
    
    # Map
    if answer in _map:
      if items_taken["koob"]:
      	display_map(4)
      else:
        roll_text("Need a map? The book in that chest has one *winky face*.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(4)
      else:
        roll_text("If you need help, there's a book in that chest...")
    
    # Movement
    elif answer in north:
      roll_text("A large ravine filled with water is in the way, I don't think you want to go that way.")
      
    elif answer in south:
      next_room = 1
      break
    
    elif answer in west:
      next_room = 19
      break
    
    elif answer in east:
      next_room = 5
      break
    
    # Chest Actions
    elif answer == "look at chest" and locked_doors["chest"]:
      roll_text("The chest is locked with a grey padlock.")
      
    elif answer == "look at chest" and not items_taken["koob"]:
      roll_text("The lock is lying next to the open chest with a book in it.")
    
    elif answer == "look at chest":
      roll_text("The lock is lying next to the open chest which is empty.")
    
    elif answer in ["unlock chest", "open chest", "use key on chest"] and "key" in inventory and locked_doors["chest"]:
      roll_text("You unlock the chest, revealing a book.")
      inventory.remove("key")
      locked_doors["chest"] = False
    
    elif answer == "unlock chest" and not locked_doors["chest"]:
      roll_text("You've already unlocked the chest.")
    
    elif answer == "open chest" and not locked_doors["chest"]:
      if items_taken["koob"] == True:
        roll_text("The chest is empty, as if someone took something from it recently.")
      
      else:
        roll_text("You see a book, but for some reason it has a face and looks irritated?")
        
    elif answer == "unlock chest":
      roll_text("You can't open the chest without a key, and I don't think fingernails will work either")
    
    elif answer == "open chest":
      roll_text("It appears the lock is preventing you from opening the chest. I suggest either getting the key, or go work out more.")
    
    # Koob Actions
    elif answer in ["take book", "pick up book"] and not locked_doors["chest"] and not items_taken["koob"]:
      roll_text("You picked up Koob, although he looks angry, like he doesn't want to be here.")
      sleep(.5)
      roll_text("Koob : Uhh, thanks for saving me? Now don't bother me too much, but if you dooooo need help, just call for me... I guess...")
      items_taken["koob"] = True
    
    elif answer in ["take book", "pick up book"]:
      roll_text("Book? What are you talikng about?")

    elif answer in ["look at book", "look at koob"] and not items_taken["koob"] and not locked_doors["chest"]:
      roll_text("You look at the book, with a curious look. It looks back with an annoyed stare...")
      sleep(1)
      roll_text("Koob : Why are you looking at me? Just pick me up already!")

    elif answer in ["look at book", "look at koob"]:
      roll_text("There is no book here stranger.")
    
    # Stone Actions
    elif answer in ["look at stone", "look at rock"] and not items_taken["key"]:
      roll_text("It's just a rock, except it's slightly elevated, looks like a small key under it.")

    elif answer in ["pick up stone", "move stone", "lift stone", "pick up rock", "move rock", "lift rock"]:
      roll_text("You moved the rock to reveal a small key.")
      locked_doors["rock"] = False
    
    elif answer in ["look at stone", "look at rock"]:
      roll_text("It's just a plane ol' rock...")
      
    
    # Key Actions
    elif answer in ["pick up key", "take key", "pick up small key", "take small key"] and not locked_doors["rock"] and not items_taken["key"]:
      roll_text("You have picked up the Key covered in rollie pollies.")
      inventory.append("key")
      items_taken["key"] = True
      
    elif answer in ["pick up key", "take key", "pick up small key", "take small key"]:
      roll_text("What do you mean? What key? I don't see any ke-, I mean, You don't see any key.")
    
    # Bush Actions
    elif answer in ["look at bush", "look at left bush"] and not items_taken["silver key"]:
      roll_text("The bush is very green and leafy, although you also see a silver key hidden in the leaves.")
      locked_doors["silver key"] = False

    elif answer in ["look at bush", "look at left bush"]:
      roll_text("The bush is very green and leafy.")
    
    # Silver Key Actions
    elif answer in ["take silver key", "pick up silver key"] and not locked_doors["silver key"] and not items_taken["silver key"]:
      roll_text("You have picked up the Silver Key, covered in lady bugs...")
      inventory.append("silver key")
      items_taken["silver key"] = True
    
    elif answer in ["take silver key", "pick up silver key"]:
      roll_text("You see a silver key? Where? I can sell it and feed my family! Wait, there's no silver key... *silently weeps*")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()
  
  return inventory, next_room, locked_doors, items_taken
      
      
# ------------------
# ----- Room 5 -----
# ------------------
def _05():
  roll_text("You see a dirt path leading to the north and to the east. In the east, you see some trees, and birds flying all around.")
  looked_at_sky = False
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
      	display_map(5)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      next_room = 10
      break
    elif answer in east:
      next_room = 6
      break
    elif answer in south:
      roll_text("There's no path in that direction, and you are afraid to take risks! Return to comfort zone!")
    elif answer in west:
      next_room = 4
      break
    
    elif answer in ["look up", "look upward", "look at sky"]:
      if looked_at_sky:
      	roll_text("You see an empty blue sky. So interesting.")
      else:
        roll_text("Hey! Don't look at me— I mean, aaah! *hides from sight*")
        looked_at_sky = True
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(5)
      else:
        roll_text("You're in the middle of nowhere. Help won't do you much good unless you don't know how to walk.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

  
# ------------------
# ----- Room 6 -----
# ------------------
def _06():
  if 8 not in rooms_visited:
    roll_text("You walk into the tree grove. You see one tree that towers over all of the others. There is a squirrel nearby, sorting its stash of nuts in a small hole. There's also a strange set of trees to the North.")
  else:
    roll_text("You walk into the tree grove. You see one tree that towers over all of the others. Nearby, a squirrel sorts its nuts by a large hole in the ground. There's also a strange set of trees to the North.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(6)
      else:
        roll_text("What map? You don't have a map, silly goose.")

    # Navigation
    elif answer in north:
      next_room = 9
      break
    
    elif answer in east:
      roll_text("You walk eastward but smack into a tree. Perhaps you should climb it?")
      
    elif answer in south:
      roll_text("Trees block your path...")
    
    elif answer in west:
      next_room = 5
      break

    # Look at stuff actions
    elif answer in ["look at nuts"] and locked_doors["nut hole"]:
      roll_text("Those nuts seem to be tempting you into taking them, although that squirrel looks ominous...")

    elif answer in ["look at nuts"]:
      roll_text("After almost getting blown up, I don't know if the nuts are worth anymore, they're right next to a hole to, making it more difficult.")

    elif answer in ["look at squirrel"] and locked_doors["nut hole"]:
      roll_text("The squirrel casually sorts its nuts, although it throws you a menacing look occasionally.")

    elif answer in ["look at squirrel"]:
      roll_text("The squirrel literally stares at you as it sorts its nuts, and it isn't a friendly stare...")

    elif answer in ["look at hole", "look down hole"] and not locked_doors["nut hole"]:
      roll_text("The hole leads down into a small cave.")

    elif answer in ["look at tree", "look at towering tree", "look at tall tree"]:
      roll_text("Looks like there could be a nest up there...")

    # Squirrel/sinkhole actions
    elif answer in ["take nuts", "steal nuts", "get nuts", "take squirrel's nuts", "steal squirrel's nuts", "get squirrel's nuts", "take squirrels nuts", "steal squirrels nuts", "steal squirrels nuts"]:
      if not locked_doors["nut hole"]:
        roll_text("You go for the nuts, but you fall into the giant hole in the ground.")
        
      else:
        roll_text("You try to swipe the squirrel's nuts, but the squirrel yells at you, \"Swiper no swiping!\" then throws a small bomb at you. The bomb explodes, and you fall into a large sinkhole in the ground.")
      
      next_room = 8
      break
    
    elif answer in ["go in hole", "go into hole", "go down hole", "climb in hole", "climb into hole", "climb down hole", "slide down hole", "enter in hole", "enter into hole", "enter hole"]:
      # If hole has already been blasted by squirrel bomb
      if not locked_doors["nut hole"]:
        next_room = 8
        break
      
      else:
        roll_text("What hole? I don't see any human-sized holes here.")
    
    # Tree actions
    elif answer in ["climb tree", "climb up tree", "go up tree", "ascend tree"]:
      next_room = 7
      break
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(6)
      	
      else:
        roll_text("Me, help you? *laughs* Go get one of those self-help books, why don't ya.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# ------------------
# ----- Room 7 -----
# ------------------
def _07():
  if not items_taken["dozen eggs"]:
  	roll_text("You climbed the tree. Near you, you see a nest with twelve eggs. You don't see a mother bird protecting them.")
  else:
    roll_text("You climbed the tree. Nearby, you see an empty nest, where a sad mother bird sits quietly. There's nothing else up here.")

  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(7)
        
      else:
        roll_text("What map? You don't have a map, silly goose.")

    # Navigation
    elif answer in north:
      roll_text("The breeze is too strong that way, and you're afraid that it'll knock you off of the tree. Probably best not to go there.")
      
    elif answer in east:
      roll_text("The tree seems to have a shortage of branches on the east side. Better not climb down that way.")
      
    elif answer in south:
      roll_text("The branches are especially mossy to the south. You're probably going to slip and fall if you go that way.")
      
    elif answer in west:
      next_room = 6
      roll_text("You climbed down from the tree.")
      break
    
    elif answer in ["take eggs", "steal eggs", "get eggs", "grab eggs", "swipe eggs", "collect eggs", "pick up eggs"]:
      if items_taken["dozen eggs"]:
        roll_text("What eggs? All I see is a sad little bird.")
        
      else:
        inventory.append("dozen eggs")
        item_descriptions["grocery list"]["dozen eggs"] = True
        item_descriptions["dozen eggs"] = "You can make a killer omelet will these bad boys."
        roll_text("You took the eggs from the nest.")
        sleep(0.25)
        roll_text("Grocery list item complete: Dozen eggs!")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(7)
      	
      else:
        roll_text("You'd be hard-pressed to find a helpful book up here in a tree.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# ------------------
# ----- Room 8 -----
# ------------------
def _08():
  roll_text("You land in a small cave, high enough to kneel in. Along the wall are engraved the words, \"If thy wish to achieve, thou needs the tool which cleaves. Should thou win, thou must shave the chin.\" A ladder of roots leads back up to the surface.")
  
  while True:
    answer = input(">").lower()
    
    # Navigation
    if answer in north:
      roll_text("You begin to trip on stalagmites, they grow in abundance the further away they are until it becomes a wall.")
    
    elif answer in south:
      roll_text("You went south, but hit your body on a dirt wall, I don't think you're a gopher bud.")
    
    elif answer in west:
      roll_text("You look to the west and scrape your noze on a dirt wall, I don't think that way's an option.")
    
    elif answer in east:
      roll_text("You start walking east, although you suddenly realize you aren't moving, but pushing yourself into a wall.")

    elif answer in ["climb up roots", "climb out of cave", "climb roots", "climb ladder of roots", "leave cave"]:
      next_room = 6
      break
    
    # Map
    elif answer in _map and items_taken["koob"]:
      guide(8)
    elif answer in _map:
      roll_text("I'm sorry, but you have no map, you are lost, very lost, I mean that's what I assume because you asked for the map.")
    
    #  Help
    elif answer in _help and items_taken["koob"]:
      display_map(8)
    elif answer in _help:
      roll_text("I'm sorry, but the book you are trying to reach is unavailable.")
    
    # Looking at wall or message
    elif answer in ["look at wall", "look at words"]:
      roll_text("It looks like it was carved into the dirt with a book, you can even see small pieces of ripped paper.")
  	
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()
  
  return inventory, next_room, locked_doors, items_taken
      
      
# ------------------
# ----- Room 9 -----
# ------------------
def _09():
  roll_text("As you approach, one of the trees shuffles, it appears to have a pretty authentic face carved into it's trunk. The face seems quiver as the rest of the tree slightly trembles.")
  
  while True:
    answer = input(">").lower()
    
    # If player calls upon koobs knowledge
    if answer in _help and items_taken["koob"]:
      guide(9)
    
    elif answer in _help:
      roll_text("You don't have a book to get help from, I suggest taking a peek inside that chest after the stone arch.")
    
    # Map with Koob
    elif answer in _map and items_taken["koob"]:
      display_map(9)
    
    elif answer in _map:
      roll_text("How can you expect to look at a map if you don't have one? HUH?")
    
    # Navigation
    elif answer in south:
      next_room = 6
      
      break
    
    elif answer in west:
      roll_text("There're too many trees in the way to go there, but you do hear rushing water.")
    
    elif answer in east:
      roll_text("A huge white wall lumes over you, reaching beyond sight into the sky.")
    
    elif answer in north:
      roll_text("The trees are too thick, but you see a rainbow over them.")
    
    # ----- Ent Dialogue and Interaction Stuff -----
    
    # Look at Ent
    elif answer in ["look at ent", "look at tree"] and not items_taken["blank leaf"]:
      roll_text("You walk up to the tree to get a closer look, and get a closer look you do. The tree is actually and ent, with a face engraved in the bark, composed of eyebrows, eyes, a nose and mouth. It continues to stare at you with a sorrowfull look.")
      roll_text("The mouth begins to move... \"Did you need something stranger?\"")
    
    elif answer in ["look at ent", "look at tree"]:
      roll_text("You walk up to the tree to get a closer look, and get a closer look you do. The tree is actually and ent, with a face engraved in the bark, composed of eyebrows, eyes, a nose and mouth. It continues to stare at you with a joyful look.")
      roll_text("The mouth begins to move... \"Did you need something friend?\"")
    
    # Talk to Ent
    elif answer in ["talk to tree", "talk to ent"] and locked_doors["ent"] and items_taken["blank leaf"]:
      roll_text("Ent : Ahh, traveler, I've recently los- Wait, is that what I think it is? It Is! That leaf you have is my fathers which I lost some time ago. Perhaps you could give it to me? I would be very greatful.")
      locked_doors["ent"] = False
      
    elif answer in ["talk to tree", "talk to ent"] and locked_doors["ent"]:
      roll_text("Ent : Oh, are you here to help me? If so I'm deeply humbled by your act, if you could bring me my fathers first leaf I would be utterly thankful. It was lost to the wind one day when it slipped out of my branches. The face is blank, not even veins cling to it's surface. I wish you luck, if you actually intend to help me.")
      locked_doors["ent"] = False
    
    elif answer in ["talk to tree", "talk to ent"] and items_taken["blank leaf"]:
      roll_text("Ent : So, do you actually intend to give me my fathers leaf, or are you going to continue holding on to it? I'd hope you've chosen the former.")
    
    elif answer in ["talk to tree", "talk to ent"]:
      roll_text("Ent : You are here, but without my fathers leaf? I see no reason of speaking with me if you have not aquired what I've asked you for. ")
    
    # Give leaf to Ent
    elif answer in ["give tree leaf", "give ent leaf", "give tree blank leaf", "give ent blank leaf"] and "blank leaf" in inventory:
      roll_text("Ent : You have my gratitude, I don't have much in rewards though. Here, have one of my branches, it should come in handy.")
      acquire_cane("cane stick")
      inventory.remove("blank leaf")
      # Here is Place for Cane progression
    
    elif answer in ["give tree leaf", "give ent leaf", "give tree blank leaf", "give ent blank leaf"]:
      roll_text("*You don't have that to give*")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()
  
  return inventory, next_room, locked_doors, items_taken
      

# -------------------
# ----- Room 10 -----
# -------------------
def _10():
  roll_text("A rushing river lies ahead of you. You see a sun-bleached rope bridge that crosses to the other side. To the left of it, you see a man quietly fishing.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(10)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in ["cross river", "ford river", "cross bridge", "go over bridge", "go on bridge", "cross rope bridge", "go over rope bridge", "go on rope bridge"]:
      next_room = 11
      break
    
    elif answer in north:
      next_room = 11
      break
    
    elif answer in east:
      roll_text("There's a really thick forest that way, doesn't look like you can get in from here.")
    elif answer in south:
      next_room = 5
      break
    
    elif answer in west:
      roll_text("There's a giant abyss to the west, stretching over to a meadow. There's no way you can cross that.")

    # Talk to fisherman action
    elif answer in ["talk to man", "talk to fishing man", "talk to fisherman", "talk to fishermen", "talk to fisher man", "talk to angler"] and not items_taken["worm"]:
      roll_text("Fishing man: \"I been fishing all day long, don't got nothin' to show for it. S'pose I'd get somethin' with a little bait on the hook, a worm would work nicely\"")
      
    elif answer in ["talk to man", "talk to fishing man", "talk to fisherman", "talk to fishermen", "talk to fisher man", "talk to angler"]:
      roll_text("Fishing man: Did you need somthin lad? I don't have anythin more for ye otherwise.")
    
    # Give worm actions
    elif answer in ["give worm", "give man worm", "give fishing man worm", "give guy worm", "give fishing guy worm", "give fisher worm", "give fisherman worm", "give fisher man worm"]:
      if items_taken["worm"] and "worm" in inventory:
        inventory.remove("worm")
        roll_text("You give the man a worm.")
        roll_text("Fishing man: \"Whah thank you sir, I'll give this a try.\"")
        sleep(0.25)
        roll_text("The man puts the worm on his fishing hook, casts it into the water... and behold! He reels in a giant trout!")
        roll_text("Fishing man: \"Thank ya so much kind sir! I... don't know how to repay you. Don't got much but an extra fishin' pole. Here ya go!\"")
        
        sleep(0.25)
        roll_text("The man gives you a long wooden object. Wait, this isn't a fishing pole. This is part of a cane!")
        acquire_cane("fishing pole cane")
      
      # If not(items_taken["worm"] and "worm" in inventory)
      else:
        roll_text("What worm? Unless you want to give him yourself, you little worm.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(10)
      else:
        roll_text("It's not like that fishing man is going to help you, nor does he have a help book for you, either.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# -------------------
# ----- Room 11 -----
# -------------------
def _11():
  roll_text("You crossed the river. Over in the east, you see a rainbow. The end of it lands nearby. As you squint to the north, you see a rocky hill as the wind blows against you.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(11)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      next_room = 13
      break
    elif answer in east:
      next_room = 12
      break
    elif answer in south:
      next_room = 10
      break
    elif answer in west:
      roll_text("There's a giant abyss that way, reaching across to a meadow. Probably can't walk over there.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(11)
      else:
        roll_text("The sight of that beautiful rainbow is probably the only thing that can help you right now. A book would be nice, though...")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# -------------------
# Room 12   Date Worked On by Christian : November 15, 2017
# -------------------
def _12():
  if not items_taken["leprechaun"]:
  	roll_text("You reach the base of the rainbow. Behind a bush, you hear someone chuckling. Next to it, a pot of gold is tipped over, with gold coins spilling out.")
  
  elif not items_taken["points"]:
    roll_text("You reach the base of the rainbow. There's also a bush, and next to it, a pot of gold is tipped over, with gold coins spilling out.")
                
  else:
    roll_text("You reach the base of the rainbow. There's also a bush, and next to it, a pot is tipped over, completely empty.")
  
  while True:
    answer = input(">").lower()
    
    # If player calls upon koobs knowledge
    if answer in _help and items_taken["koob"]:
      guide(12)
    
    elif answer in _help:
      roll_text("You expect to have a guide help you along the way? Well you do, but for some reason you haven't found it yet!")
    
    # Map with Koob
    elif answer in _map and items_taken["koob"]:
      display_map(12)
    
    elif answer in _map:
      roll_text("You don't have a map! Maybe you can buy one with that gold over there... MAYBE, I didn't say you could.")
    
    # Navigation of the Game(for this room anyways)
    elif answer in north:
      roll_text("It get's too steep, and there are too many rocks to go that way. I mean, you could trip and die, who want's a story where the protagonist dies?")

    elif answer in east:
      roll_text("As you walk the ground suddenly disapeers from under you, but then a branch catches you and lowers you back to where you were. You look to see a huge cliff infront of you, and an ent next to it.")
    
    elif answer in south:
      roll_text("You begin walking, then you step on a root. About 20 trees quickly swerve to watch you standing there, you then slowly turn around and walk back.")
      
    elif answer in west:
      next_room = 11
      
      break

    # ----- Interaction Stuff -----
    
    # Bush Interactions
    elif answer in ["look at bush"] and not items_taken["blue berries"] and not items_taken["leprechaun"]:
      roll_text("You go up to the bush to find Blue Berries growing, but you also find a Leprechaun squatting next to it.")
      locked_doors["blue berries"] = False
      locked_doors["leprechaun"] = False
    
    elif answer in ["look at bush"] and not items_taken["blue berries"]:
      roll_text("You walk up to the bush to find Blue Berries growing out of the branches.")
    
    elif answer in ["look at bush"] and not items_taken["leprechaun"]:
      roll_text("You walk up to the bush, only to find a Leprechaun squatting next to it staring at the full pot of gold.")
    
    elif answer in ["look at bush"]:
      roll_text("You walk up to the bush to find nothing except the bush. That's all, you can go now...")
    
    elif answer in ["take blue berries", "pick up blue berries"] and not locked_doors["blue berries"] and not items_taken["blue berries"]:
      roll_text("You pick some blue berries and through them in your backpack, hope you can find them later...")
      items_taken["blue berries"] = True
      inventory.append("blue berries")
      roll_text("*You have acquired Blue Berries*")
      roll_text("You have checked off Banana from the grocery list.")
      
    # Leprechaun Interactions
    elif answer in ["look at leprechaun", "look at midget"] and not items_taken["leprechaun"]:
      roll_text("You begin to stare at the Leprechaun intently, it then turns to look at you with a disgusted look.")
      roll_text("Midget : Huh? Ya need somthin? Beat it! Im tryin to coun these coins! I think therez abou thousan of em.")
    
    elif answer in ["look at leprechaun", "look at midget"]:
      roll_text("What? A leprechaun? All I see are some pretty deep foot prints from when someone was squatting for a coupl of days...")
    
    elif answer in ["talk to leprechaun", "talk to midget"] and not items_taken["leprechaun"]:
      roll_text("Midget : OY! I don' need you! Beat it! These coin ar mine!")
    
    elif answer in ["talk to leprechaun", "talk to midget"]:
      roll_text("Uhh... Do you need some help? Because there isn't anyone here to talk to?")
    
    elif answer in ["give leprechaun pills", "give leprechaun sleeping pills", "give midget pills", "give midget sleeping pills"] and "pills" in inventory:
      roll_text("You hand the Leprechaun the pills, he begins to look at them intently...")
      roll_text("Midget : Drugs? Why not, I coul use som mor. *Takes Pills*")
      roll_text("The Leprechaun then falls onto the ground unconscious, you then pick up the Leprechaun. *Leprechaun Added to Inventory*")
      items_taken["leprechaun"] = True
      inventory.append("leprechaun")
      inventory.remove("pills")
    
    elif answer in ["give leprechaun pills", "give leprechaun sleeping pills", "give midget pills", "give midget sleeping pills"]:
      roll_text("You don't have pills to give...")
    
    # Pot of Gold Interactions
    #look at commands
    elif answer in ["look at pot", "look at pot of gold"] and not items_taken["points"]:
      roll_text("It's a rusted iron pot tipped over on to it's side with gold spilling out of it.")
    
    elif answer in ["look at pot", "look at pot of gold"]:
      roll_text("It's a rusted pot tipped over on it's side, although it's empty.")
    
    elif answer in ["look at gold"] and not items_taken["points"]:
      roll_text("Each individual coin reflects the sunlight as they sit in their large pile.")
    
    elif answer in ["look at gold"]:
      roll_text("What? Gold? I can sell it to feed my family and get a house! Wait... there's no gold... ;-;")
    
    #take/pick up commands
    elif answer in ["take pot of gold", "pick up pot of gold"] and items_taken["leprechaun"]:
      roll_text("You attempt to life the pot with all the gold in it, although, with your wimpy arms, it doesn't budge an inch.")
    
    elif answer in ["take pot of gold", "pick up pot of gold"]:
      roll_text("Midget : OY! Whatchya thin ya doin!? Get yer hands off me pot!")
    
    elif answer in ["take gold", "pick up gold"] and items_taken["leprechaun"] and not items_taken["points"]:
      roll_text("You reach out your hand to start grabbing the gold, but right as you touch it, the gold vaporizes. An etheral voice then echoes...")
      roll_text("*You have aquired 1000 Points*")
      items_taken["points"] = True
      inventory.append("1000 points")
    
    elif answer in ["take gold", "pick up gold"] and items_taken["leprechaun"]:
      roll_text("There isn't any gold to take...")
    
    elif answer in ["take gold", "pick up gold"]:
      roll_text("Midget : WOAH, get yer hands off me gold! I don' wan to see ya doin that again!")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

  return inventory, next_room, locked_doors, items_taken
    

# -------------------
# ----- Room 13 -----
# -------------------
# Started by Luke: 11-15-2017
# Completed by Luke: 11-24-2017
def _13():
  roll_text("Ahead you find the entrance to a cave with gusts of wind emitting from it. An eye is engraved in the stone above it. A mighty and constant roar is heard to the west, most likely a waterfall.")
  
  while True:
    answer = input(">").lower()
  	
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(13)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north or answer in ["enter cave", "go into cave", "walk into cave"]:
      roll_text("You try and go to the north but can't because of the mini mountain, you can only head more north by entering the cave.")

    elif answer in ["enter cave", "go into cave", "walk into cave"]:
      next_room = 14
      break
    
    elif answer in east:
      roll_text("The horizon stretches so far out there... meh, too far. Don't care.")
      
    elif answer in south:
      next_room = 11
      break
    
    elif answer in west:
      next_room = 16
    
    # Stone eye interactions
    elif answer in ["look at eye", "look at stone eye", "talk to eye", "talk to stone eye", "touch eye", "touch stone eye", "interact with eye", "interact with stone eye"]:
      roll_text("The eye whispers to you: \"Decayed bodies are great fertilizer, and bonemeal is pretty good for plants.\"")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(13)
      else:
        roll_text("The eye isn't going to give you a magic help book, but you could try talking to it.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# -------------------
# ----- Room 14   Date Worked On by Christian : November 22, 2017 -----
# -------------------
def _14():
  roll_text("As you enter the cavern you see glowing crystals covering the walls and ceiling, creating a path to what seems to be a golden throne. To the side is a crystal like table with a plate of pancakes on it.")
  
  while True:
    answer = input(">").lower()
    
     # If player needs help
    if answer in _help and items_taken["koob"]:
      guide(14)
    
    elif answer in _help:
      roll_text("There's no words for you in this spooky cave... Well I guess it isn't that spooky and more majestic but whatever!")
    
    # The Map of Koob
    elif answer in _map and items_taken["koob"]:
      display_map(14)
    
    elif answer in _map:
      roll_text("Would a map help you when you're in a cave? Yes, if you had a magical one anyways.")
    
    # Thow Worlds Navigational System
    elif answer in ["enter back room", "enter room", "go into room", "go to room", "walk into room"] and not locked_doors["throne"]:
      next_room = 15
      break

    elif answer in ["walk out of cave", "exit cave", "leave cave", "go out of cave", "leave", "exit"]:
      next_room = 13
      break
    
    elif answer in north:
      roll_text("You can't tell which direction is North.")

    elif answer in east:
      roll_text("You can't tell which direction is East.")
    
    elif answer in south:
      roll_text("You can't tell which direction is South")
      
    elif answer in west:
      roll_text("You can't tell which direction is West.")
    
    # - Interaction and Things -
    #look at interactions
    elif answer in ["look at golden throne", "look at throne"] and locked_doors["throne"]:
      roll_text("The throne looks to be completely made of gold, except there seems to be a pressure plate on the seat. There are also words engraved in the throne, \"Only the most Greedy of them may sit in this seat\". I wonder what it means?")
      
    elif answer in ["look at golden throne", "look at throne"]:
      roll_text("The unconscious Leprechaun lies on on the throne, in a spread out position. The pressure plate now seems to have been activated.")
    
    elif answer in ["look at plate of pancakes", "look at pancakes"] and not items_taken["pancakes"]:
      roll_text("The pancakes are stacked with precision, each directly over the other. Syrup is lathered over the surface with a lob of butter on top. Look delicious...")
    
    elif answer in ["look at plate of pancakes", "look at pancakes"]:
      roll_text("I'm sorry to say... but there are no longer pancakes on that table... It's sad, I know...")
    
    #take/pick up interactions
    elif answer in ["take pancakes", "pick up pancakes", "take plate of pancakes", "pick up plate of pancakes"] and not items_taken["pancakes"]:
      roll_text("As you tread caution as to not get sticky, you pick up the plate.")
      roll_text("*Pancakes Aquired*")
      items_taken["pancakes"] = True
      inventory.append("pancakes")
    
    elif answer in ["take pancakes", "pick up pancakes", "take plate of pancakes", "pick up plate of pancakes"]:
      roll_text("Pa-pancakes? Wh-where? I'm so h-hungry... ~~GRUMBLE~~")
    
    #put item on interactions
    elif answer in ["put leprechaun on golden throne", "put leprechaun on throne", "put midget on golden throne", "put midget on throne", "use leprechaun on throne", "use leprechaun on golden throne"] and "leprechaun" in inventory:
      roll_text("You get out the leprechaun and place him on the Golden Throne, you here stone grinding, and see the wall behind the throne open up into another room.")
      inventory.remove("leprechaun")
      locked_doors["throne"] = False
    
    elif answer in ["put leprechaun on golden throne", "put leprechaun on throne", "put midget on golden throne", "put midget on throne"]:
      roll_text("You don't have the leprechaun to put down...")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()
  
  return inventory, next_room, locked_doors, items_taken
    
  
# -------------------
# ----- Room 15   Date Worked On by Christian : November 22, 2017 -----
# -------------------
def _15():
  if not items_taken["banana"]:
  	roll_text("An old goblin is lying on the floor hugging a banana, he notices your footsteps and gets up to greet you.")
  else:
    roll_text("An old goblin is sitting, legs folded, he sees you and gives a smile. He then stands up.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(15)
      else:
        roll_text("Map? You don't have one, but you are in one of the highest points on the map.")
    
    # Navigation
    elif answer in north:
      roll_text("Another wall lies ahead, I don't think we're a high enough level to get past it yet!(You'll never reach the level to get past it...)")
      
    elif answer in east:
      roll_text("There's just a wall that way, although it's pretty far considering this is a cave.")
      
    elif answer in south:
      next_room = 14
      break
      
    elif answer in west:
      roll_text("There's just another wall... That's it.")
      
    
    # Actions
    #looking at things
    elif answer in ["look at old goblin", "look at goblin"]:
      roll_text("The Old Goblin is standing in the center of the room, cradling a banana in one of his arms.")
    
    elif answer in ["look at banana"]:
      roll_text("The banana is resting snug in the Old Goblins arm.")
    
    #talking to goblin 
    elif answer in ["talk to goblin", "talk to old goblin", "talk to goblin hugging a banana", "talk to old goblin hugging a banana"] and not items_taken["banana"]:
      roll_text("Old Goblin : Ahhhhhh, traveler... Thank you for returning the greedy king to his rightful throne. If you need, I can offer you an award, but all I have is this banana.")
      locked_doors["banana"] = False
      
    elif answer in ["talk to goblin", "talk to old goblin", "talk to goblin hugging a banana", "talk to old goblin hugging a banana"]:
      roll_text("Old Goblin : Ahhhhhh, good to see you young traveler! I hope your journey is faring you well.")
    
    #taking banana
    elif answer in ["take banana", "pick up banana"] and not locked_doors["banana"]:
      roll_text("Old Goblin : Alright, this fruit is yours.")
      sleep(.5)
      roll_text("*You have aquired the Banana!*")
      roll_text("Banana has been checked off the grocery list.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(15)
      else:
        roll_text("You need help getting a banana? I don't think so...")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken
  

# -------------------
# ----- Room 16 -----
# -------------------
# Started by Luke: 11-24-2017
# Completed by Luke: 11-24-2017
def _16():
  roll_text("The roar of the waterfall is deafening as it feeds a ravine with massive streams of water. You see a small stone path leading behind the fall.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(16)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in ["walk down small stone path", "walk down small path", "walk down path", "follow path", "follow path behind waterfall", "follow path behind fall", "follow stone path", "follow stone path behind waterfall", "follow stone path behind waterfall", "follow small stone path", "follow small stone path behind fall", "follow small stone path behind waterfall", "go down path", "go down stone path", "go down small stone path", "go behind waterfall", "go behind fall"]:
      next_room = 17
      break
    
    elif answer in north:
      roll_text("That's the way the path leads. You should follow it.")
      
    elif answer in east:
      next_room = 13
      break
    
    elif answer in south:
      roll_text("Careful, there. If you go that way, you'll fall into the streams and drown.")
      
    elif answer in west:
      roll_text("The spray from the fall is powerful, and you get really wet going that way. You decide not to be all soaked and miserable.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(16)
      	
      else:
        roll_text("Well, if you pulled out a help book here, the pages would get super soaked. That would be useless.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 17 -----
# -------------------
# Started by Luke: 11-24-2017
# Completed by Luke: 11-24-2017
def _17():
  # Neither door unlocked
  if locked_doors["dead bodies"] and locked_doors["giant stone scissors"]:
  	roll_text("You enter the small cavern with the waterfall behind you, and giant stone scissors ahead. Two lumps with spears resting on them lie on either side of the scissors.")
  # Dead bodies unlocked, not scissors
  elif not locked_doors["dead bodies"]:
    roll_text("You enter the small cavern with the waterfall behind you, and giant stone scissors ahead. Two dead corpses with spears resting on them lie on either side of the scissors.")
  # Scissors unlocked, not dead bodies
  elif not locked_doors["giant stone scissors"]:
    roll_text("You enter the small cavern with the waterfall behind you. Ahead lies a cave with large, crumbled rocks at the entry. On either side of it, you see two lumps with spears resting on them.")
  # Both doors unlocked
  elif not locked_doors["dead bodies"] and not locked_doors["giant stone scissors"]:
    roll_text("You enter the small cavern with the waterfall behind you. Ahead lies a cave with large, crumbled rocks at the entry. On either side of it, you see two dead corpses with spears resting on them.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(17)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    if answer in north:
      if not locked_doors["giant stone scissors"]:
        next_room = 18
        break
      else:
        roll_text("The giant stone scissors block your path that way.")
    elif answer in east:
      roll_text("You hit your face on the rock wall. Try another direction.")
    elif answer in south:
      next_room = 16
      break
    elif answer in west:
      roll_text("Your teeth hurt because you just hit your face on rocks. Try another way.")
      
    # Lump actions (Oh my gosh I used so many responses)
    elif answer in ["look at lumps", "look at lumps with spears", "look at corpses", "look at left lump", "look at left lump with spear", "look at right lump", "look at right lump with spear",
                  "look at left corpse", "look at left corpse with spear", "look at right corpse", "look at right corpse with spear",
                  "inspect lumps", "inspect lumps with spears", "inspect corpses", "inspect left lump", "inspect left lump with spear", "inspect right lump", "inspect right lump with spear",
                  "inspect left corpse", "inspect left corpse with spear", "inspect right corpse", "inspect right corpse with spear",
                  "search lumps", "search lumps with spears", "search corpses", "search left lump", "search left lump with spear", "search right lump", "search right lump with spear",
                  "search left corpse", "search left corpse with spear", "search right corpse", "search right corpse with spear"]:
      if locked_doors["dead bodies"]:
        if items_taken["bonemeal"]:
          roll_text("Poor guys. Must not have been pretty. Sure ain't pretty now.")
        else:
          roll_text("These lumps are decaying corpses. Ewww... but wait, they're full of bonemeal. You can really grow some plants with that.")
          locked_doors["dead bodies"] = False
    
    # Boneameal actions
    elif answer in ["take bonemeal", "get bonemeal", "collect bonemeal", "harvest bonemeal", "pick up bonemeal"]:
      if items_taken["bonemeal"]:
        roll_text("Doesn't look like there's any bonemeal left in these corpses. You got the last of it!")
      else:
        inventory.append("bonemeal")
        item_descriptions["bonemeal"] = "This stuff grows plants really quickly."
        roll_text("You harvested the bonemeal from the corpses.")
    
    # Giant stone scissors actions
    elif answer in ["look at scissors", "search scissors", "look at stone scissors", "search stone scissors", "look at giant stone scissors", "search giant stone scissors"]:
      if items_taken["magic rock"] and "magic rock" in inventory:
        roll_text("These are big scissors. But you have a magic rock. Rock beats scissors!")
      else:
        roll_text("You gaze upon the majestic stone scissors. Maybe one day, you'll find a rock powerful enough to smash them.")
    
    elif answer in ["use rock on scissors", "use rock on stone scissors", "use rock on giant stone scissors", "use magic rock on scissors", "use magic rock on stone scissors", "use magic rock on giant stone scissors",
                    "throw rock at scissors", "throw rock at stone scissors", "throw rock at giant stone scissors", "throw magic rock at scissors", "throw magic rock at stone scissors", "throw magic rock at giant stone scissors"]:
      if items_taken["magic rock"] and "magic rock" in inventory:
        roll_text("You threw the magic rock at the giant scissors.")
        sleep(0.25)
        roll_text("*crack*...")
        sleep(0.25)
        roll_text("*crack crack*...")
        sleep(0.25)
        roll_text("*CRRRAAACCCKKKK*")
        roll_text("The scissors crumble into a giant heap of rocks. Behold, where they stood now lies an opening to a cave! You should totally check that out.")
        locked_doors["giant stone scissors"] = False
      else:
        roll_text("You don't appear to have any kind of rock that'll put a dent in those scissors. You should go get one.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(17)
      else:
        roll_text("Rock beat scissors. What else do you need, a book?")
        
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# -------------------
# ----- Room 18 -----
# -------------------
# Started by Luke: 11-24-2017
# Completed by Luke: 11-24-2017
# @Christian: Read comment on Book section below
def _18():
  # This sequence accounts for everyting, I promise c:
  intro = "You enter a large stone room."
  
  # Book is still there
  if not items_taken["nireal book"]:
    intro += " In it, you find a book titled Nireal"
    # Key is on top of book
    if not items_taken["golden key"]:
      intro += "; a golden key lies on top of it."
    # Key is not there, end the sentence.
    else:
      intro += "."
      # Lock is still locked
      if locked_doors["silver lock"]:
        intro += " The book is locked shut by a silver lock."
      # Lock has been unlocked
      else:
        intro += " An unlocked silver lock sits on the ground next to it."

  # Book is not there, but golden key is there.
  elif not items_taken["golden key"]:
    intro += " A golden key lies on the ground."
    # Lock is unlocked. Lock cannot be locked without the book, because it would not have a book to be locking, now would it?
    if locked_doors["silver lock"]:
      intro += " Next to it sits an unlocked silver lock."

  # Book and golden key have both been taken, only the lock remains.
  else:
    intro += " On the ground sits an unlocked silver lock. So, so lonely..."
  
  # FINALLY, roll the text.
  roll_text(intro)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(18)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("You run into the north wall of the cave. Try going somewhere else.")
    elif answer in east:
      roll_text("You hit the east wall of the cave. You shouldn't do that, it's bad for your health.")
    elif answer in south:
      next_room = 16
    elif answer in west:
      roll_text("Why do you have a broken nose all of a--ohh, you've been smashing your face on stone walls, haven't you? That's not okay.")
      
    # Golden key actions
    elif answer in ["get key", "get gold key", "get golden key", "take key", "take gold key", "take golden key", "pick up key", "pick up gold key", "pick up golden key"]:
      if not items_taken["golden key"]:
        inventory.append("golden key")
        item_descriptions["golden key"] = "Must unlock a golden lock."
        items_taken["golden key"] = True
        roll_text("You picked up the golden key.")
      else:
        roll_text("What key? I know what is key: observation. There is no key in here, so you are not observant.")
    
    # Silver lock actions
    elif answer in ["unlock lock", "unlock silver lock", "unlock book"]:
      if items_taken["silver key"] and "silver key" in inventory:
        locked_doors["silver lock"] = False
        inventory.remove("silver key")
        roll_text("*clink*")
        roll_text("The silver lock opened and hit the stone floor. You unlocked the book.")
      else:
        roll_text("You're going to need a silver key for that silver lock there, partner.")
    
    # Book actions
    elif answer in ["get book", "pick up book", "take book"]:
      if locked_doors["silver lock"]:
        roll_text("There's still a silver lock on that book. It'd be hard to read a book if it's locked shut, now wouldn't it?")
      else:
        inventory.append("nireal book")
        item_descriptions["nireal book"] = "The Book of Nireal." # @Christian I'm not sure what you wanted in the book so I'll leave that to you c:
        items_taken["nireal book"] = True
        roll_text("You picked up the book, and now it's yours. Happy reading!")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(18)
      else:
        roll_text("You're in a room with plain stone walls. Even a help book wouldn't tell you any differently.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

              
# -------------------
# ----- Room 19 -----
# -------------------
# Started by Christian: 11-24-2017
# Completed by Christian: 11-24-2017
def _19():
  if not items_taken["worm"]:
  	roll_text("You see a dirt path start to form to the west, and a clearing to the north. In the grass around you, you see a dirt patch standing out.")
  else:
    roll_text("You see a dirt path start to form to the west, and a clearing to the north. In the grass around you, you see a hole, kinda slimy.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(19)
      else:
        roll_text("No. No map for you.")
    
    # Navigation
    elif answer in north:
      next_room = 24
      break
      
    elif answer in east:
      next_room = 4
      break
      
    elif answer in south:
      roll_text("You hit your face on a brick wall. Try another direction.")
      
    elif answer in west:
      next_room = 20
      break
      
      
    # Actions
    #look at the dirt patch
    elif answer in ["look at dirt patch", "look at patch"] and not items_taken["worm"]:
      roll_text("It seems to be more loose than everything else, easy to dig up.")
    
    elif answer in ["look at dirt patch", "look at patch"]:
      roll_text("It's just a hole, with some beetles and worms. (Can't interact with them.)")
    
    #use shovel on patch
    elif answer in ["use shovel on patch", "use shovel on dirt patch"] and not items_taken:
      roll_text("You dig up the patch to find a some worms! They must be great for bait.")
      roll_text("*You have acquired a Worm*")
      items_taken["worm"] = True
      inventory.append("worm")
    elif answer in ["use shovel on patch", "use shovel on dirt patch"]:
      roll_text("There is no patch to dig up...")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(19)
      else:
        roll_text("The kid who asked for help, except, no one came.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken
              

# -------------------
# ----- Room 20 -----
# -------------------
# Started by Christian: 11-24-2017
# Finished by CHristian: 11-28-2017
def _20():
  global end
  if not items_taken["watermelon"]:
  	roll_text("You see an old man sitting on a rock next to the path which continues to the west. It also splits off to the south.")
  else:
    roll_text("You see a rock next to the path which continues to the west. It also splits off to the south. There's also a spot where the grass was blown around a lot.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(20)
      else:
        roll_text("You don't have a map to use... I mean, doodling is what maps are for right?")
    
    # Navigation
    elif answer in north:
      roll_text("There are too many trees, but you see a figure with plad through them.")
      # North
    elif answer in east:
      next_room = 19
      break
      # East
    elif answer in south:
      next_room = 22
      break
      # South
    elif answer in west:
      next_room = 21
      break
      # West
      
    # Actions
    #look at things actions
    elif answer in ["look at old man", "look at man", "look at old", "look at old guy", "look at watermelon"] and not items_taken["watermelon"]:
      roll_text("He seems to be new, despite his appearance, his eyes are full of life and curiosity. His eyes land on you and light up, maybe you should go talk to him?")
    
    elif answer in ["look at old man", "look at man", "look at old", "look at old guy", "look at watermelon"]:
      roll_text("There is no magical being in the immediate vicinity, well, except Koob.")
    
    #when you talk to the old man
    elif answer in ["talk to old man", "talk to man", "talk to old", "talk to old guy"] and not items_taken["watermelon"] and locked_doors["old man dialogue"] and "cane" in inventory:
      roll_text("Old Man : Boy! You seem to have a cane! Would you do me a favor and let me have it? I'm willing to pay you a fantastic reward! Just go ahead and give it to me.")
      locked_doors["old man dialogue"] = False
      
    elif answer in ["talk to old man", "talk to man", "talk to old", "talk to old guy"] and not items_taken["watermelon"] and locked_doors["old man dialogue"]:
      roll_text("Old Man : Ah, boy, would you perhaps know where a cane is? I lost mine, you can even construct one? Well, I'll leave it to you to decide, I'll just wait here on this rock.")
      sleep(.5)
      roll_text("Oh wait, I forgot to mention, I'll reward you handsomely for getting me a new cane!")
      locked_doors["old man dialogue"] = False
    
    elif answer in ["talk to old man", "talk to man", "talk to old", "talk to old guy"] and not items_taken["watermelon"]:
      roll_text("Old Man : You are back without a cane? Well you aren't getting that glorious reward with nothing! Better keep on looking for parts for a new cane!")
    
    elif answer in ["talk to old man", "talk to man", "talk to old", "talk to old guy"]:
      roll_text("There isn't anyone here to talk to...")
    
    #when you give him the cane / very major event right here
    elif answer in ["give old man cane", "give old guy cane", "give man cane", "give old cane", "give old man the cane", "give old guy the cane", "give man the cane", "give old the cane"] and "cane" in inventory:
      roll_text("Old Man : Woah! Thanks a ton boy! I'd never of thought I'd get a cane ever again! Well, you better get ready for your reward then! >:D")
      sleep(.5)
      roll_text("The ground begins to rumble, the wind starts to roar, everything around you seems to shake. You look back at the Old Man to find him slowly lifting off of the ground and his beard growing longer.")
      roll_text("He rises and rises, his beard grows and grows, stopping a couple of feet off the ground, the wind and rumbling growing stronger still.")
      roll_text("*He has to yell over the wind* Old Man : HA HA! THIS IS WHAT I'VE BEEN WAITING FOR! THIS WORLD SHALL BECOME MINE AFTER ALL THESE YEARS!")
      sleep(1)
      roll_text("*THANK YOU BOY*")
      sleep(1)
      
      if items_taken["koob"]:
        roll_text("Koob : WE HAVE TO STOP HIM SOMEHOW!")
        sleep(1)
        roll_text("Koob : PERHAPS WE CAN DO SOMETHING TO HIS BEARD!")
        
        # Hint at you needing the scissors to defeat him if you have koob but not the scissors
        if items_taken["scissors"]:
          roll_text("You : *But we don't have any scissors...*")
      
      else:
        roll_text("You : *What should I do? Is this good or bad?*")
        sleep(.5)
        roll_text("You : *Should I join him or stop him?*")
      
      # The loop for making the (probably) final decision
      while True:
        answer = input(">").lower()
        
        if answer in ["join him", "join", "join old man"]:
          roll_text("Old Man : GREAT CHOICE! THEN COME ON, ONLY THE WORLD WAITS!")
          sleep(1)
          roll_text("*Everything begins to shine brighter, everything turning white, a loud buzz begins to over power the howling of the wind.*")
          roll_text("*Everything keeps on getting brighter and brighter, until it's all white,*")
          sleep(.5)
          roll_text("*completely still,*")
          sleep(.75)
          roll_text("*silent,*")
          sleep(1.5)
          roll_text("*Dead*")
          
          end = 1
          break
        
        elif answer in ["stop him", "stop"]:
          roll_text("You : *But how? How will I stop him?*")
          sleep(1)
          roll_text("????? : Maybe you can end his life with a pistol?")
          roll_text("????? : Or maybe you can weaken him with water?")
        
        elif answer in ["cut off beard", "use scissors", "use scissors on beard", "cut off his beard"] and "scissors" in inventory:
          roll_text("You pull out the scissors and look up at the Old Man.")
          roll_text("He looks back with a shocked expression.")
          sleep(.5)
          roll_text("Old Man : WAIT! WHAT ARE YOU DOING? THOSE SCISSORS ARE DANGE-")
          sleep(.3)
          roll_text("You jump up and to snip at his beard but miss. He tries to move but realizes he's still transforming. You jump again and cut the beard completely off.")
          sleep(.2)
          roll_text("*You have acquired Magical Scissors*")
          roll_text("The scissors suddenly begin to glow brightly, giving off a magical aura. As for the Old Man...")
          inventory.append("magic scissors")
          items_taken["magic scissors"] = True
          sleep(1)
          roll_text("He immediently falls to the ground. All of the rumbling stops, the wind dies down, everything becomes peaceful again.")
          sleep(.5)
          roll_text("You look at the Old Man to see a... Kangaroo??? It begins to shrink, morphing into a cat, a fat one too. It continues to shrink and morph into a striped green sphere.")
          roll_text("It actually looks like a watermelon... Huh, another item on the list!")
          sleep(.5)
          roll_text("Watermelon : Hey! Can you even hear me? You can't do this! I worked so hard to get that far! Then you just ruined it, I'm back at the begining now!")
          roll_text("You ignore the watermelon and pick it up.")
          roll_text("*You have acquired Watermelon!*")
          inventory.append("watermelon")
          items_taken["watermelon"] = True
          
          break
        
        elif answer in ["use pistol on old man", "shoot old man", "use b23r pistol on old man", "use b23r on old man"] and items_taken["pistol"]:
          roll_text("You slowly pull out the pistol, bringing it up to the old man.")
          sleep(.5)
          roll_text("The Old Man looks horrified by the object.")
          roll_text("Old Man : WHAT ARE YOU DOING? THAT ISN'T SOMETHING TO BE PLAYING WI-")
          roll_text("3 shots fire off rapidly, one after another from one pull of the trigger.")
          roll_text("The Old Mans face is frozen, expressionless. He hangs in the air as the wind and rumbling fade away. He then falls to the ground, a puddle of blood beginning to form under the body.")
          sleep(1)
          roll_text("You look down at the pistol.")
          roll_text("You : *Was this the right decision?*")
          items_taken["watermelon"] = True # You don't actually get the watermelon, but his life is "taken", idk, I just means that you've had this encounter
          
          break
        
        elif answer in ["use cup of water on old man", "pour water on old man", "pour cup of water on old man"] and "cup of water" in inventory:
          roll_text("You carefully bring out the cup of water. Then, suddenly, you chuck the cup at the Old Man.")
          inventory.remove("cup of water")
          sleep(.5)
          roll_text("Old Man : WHAT THE? WHAT DO YOU THINK YOU'RE DOING, NOW I'M ALL WET! YOU BETT-")
          roll_text("The Old Man begins to distort and shrink, you see him slowly morph into a Kangaroo, still shrinking he morphs into a really fat cat.")
          roll_text("As the wind and rumbling die down completely, he shrinks into a watermelon. It then falls to the ground, a small crack is visible, and it begins to move.")
          sleep(.5)
          roll_text("Watermelon : AWW MAN! I worked so hard to get to that point in transformation! Then you came a long and ruined it! All I wanted was to be a dinosaur...")
          roll_text("You kinda feel bad for the fruit, or, maybe you don't...")
          roll_text("Anyways, you pick up the watermelon, checking it off your grocery list.")
          roll_text("*You have acquired Watermelon*")
          items_taken["watermelon"] = True
          inventory.append("watermelon")
          
          break
        
        else:
          roll_text("You can't do that, or maybe you typed it in wrong.")
      
    elif answer in ["give old man cane", "give old guy cane", "give man cane", "give old cane", "give old man the cane", "give old guy the cane", "give man the cane", "give old the cane"]:
      roll_text("Old Man : Boy, you think this is funny!? If you have nothing to bring me, then don't say you have something to bring me! Just, go and make that cane... Please?")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(20)
      else:
        roll_text("That old man looks suspicious, I don't think he can help you, I mean, I can't either. XD")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))
    
    if end == 1:
      break

  return inventory, next_room, locked_doors, items_taken


# -------------------
# ----- Room 21 -----
# -------------------
# I'm really salty about the coffee, lol.
# Started by Luke: 11-27-2017
# Completed by Luke: 11-27-2017
def _21():
  intro = "There's an empty, charred fire pit with two mossy rocks next to it. One of the rocks looks good for sitting"
  if locked_doors["coffee cup"]:
    intro += "; a cup of coffee rests near the edge of it."
  elif not items_taken["cup"]:
    intro += ". A cup sits on the ground, spilled coffee staining the dirt."
  else:
    intro += ". The dirt below is stained with coffee."
  
  if not items_taken["square"]:
    intro += " You even see a Square sitting on the other rock, excited about your arrival."
  
  roll_text(intro)
  
  sitting_down = False
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(21)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("The mountains in the distance... they... they look way too daunting. Let's not go there.")
    elif answer in east:
      next_room = 20
      break
    elif answer in south:
      roll_text("*FZZ-FZZZ* There's a glitch--*FZZ*--in the matrix--*FZZ FZZ*--can't go--*ffzzzzzzzzz*...")
    elif answer in west:
      roll_text("The path ends that way. Better not stray off the path, lest you get caught after dark.")
    
    # Sitting down actions
    elif answer in ["sit on rock", "sit on the rock", "sit down on rock", "sit down on the rock", "sit down", "sit"]:
      if sitting_down:
        roll_text("You're already sitting down, silly.")
      else:
        sitting_down = True
        if locked_doors["coffee cup"]:
          locked_doors["coffee cup"] = False
          roll_text("As you sit down, you accidentally knock a cup of coffee off of the rock. Brown java goodness spills all over the ground. The cup lies there, now empty and sad.")
        elif items_taken["cup"]:
          roll_text("You sat down on the rock. Your feet sit on the remains of once-beautiful coffee goodness.")
        else:
          roll_text("You sat down on the rock. At your feet, the coffee cup lies next to a bunch of spilled, wasted coffee.")
        
        if not items_taken["square"]:
          roll_text("Suddenly, the square begins to talk to you.")
          roll_text("Square: \"HI! I AM THE FRIENDLIEST SQUARE YOU'LL EVER MEET! PLEASE LET ME HOP INTO YOUR INVENTORY, PLEASEPLEASEPLEASEPLEASEPLEASE!!!\"")
          sleep(0.25)
          roll_text("You: \"What? No, I don't--Wait, what are you doing? No! Don't! Aaahhh--!\"")
          roll_text("Square: *hops into your inventory*")
          items_taken["square"] = True
          item_descriptions["square"] = "It looks a lot like the square on a PlayStation controller."
          inventory.append("square")
    
    # Coffee cup actions
    elif answer in ["get cup", "get coffee cup", "get cup of coffee", "pick up cup", "pick up coffee cup", "pick up cup of coffee", "take cup", "take coffee cup", "take cup of coffee"]:
      if locked_doors["coffee cup"]:
        roll_text("The cup is below your reach and you don't feel like bending down to get it. You'll have to sit on the rock first.")
      elif not items_taken["cup"]:
        items_taken["cup"] = True
        inventory.append("cup")
        item_descriptions["cup"] = "This cup holds coffee. And water."
        roll_text("You picked up the cup.")
      else:
        roll_text("There's no cup here. Just a bunch of wasted coffee.")
    
    # Getting up actions
    elif answer in ["get up", "stand up", "stand", "rise up", "rise"]:
      if sitting_down:
        sitting_down = False
        # Hehe, easter egg. Random 10% chance.
        if random.random() < 0.10:
        	roll_text("You stood up. Good job, way to take a stand for yourself!")
        else:
          roll_text("You stood up.")
      # If standing up
      else:
      	roll_text("You're not sitting down, though.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(21)
      else:
        roll_text("Is that cup of coffee going to help you? No, I don't think so. It'd be better to sip on that coffee while reading a good book.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 22 -----
# -------------------
# Started by Luke: 11-27-2017
# Completed by Luke: 11-27-2017
def _22():
  intro = "The path abruptly ends at the wheels of a broken down bus covered in vines. You look up and see \"BOii Tranzit\" above the windows, which all appear to be shut"
  if locked_doors["bus"]:
    intro += ", including the bus door."
  else:
    intro += ". The door is open, though."
  
  roll_text(intro)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(22)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      next_room = 20
      break
    
    elif answer in east:
      roll_text("There's no path that way. The path ends here, remember?")
      
    elif answer in south:
      roll_text("There's a bus in your way. Maybe you should try going into it, eh?")
      
    elif answer in west:
      roll_text("A spooky zombie waits over there. Unless you wish to support the apocalypse, don't go there.")
    
    # Outside-of-bus interactions
    elif answer in ["look at bus", "go to bus", "approach bus", "search bus", "inspect bus", "talk to bus"]:
      if locked_doors["bus"]:
        roll_text("There is only the sign, windows and door. But as you look at the door, you here a faint whisper. \"Hold square to open the door...\"")
      else:
        roll_text("The bus doors appear to be open...")
    
    # Enter bus actions
    elif answer in ["go in bus", "go on bus", "go into bus", "go onto bus", "enter bus", "enter into bus", "walk in bus", "walk into bus", "step in bus", "step into bus", "step onto bus", "hop in bus", "hop on bus", "hop into bus", "hop onto bus"]:
      if locked_doors["bus"]:
        roll_text("What are you doing? The doors are obviously closed.")
        
      else:
        next_room = 23
        break
    
    # Unlocking bus actions
    elif answer in ["hold square", "hold square to open door", "hold square to unlock door", "use square on bus,", "use square on door", "use square on bus door"]:
      if locked_doors["bus"]:
        if "square" in inventory:
          locked_doors["bus"] = False
          roll_text("*WOOSH*")
          roll_text("The door opens and debris from behind it is whisked outward by a great gust of wind.")
          roll_text("The bus is open for you to hop right on into it.")

        else:
          roll_text("You don't have a Square to hold...")

      else:
        roll_text("The bus is already open... You don't have to hold the square again.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(22)
      else:
        roll_text("Maybe that bus has a helpful book on it. Or something.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# -------------------
# ----- Room 23 -----
# -------------------
# Started by Luke: 11-27-2017
# Completed by Luke: 11-27-2017
def _23():
  intro = "You find a mechanical driver at the wheel after you pass through the rusted door frame. In the middle of the ceiling you see"
  if not items_taken["pistol"]:
    intro += " an outline of a pistol"
  else:
    intro += " a pistol with an outline around it"
  
  if not items_taken["oranges"]:
    intro += ", and a basket of oranges at the back of the bus."
  else:
    intro += "."
  
  roll_text(intro)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(23)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("You'll have to leave through the bus door to go that way.")
    elif answer in east:
      roll_text("You take off sprinting and--oh no, you tripped on a bus seat. Too bad.")
    elif answer in south:
      roll_text("The bus driver doesn't appreciate you rubbing your face against the windows like that.")
    elif answer in west:
      roll_text("You try to break a window to get out through a window, but you hurt your hand and give up.")

    # Look at driver action
    elif answer in ["look at driver", "look at mechanical driver", "look at bus driver", "look at mechanical bus driver"]:
      roll_text("The robot has glowing blue eyes and a bus driver uniform which has decayed. It looks around every once in a while, then honks the horn but nothing happens...")
      
    # Gun actions
    elif answer in ["look at pistol", "look at gun", "look at pistol outline", "look at gun outline", "look at pistol with outline", "look at gun with outline",
                    "inspect pistol", "inspect gun", "inspect pistol outline", "inspect gun outline", "inspect pistol with outline", "inspect gun with outline",
                    "search pistol", "search gun", "search pistol outline", "search gun outline", "search pistol with outline", "search gun with outline"]:
      if not items_taken["pistol"]:
      	roll_text("Pistol: *whispers* \"Hold square for B23R [Cost: 1000]\"")
      elif "B23R pistol" in inventory:
        roll_text("This is one of the rare guns where you can't buy more ammo! Good luck with that!")
      else:
        roll_text("Pistol: *whispers* \"Hold square for B23R [Cost: 1000]\"")
    
    elif answer in ["hold square", "hold square to buy gun", "hold square to purchase gun", "use square on outline", "use square on pistol outline", "use square on pistol"]:
      if "1000 points" in inventory:
        inventory.remove("1000 points")
        items_taken["pistol"] = True
        inventory.append("B23R pistol")
        item_descriptions["B23R pistol"] = "Man, this thing could shoot something important!"
        roll_text("You bought the B23R Pistol.")
      else:
      	roll_text("You don't have 1,000 points to buy this pistol!")
    
    # Orange actions
    elif answer in ["look at oranges", "look at basket of oranges", "look at basket", "inspect oranges", "inspect basket of oranges", "inspect basket",
                    "search oranges", "search basket of oranges", "search basket"]:
      if items_taken["oranges"]:
        roll_text("What oranges? There are no oranges here.")
      else:
        roll_text("Mmmm, juicy oranges. You could make some killer orange juice with those.")
    
    elif answer in ["get oranges", "get basket of oranges", "get basket", "pick up oranges", "pick up basket of oranges", "pick up basket",
                    "take oranges", "take basket of oranges", "take basket"]:
      items_taken["oranges"] = True
      item_descriptions["oranges"] = "You could make some killer orange juice with these."
      item_descriptions["grocery list"]["oranges"] = True
      inventory.append("oranges")
      roll_text("You picked up the oranges.")
      sleep(0.25)
      roll_text("Grocery list item complete: Oranges!")
    
    # Leaving actions. One of the more complicated option lists I've made.
    elif answer in ["leave bus", "leave bus through door", "leave through bus door",
                    "go out of bus", "go out of bus through door", "go out door", "go out through door", "go out through bus door",
                    "get out of bus", "get out of bus through door", "get out through door",
                    "get off bus", "get off bus through door", "get off through bus door", "get off through door",
                    "get off of bus", "get off of bus through door",
                    "exit bus", "exit bus through door", "exit bus through bus door", "exit through door"]:
      next_room = 22
      break
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(23)
      else:
        roll_text("The only helpful book in here might be a bus manual. Sounds pretty boring.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 24 -----
# -------------------
# Started by Luke: 11-28-2017
# Completed by Luke: 11-28-2017
def _24():
  intro = "You walk into a meadow and find a small dwarf with a red beard digging a hole with a shovel."
  if not items_taken["pickaxe"]:
    intro += " A mound of dirt lies next to it with a pickaxe on top."
  
  roll_text(intro)
  diggy_diggy_hole = "Dwarf: *hums* \"I am a dwarf and I'm digging a hole... diggy diggy hole... I'm digging a hole...\""
  if 24 not in rooms_visited:
    roll_text(diggy_diggy_hole)
  elif random.random() < 0.33:
    roll_text(diggy_diggy_hole)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(24)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      next_room = 25
      break
    elif answer in east:
      roll_text("You peer over a large canyon and faintly see a river. You can't just jump into the canyon, though. That's not a good idea.")
    elif answer in south:
      next_room = 19
      break
    elif answer in west:
      roll_text("A thick wall of trees blocks your way. You don't want splinters in your mouth, so you back away.")
      
    # Talk to dwarf actions
    elif answer in ["talk to dwarf", "speak to dwarf", "look at dwarf", "inspect dwarf"]:
      if locked_doors["dwarf"]:
        roll_text("Dwarf: \"Yee, I really always wish'd I had a good ol' sign post. I al'ays wanted ta put a sign right there on me dirt hill, make sure people know it's mine.\"")
      else:
        roll_text("Dwarf: \"Thanks ya mateey for me good ol' sign post. I be very grateful fer it!\"")
    
    # Give sign post actions
    elif answer in ["give dwarf sign post", "give dwarf signpost", "give signpost to dwarf", "give sign post to dwarf",
                    "offer dwarf sign post", "offer dwarf signpost", "offer signpost to dwarf", "offer sign post to dwarf"]:
      if not locked_doors["dwarf"]:
        roll_text("Dwarf: \"Yee, thanks for the offer but eh, I already got me a good ol' sign post.\"")
      elif "sign post" not in inventory:
        roll_text("Dwarf: \"Er, I don't see any sign post on yer person, there. Don't think yer gonna be much use to me.\"")
      else:
        # If dwarf is locked and has sign post in inventory
        inventory.remove("sign post")
        roll_text("You give the sign post to the dwarf.")
        sleep(0.25)
        roll_text("Dwarf: \"Whah, I can't believe it! I has me a sign post! Thank ye so much!\"")
        roll_text("Dwarf: \"Well, I don't have a whole lot ot give ya... Pile o' dirt?\"")
        roll_text("Dwarf: \"Ah, I got one bett'r! I'll give ye me shovel!\"")
        sleep(0.25)
        roll_text("The dwarf gives you his shovel.")
        roll_text("You accept the shovel.")
        inventory.append("shovel")
        items_taken["shovel"] = True
        locked_doors["dwarf"] = False
    
    # Pickaxe actions
    elif answer in ["look at pickaxe", "inspect pickaxe"]:
      if items_taken["pickaxe"]:
        roll_text("There's no pickaxe here. And the dwarf won't give up his shovel.")
      else:
      	roll_text("The pickaxe sits there in the dirt, unattended by the dwarf.")
    
    elif answer in ["get pickaxe", "take pickaxe", "pick up pickaxe", "steal pickaxe"]:
      if items_taken["pickaxe"]:
        roll_text("There's no pickaxe here. And the dwarf won't give up his shovel.")
      else:
        items_taken["pickaxe"] = True
        inventory.append("pickaxe")
        item_descriptions["pickaxe"] = "This used to belong to a dwarf, but now it's yours."
        roll_text("You picked up the pickaxe.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(24)
      else:
        roll_text("That dwarf is digging a hole. He's not handing out self-help books.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 25 -----
# -------------------
# Started by Luke: 11-28-2017
# Completed by Luke: 11-28-2017
def _25():
  intro = "You walk into an abandoned community center. In the middle, you find a decommissioned water fountain; the water looks crystal clear."
  if not items_taken["grass"]:
     intro += "You also see a bag of grass leaning against an eroded wall."
  
  roll_text(intro)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(25)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      next_room = 26
      break
    elif answer in east:
      roll_text("What's that over there? Is that... a waterfall? Eh, you'd have to vault over this canyon in front of you to figure out. Too bad you're not Superman.")
    elif answer in south:
      next_room = 24
      break
    elif answer in west:
      next_room = 27
      break
      
    # Fountain actions
    elif answer in ["look at fountain", "look at water fountain", "inspect fountain", "inspect water fountain", "search fountain", "search water fountain",
                    "walk toward fountain", "walk toward water fountain", "walk to fountain", "walk to water fountain", "approach fountain", "approach water fountain"]:
      if locked_doors["water fountain"]:
        locked_doors["water fountain"] = False
        roll_text("As you approach the fountain, you accidentally kick a rock into the water--sparkles everywhere! A squirrel swims out from where the rock splashed!")
      elif random.random() < 0.33:
        roll_text("As you approach the fountain, you accidentally kick a rock into the water *again*. Sparkles everywhere! A squirrel swims out from where the rock splashed.")
    
    # Grass actions
    elif answer in ["look at grass", "look at bag of grass", "inspect grass", "inspect bag of grass", "search grass", "search bag of grass"]:
      if items_taken["grass"]:
        roll_text("I don't see any grass here. You must be crazy or something.")
      else:
        roll_text("That bag of grass sure looks tasty--I mean, green and beautiful and stuff.")
    
    elif answer in ["get grass", "get bag of grass", "take grass", "take bag of grass", "pick up grass", "pick up bag of grass"]:
      if items_taken["grass"]:
        roll_text("I don't see any grass here. You must be crazy or something.")
      else:
        items_taken["grass"] = True
        inventory.append("grass")
        item_descriptions["grass"] = "This grass sure looks tasty--I mean, green and beautiful and stuff."
        roll_text("You took the bag of grass.")
    
    # Cup actions with fountain. Another of the more complex ones.
    elif answer in ["scoop water", "scoop water with cup", "get water", "get water with cup", "collect water", "collect water with cup", "take water", "take water with cup", "fill cup with water",
                    "scoop fountain water", "scoop water from fountain", "scoop water from fountain with cup", "scoop fountain water with cup",
                    "get fountain water", "get water from fountain", "get water from fountain with cup", "get fountain water with cup",
                    "collect fountain water", "collect water from fountain", "collect water from fountain with cup", "collect fountain water with cup",
                    "take fountain water", "take water from fountain", "take water from fountain with cup", "take fountain water with cup",
                    "fill cup with fountain water", "fill cup with water from fountain"]:
      if "cup" not in inventory:
        if "cup of water" in inventory:
          roll_text("Your cup is already full of water, silly goose.")
        else:
        	roll_text("You don't have a cup to get that water. Ya snooze ya lose.")
      else:
        items_taken["cup of water"] = True
        inventory.remove("cup")
        inventory.append("cup of water")
        del item_descriptions["cup"]
        item_descriptions["cup of water"] = "This is a cup of water. MAGICAL WATEERRRRR!"
        roll_text("You filled your cup with the magical water.")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(25)
      else:
        roll_text("This fountain has no lifeguard (because people totally swim in water fountains), and therefore no one is here to give you a help book or something.")

    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()
  	
    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 26 -----
# -------------------
# Started by Luke: 11-28-2017
# Completed by Luke: 11-28-2017
def _26():
  intro = "You find a circle of marble pillars, grown over with vines."
  if locked_doors["stone bird"]:
    intro += " A pedestal supports a stone bird in the center."
  else:
    intro += " An empty pedestal sits in the middle."
    if not items_taken["rotisserie chicken"] and not locked_doors["stone bird"]:
      intro += " A roasted chicken lies on the ground next to it."
  
  roll_text(intro)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(26)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("You walk into the wall and get all tangled in vines. Not fun. You go back to where you were.")
    elif answer in east:
      roll_text("Behind the wall, you hear flowing water. But alas, you cannot break through a solid stone wall.")
    elif answer in south:
      next_room = 25
      break
    elif answer in west:
      roll_text("You hit your face on a pillar. You retreat to where you stood before.")
      
    # Inspecting bird actions
    elif answer in ["look at bird", "look at stone bird", "inspect bird", "inspect stone bird", "search bird", "search stone bird"]:
      if not locked_doors["stone bird"]:
        if not items_taken["rotisserie chicken"]:
          roll_text("Does that roasted chicken over there count as a bird? It's kinda dead... but sure looks tasty...")
        else:
        	roll_text("I don't see any bird except for you, silly. Get it? Because you're a silly *goose*. Haha. hah. hah...")
      else:
        roll_text("The bird... it glares at you with that menacing stone eyeball, almost like it's alive.")
    
    # Pouring water on bird actions. I'm done saying these are complex.
    elif answer in ["give bird water", "give bird water from cup", "give bird fountain water", "give bird cup water",
                    "give stone bird water", "give stone bird water from cup", "give stone bird fountain water", "give stone bird cup water",
                    "pour water on bird", "pour water from cup on bird", "pour fountain water on bird", "pour fountain water from cup on bird",
                    "pour water on stone bird", "pour water from cup on stone bird", "pour fountain water on stone bird", "pour fountain water from cup on stone bird"]:
      if not locked_doors["stone bird"]:
        roll_text("I don't see any bird except for you, silly. Get it? Because you're a silly *goose*. Haha. hah. hah...")
      else:
        locked_doors["stone bird"] = False
        inventory.remove("cup of water")
        del item_descriptions["cup of water"]
        inventory.append("cup")
        item_descriptions["cup"] = "This cup holds coffee. And water."
        roll_text("You poured the water on the bird.")
        sleep(0.25)
        roll_text("*crack*... *crack crack*")
        sleep(0.5)
        roll_text("*BLAM!* The bird breaks free from its stone form! Behold, the magical flying chicken ascends into the air!")
        roll_text("So majestic, so glorious, so--*ZZZZAAAPPPP!!!*")
        roll_text("The majestic avian creature is struck by the deadly sun laser. The bird plummets down.")
        sleep(0.25)
        roll_text("A roasted chicken lands on the ground, free for the taking.")
    
    # Pick up chicken actions
    elif answer in ["get chicken", "get roasted chicken", "pick up chicken", "pick up roasted chicken", "take chicken", "take roasted chicken"]:
      if items_taken["rotisserie chicken"] or locked_doors["stone bird"]:
        roll_text("What chicken? I don't see any chicken here. That is, unless you're scared, you chicken.")
      else:
        items_taken["rotisserie chicken"] = True
        inventory.append("rotisserie chicken")
        item_descriptions["rotisserie chicken"] = "Tastes like chicken."
        item_descriptions["grocery list"]["rotisserie chicken"] = True
        roll_text("You picked up the chicken.")
        sleep(0.25)
        roll_text("Grocery list item complete: Rotisserie chicken!")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(26)
      else:
        roll_text("The vines... they, they seem to be saying... to go help yourself. Read a book or something.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 27 -----
# -------------------
# Huzzah for filler rooms!
# Started by Luke: 11-28-2017
# Completed by Luke: 11-28-2017
def _27():
  if not items_taken["sign post"]:
  	roll_text("You stop at a wooden sign post. An arrow engraved with \"Community Center\" points east. Another arrow points south, and yet another points west with \"Barber\" engraved in the wood.")
  
  else:
    roll_text("You stop at a hole in the ground. You don't know which direction to go, although you can go any direction.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(27)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("Oh yeah, I forgot to mention, the sign also points north saying, \"Danger: Deadly cliff abyss!\" Best not go there.")
    elif answer in east:
      next_room = 25
      break
    elif answer in south:
      next_room = 28
      break
    elif answer in west:
      next_room = 30
      break
    
    #Look at post action
    elif answer in ["look at post", "look at sign", "look at sign post", "look at wooden sign post"] and not items_taken["sign post"]:
      roll_text("The post is pointing in 3 directions, although it's not stuck into the ground very well. You could probably pull it out.")
    
    elif answer in ["look at post", "look at sign", "look at sign post", "look at wooden sign post"]:
      roll_text("There isn't a sign here, some one must've taken it!")

    #take sign post action
    elif answer in ["take post", "take sign", "take sign post", "take wooden sign post", "pick up post", "pick up sign", "pick up sign post", "pick up wooden sign post", "pull out post", "pull out sign"] and not items_taken["sign post"]:
      roll_text("You rap your arms around the the sign post and lift from the dirt. You then somehow manage to put it in your backpack.")
      roll_text("*You have acquired Sign Post*")
      items_taken["sign post"] = True
      inventory.append("sign post")
      
    elif answer in ["take post", "take sign post", "take wooden sign post", "pick up post", "pick up sign post", "pick up wooden sign post"]:
      roll_text("You can't steal a sign that's already been stolen. -Koob, the book of the century")
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(27)
      else:
        roll_text("The only thing that can help you here is that sign. You could really use a good book, though.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 28 -----
# -------------------
# Started by Luke: 11-28-2017
# Completed by Luke: 11-28-2017
def _28():
  intro = "You walk into a small clearing in a forest."
  # If you haven't given him bonemeal, even if you have given him pancakes, he is sad because his sapling is still small.
  if locked_doors["lumberjack_bonemeal"] and locked_doors["lumberjack_pancakes"]:
    if 26 in rooms_visited:
    	intro += " The lumberjack sits atop a small stump, an axe by his side. He's staring at a small sapling in front of him. Trees surround him and the sapling."
    else:
      intro += " A lumberjack sits atop a small stump, an axe by his side. He's staring at a small sapling in front of him. Trees surround him and the sapling."
  # If you did give him bonemeal and also gave him pancakes, he has chopped down a bunch of trees and is enjoying his pancakes.
  elif not locked_doors["lumberjack_bonemeal"] and not locked_doors["lumberjack_pancakes"]:
    intro += " The lumberjack sits atop a small stump, happily munching on his pancakes. Debris of massacred trees lies all around him."
  # Have given him bonemeal but did not give him pancakes
  elif not locked_doors["lumberjack_bonemeal"] and locked_doors["lumberjack_pancakes"]:
    intro += " The lumberjack stands above a splitered stump across from the one he previously sat on. He breathes heavily, axe in hand, with a satisfied smile on his face."
  # If you have not given him bonemeal but did give him pancakes, he will eat his pancakes but will still be sad about his sapling.
  elif locked_doors["lumberjack_bonemeal"] and not locked_doors["lumberjack_pancakes"]:
    intro += " The lumberjack sits atop a small stump, sadly feeding on his pancakes. The sapling in front of him is still small."
  
  roll_text(intro)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(28)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      next_room = 27
      break
    elif answer in east:
      roll_text("You run into a tree. The feeling of hitting your face on bark is uncomfortable, so you turn away.")
    elif answer in south:
      roll_text("The trees are so dense that way, you would think someone is *trying* to keep you out of there. Or maybe someone is--wait, I'm not allowed to say that...")
    elif answer in west:
      if not locked_doors["lumberjack_pancakes"]:
        next_room = 29
        break
      else:
        roll_text("There's a particularly large tree that way. You can barely see a path behind it, but there's no way you can squeeze through the trees next to it.")

    # Talking to the Luberjack
    elif answer in ["talk to lumberjack", "talk to lumber jack"] and locked_doors["lumberjack_pancakes"] and locked_doors["lumberjack_bonemeal"]:
        roll_text("Lumberjack : Oh hey there adventurer, I'm pretty hungry right now, and this tree isn't grown enough yet, so I'm not in the mood to help you... Man, pancakes sound so good right now...")

    elif answer in ["talk to lumberjack", "talk to lumber jack"] and locked_doors["lumberjack_pancakes"]:
        roll_text("Lumberjack : Oh hey there adventurer, I'm pretty hungry right now, so I'm not in the mood to help you. Man, pancakes sound so good right now...")

    elif answer in ["talk to lumberjack", "talk to lumber jack"] and locked_doors["lumberjack_bonemeal"]:
        roll_text("Lumberjack : Oh hey there, I really wish this sapling will grow up soon, I really want to chop it down... Maybe you can help it grow faster? Oh, I can also cut something in half for you!")

    elif answer in ["talk to lumberjack", "talk to lumber jack"]:
        roll_text("Lumberjack : Well hey there buddy, need anything chopped in half? Just give it to me and I'll do all the work fer yeah!")
      
    # Giving bonemeal actions
    elif answer in ["give lumberjack bonemeal", "give bonemeal to lumberjack"]:
      if "bonemeal" not in inventory:
        roll_text("You don't have any bonemeal to give! Thou cannot giveth what thou doth not haveth!")
      elif not locked_doors["lumberjack_bonemeal"]:
        # If somehow you have bonemeal after having given it to the lumberjack
        roll_text("This lumberjack doesn't need any more bonemeal. He has satisfied the desire to grow his tree and chop it down.")
      else:
        # If you have bonemeal and have not given it to him yet
        inventory.remove("bonemeal")
        locked_doors["lumberjack_bonemeal"] = False
        roll_text("You give the bonemeal to the lumberjack.")
        sleep(0.25)
        roll_text("Lumberjack: \"Aw, thanks! Now I can grow my tree, and CHOP IT DOWN!!!\" *maniacal laugh*")
        roll_text("Lumberjack: *throws bonemeal onto sapling*")
        roll_text("There is a quake in the ground... *rrrruummmmmbbbbllleeee*")
        roll_text("Suddenly, the sapling springs up from the ground, shooting up toward the sky.")
        roll_text("In seconds, you and the lumberjack behold a hefty 7-meter wide tree, towering high and mighty.")
        sleep(0.25)
        roll_text("Lumberjack: *another maniacal laugh* \"YES! I shall cut this tree down, along with everything else that stands in my way!!!\"")
        roll_text("You take a cautious step back as the lumberjack goes on his rampage.")
        roll_text("*CHOP*, *CHOP*, *CHOP*. First he strikes down the new-grown tree, then he hacks down every other tree in the immediate vicinity.")
        sleep(0.25)
        roll_text("*CRACK*")
        sleep(0.25)
        roll_text("He chopped down the tree that blocks the path to the west! Huzzah!")
        roll_text("The tree falls over, revealing the path to the spooky place of westernlands... Oooohh...")
    
    # Giving pancakes actions
    elif answer in ["give lumberjack pancakes", "give pancakes to lumberjack", "feed lumberjack pancakes", "feed lumberjack with pancakes"]:
      if "pancakes" not in inventory:
        roll_text("You don't have any pancakes, which is disappointing, because pancakes are delicious.")
      elif not locked_doors["lumberjack_pancakes"]:
        # Again, if they manage to cheat the game in some way that doesn't even matter
        roll_text("The lumberjack has already received the delicious gift of pancakes, no need to give him more. More for you!")
      else:
        # Has pancakes, has not given them to lumberjack
        inventory.remove("pancakes")
        locked_doors["lumberjack_pancakes"] = False
        roll_text("Lumberjack: \"Pancakes? PANCAKES?! Oh my, thank you so much.\"")
        roll_text("Lumberjack: *swipes pancakes from you and begins chowing down*\"")
        roll_text("Lumberjack: *talks with mouth full* \"I don't got any money, but if you need somethin' split in half, I'm really super good at that. Just hit me up if you need somethin'.\"")
    
    # Giving pickaxe to lumberjack actions
    elif answer in ["give lumberjack pickaxe", "give lumberjack pickaxe to split in half", "give lumberjack pickaxe to chop in half", "give lumberjack pickaxe to cut in half",
                    "give pickaxe to lumberjack", "give pickaxe to lumberjack to split in half", "give pickaxe to lumberjack to chop in half", "give pickaxe to lumberjack to chop in half"]:
      if "pickaxe" not in inventory:
        roll_text("What pickaxe? You don't have a pickaxe, you silly.")
      elif not locked_doors["lumberjack_pickaxe"]:
        # If game hax
        roll_text("First, you don't need to give this guy another pickaxe. Second, how do you even have another pickaxe? Like, seriously. *scoffs*")
      elif locked_doors["lumberjack_pancakes"]:
        # Has not given pancakes yet
        roll_text("That lumberjack is big and beefy. You better not go around giving him pickaxes unless he's a happy fellow.")
      else:
        # Has pickaxe and has not given it yet, but has given pancakes
        inventory.remove("pickaxe")
        locked_doors["lumberjack_pickaxe"] = False
        roll_text("Lumberjack: \"Alrighty, let's see what I can do fer ya here.\"")
        roll_text("The lumberjack balances the pickaxe on his sitting stump. Then he heaves back with his axe, and...")
        roll_text("*WHAM!* The pickaxe splits into two, smaller pickaxes.")
        roll_text("Lumberjack: *hands you the pickaxes* \"Now you got yourself some ice picks. It gets real cold up north of here. Good luck!\"")
        inventory.append("ice picks")
        item_descriptions["ice picks"] = "Good for climbing giant walls of ice."
        items_taken["ice picks"] = True
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(28)
      else:
        roll_text("There may be a lot of wood here, but paper and help books don't magically pop out of trees.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# -------------------
# ----- Room 29 -----
# -------------------
# Started by Christian: 11-28-2017
# Finished by Christian: 11-28-2017
def _29():
  roll_text("You walk up to a grave surrounded by small creatures, a sword with a blue handle is encased in the grave stone. Atop the sword is a green cap with a red band along the base. An apple tree stands over the grave as if it were guarding it.")
  
  while True:
    answer = input(">").lower()
    
    # Map command # *** EDIT MAP ROOM NUMBER *** #
    if answer in _map:
      if items_taken["koob"]:
        display_map(29)
      else:
        roll_text("You don't have a map even though you should start with one in every game? Wait... Wrong game, sorry!")
    
    # Navigation
    elif answer in north:
      roll_text("Symmetrical trees and bushes are in your way...")
      
    elif answer in east:
      next_room = 28
      break
                  
    elif answer in south:
      roll_text("A ton of bushes are in the way, and you don't know how to pick them up...")
      
    elif answer in west:
      roll_text("You start to walk west, but you find a row of symmetrical trees that are completely solid.")
      
    # Actions
    # Look at Actions
    elif answer in ["look at sword"]:
      roll_text("Its jutting out of the top of the grave stone, it doesn't look like it's gonna budge anytime soon.")
    
    elif answer in ["look at grave", "look at grave stone"]:
      roll_text("You look closer to find \"10/10 Would seal Ganon away again.\" There isn't really anything else.")
            
    elif answer in ["look at cap", "look at green cap"] and not items_taken["green cap"]:
      roll_text("The cap is really smooth, like you can't see the knitting smooth. It also has a red band at the base.")
    
    elif answer in ["look at cap", "look at green cap"]:
      roll_text("Cap? There isn't a cap resting on the hilt of that sword.")
    
    elif answer in ["look at tree", "look at apple tree"]:
        roll_text("The tree is very symmetrical, but it's more bouncy and fluffy than the other trees. It also has apples in it.")
    
    #take/pick up Actions
    elif answer in ["pick up sword", "take sword", "lift sword"]:
      roll_text("You place your hands on the handle and proceed to lift the sword. Although, absolutely nothing happnes, the sword doesn't move an atom.") 
      sleep(.5)
      roll_text("I've heard that only a true hero can lift the sword, well, the true hero of Hyrule. Wrong game though...")
    
    elif answer in ["pick up cap", "take cap", "pick up green cap", "take green cap"] and not items_taken["green cap"]:
      roll_text("You lift the cap from the handle, placing it on your head. I mean, why put it in your bag when it fits on your head?")
      items_taken["green cap"] = True
    
    elif answer in ["pick up cap", "take cap", "pick up green cap", "take green cap"]:
      roll_text("You look and look, but can't seem to find a cap to pick up...")
    
    elif answer in ["pick an apple", "pick up apple", "take apple"] and not items_taken["apple"]:
      roll_text("You reach up to grab an apple from the tree.")
      roll_text("*You have acquired Apple*")
      roll_text("You proceed to check off Apple from your grocery list.")
      inventory.append("apple")
      items_taken["apple"] = True
    
    elif answer in ["pick an apple", "pick up apple", "take apple"]:
      roll_text("The apples look really good, but you already have one, wouldn't want to disturb the tree.")
      
    elif answer in ["take grave", "pick up grave", "take grave stone", "pick up grave stone", "lift grave", "lift grave stone"]:
      roll_text("Why would you even try this???")
    
    # If you need help from Koob, cause why not? # *** EDIT GUIDE AND HELP MESSAGE *** #
    elif answer in _help:
      if items_taken["koob"]:
      	guide(29)
      else:
        roll_text("Hey Listen! Koob isn't here to help you! And I, Navi, am not of much help either!")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 30 -----
# -------------------
# Started by Luke: 11-29-2017
# Completed by Luke: 11-29-2017
def _30():
  roll_text("You approach a large cliff face, A length a rope swings at eye level, leading up to a ledge on the cliff. There's also a small house to the west, with a sign over the door saying \"Barber.\"")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(30)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("That's the direction of the swinging rope. Maybe you should try climbing it?")
    elif answer in east:
      next_room = 27
      break
    elif answer in south:
      roll_text("The dense forest blocks your way in that direction. You'll have to try a different way.")
    elif answer in west:
      next_room = 31
      break
      
    # Rope actions
    elif answer in ["look at rope", "inspect rope", "search rope", "test rope", "grab rope", "grab on rope", "grab onto rope"]:
      roll_text("That rope looks like it leads up to that ledge up there. Perhaps you should climb it.")
    
    elif answer in ["climb rope", "climb rope to ledge", "climb up", "climb up rope", "climb up to ledge", "climb up rope to ledge"]:
      next_room = 32
      break
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(30)
      else:
        roll_text("It doesn't appear that there would be a helpful book around here anywhere, not even in that barber shop.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken
                  
  
# -------------------
# ----- Room 31 -----
# -------------------
# Started by Christian: 11-29-2017
# Finished by Christian: 11-29-2017
def _31():
  if not items_taken["pills"] and not items_taken["scissors"]:
  	roll_text("You walk into a barber shop. The man running the shop is busy cutting the hair of a mountain goat. All of the other chairs are empty. You also see Sleeping Pills on a counter.")
  elif not items_taken["pills"]:
    roll_text("You walk into the barber shop. The man running the shop is sitting at the counter, looking bored beyond redemption. All of the other chairs are empty. You also see Sleeping Pills on a counter.")
  elif not items_taken["scissors"]:
    roll_text("You walk into the barber shop. The man running the shop is busy cutting the hair of a mountain goat. All of the other chairs are empty.")
  else:
    roll_text("You walk into the barber shop. You see the owner sitting at the counter, twirling his hair waiting for more customers...")
  
  while True:
    answer = input(">").lower()
    
    # Map command # *** EDIT MAP ROOM NUMBER *** #
    if answer in _map:
      if items_taken["koob"]:
        display_map(31)
      else:
        roll_text("You don't have a map, but I can tell that you're on the very west")
    
    # Navigation
    elif answer in north:
      roll_text("There is a wooden wall, there's also a stone mountain behind that wall.")
      
    elif answer in east or answer in ["exit barber", "walk out door", "exit building", "leave", "leave building"]:
      next_room = 30
      break
      
    elif answer in south:
      roll_text("There are some couchs and seats, but no openings or paths...")
      
    elif answer in west:
      roll_text("You walk into the back of the barber shop, although there isn't a back door.")
      
    # Actions
    # Look at stuff actions
    elif answer in ["look at goat"] and locked_doors["goats hair cut"]:
      roll_text("The goat seems to be really bored, though it's stomach is growling like crazy, I bet you it wants some nice grass.")
    
    elif answer in ["look at goat"]:
      roll_text("There is no goat.")
    
    elif answer in ["look at sleeping pills", "look at pills"] and not items_taken["pills"]:
      roll_text("They're sitting on the counter, just begging to be taken.")
    
    elif answer in ["look at sleeping pills", "look at pills"]:
      roll_text("They're gone! Some greedy person must've taken them...")
    
    elif answer in ["look at man"]:
      roll_text("He looks bored as he works on stuff...")
    
    #give goat grass action
    elif answer in ["give goat grass", "feed goat grass", "use grass on goat"] and "grass" in inventory:
      roll_text("You get out some grass and hand it to the goat. It excitedly almost bites your hand off and takes off out the door.")
      roll_text("The barber is a bit annoyed at first, then he drops it pretty fast.")
      sleep(.5)
      roll_text("Barber : Well, i'm free if you needed a hair cut. Just come talk to me.")
      locked_doors["goat hair cut"] = False
    
    elif answer in ["give goat grass", "feed goat grass", "use grass on goat"] and locked_doors["goat hair cut"]:
      roll_text("You don't have nay grass to give.")
    
    elif answer in ["give goat grass", "feed goat grass", "use grass on goat"]:
      roll_text("There isn't a goat to feed.")
    
    # take/pick up pills action
    elif answer in ["take sleeping pills", "take pills", "pick up sleepng pills", "pick up pills"] and not items_taken["pills"]:
      roll_text("You rap your fingers around the bottle, a weird tingly feeling fills your body. Oh my, what might you do with these?")
      roll_text("*You have acquired Sleeping Pills*")
      items_taken["pills"] = True
      inventory.append("pills")
    
    elif answer in ["take sleeping pills", "take pills", "pick up sleepng pills", "pick up pills"]:
      roll_text("Maaaan, there aren't any pills left...")
    
    # talk to barber action
    elif answer in ["talk to barber"] and locked_doors["goat hair cut"]:
      roll_text("Barber : Sorry, but you're going to have to wait for the goat. He's not moving anytime soon...")
      sleep(.5)
      roll_text("Barber : He seems, pretty hungry though...")
    
    elif answer in ["talk to barber"] and not items_taken["scissors"]:
      roll_text("Barber : You're ready then? Alright, time for a hair cut!")
      roll_text("The Barber takes out some scissors and begins his work.")
      sleep(1)
      roll_text("Barber : Uhhhh, I've ran into a problem... The scissors are now stuck in your hair.")
      sleep(.5)
      roll_text("Barber : So, uhh, you can go, free of charge, and you can keep the scissors to... Make sure to try and get them out sometime. So cya!")
      roll_text("He then walks back behind the counter to sit down and be bored...")
      sleep(.5)
      roll_text("You get up from your seat and began to walk off, but the scissors fall out of your hair. No use in wasting them.")
      roll_text("*You have acquired Scissors*")
      items_taken["scissors"] = True
      inventory.append("scissors")
    
    elif answer in ["talk to barber"]:
      roll_text("Barber : Oh hey... I don't have any spair scissors, soooo, I can't do much of anything... I just get to sit here and, be bored I guess...")
    
    elif answer in ["give scissors to barber", "give scissors barber"]:
      roll_text("Barber : Huh? I said you can keep those, besides, they're covered in hero germs now...")
      
    # If you need help from Koob, cause why not? # *** EDIT GUIDE AND HELP MESSAGE *** #
    elif answer in _help:
      if items_taken["koob"]:
      	guide(31)
      else:
        roll_text("The shop owner is too bored to notice your call for help, and there's nothing else to hear it.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 32 -----
# -------------------
# Started by Luke: 11-29-2017
def _32():
  intro = "After a long climb you reach a flat on the side of the mountain, finding"
  if not items_taken["magic rock"]:
    intro += " a large stone fist blocking a cave and"
  intro += " an icy wall leading to the peak."
  
  if locked_doors["leaf lump"]:
    intro += " There's also a small lump under the layer of snow beside the cave."
  elif not items_taken["blank leaf"]:
    intro += " There's also a golden leaf, frozen in ice, beside the cave."
  
  roll_text(intro)
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(32)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("There's an ice wall right there, you'll need to climb it with ice picks.")
      
    elif answer in east:
      roll_text("Careful, you're going to fall off that cliff! That would be bad.")
      
    elif answer in south or answer in ["climb down rope", "climb down", "climb back down", "climb back down rope"]:
      next_room = 30
      break
      
    elif answer in west or answer in ["go into cave", "go through cave", "enter cave", "go to cave"]:
      if not locked_doors["stone fist"]:
        next_room = 33
        break
      
      else:
        roll_text("A large stone fist blocks your way.")
      
    # Lump actions
    elif answer in ["look at lump", "look at lump of snow", "look at snow lump", "inspect lump", "inspect lump of snow", "inspect snow lump",
                    "search lump", "search lump of snow", "search snow lump"]:
      if not locked_doors["leaf lump"]:
        message = "I don't see any lumps here."
        if not items_taken["blank leaf"]:
          message += " I do see a leaf encased in ice, though."
        roll_text(message)
      else:
        locked_doors["leaf lump"] = False
        roll_text("Under the lump of snow, there's a leaf encased in ice. It looks very well preserved.")
    
    # Pick up leaf actions
    elif answer in ["get leaf", "get leaf in ice", "get leaf encased in ice",
                    "pick up leaf", "pick up leaf in ice", "pick up leaf encased in ice",
                    "take leaf", "take leaf in ice", "take leaf encased in ice"]:
      if items_taken["blank leaf"]:
        roll_text("There's no leaf here. What do you think you're talking about?")
      else:
        locked_doors["leaf lump"] = False
        items_taken["blank leaf"] = True
        inventory.append("blank leaf")
        item_descriptions["blank leaf"] = "This leaf is so freshly preserved, it could belong to a living tree."
        roll_text("You took the leaf.")
    
    # Stone fist actions
    elif answer in ["use paper on fist", "use paper on stone fist", "use paper on large stone fist", "use paper on giant stone fist",
                    "use magic paper on fist", "use magic paper on stone fist",
                    "use magic paper on large stone fist", "use magic paper on giant stone fist",
                    "use magical paper on fist", "use magical paper on stone fist",
                    "use magial paper on large stone fist", "use magical paper on giant stone fist",
                    "throw paper on fist", "throw paper on stone fist", "throw paper on large stone fist", "throw paper on giant stone fist",
                    "throw magic paper on fist", "throw magic paper on stone fist",
                    "throw magic paper on large stone fist", "throw magic paper on giant stone fist",
                    "cover fist with paper", "cover stone fist with paper",
                    "cover large stone fist with paper", "cover giant stone fist with paper",
                    "cover fist with magic paper", "cover stone fist with magic paper",
                    "cover large stone fist with magic paper", "cover giant stone fist with magic paper",
                    "cover fist with magical paper", "cover stone fist with magical paper",
                    "cover large stone fist with magical paper", "cover giant stone fist with magical paper"]:
      if not locked_doors["stone fist"]:
        if not items_taken["magic rock"]:
          roll_text("There's no stone fist here, just a pile of rocks where one used to be.")
          roll_text("But look at that one... that one looks very magical.")
        else:
          roll_text("There's no stone fist here, just a pile of rocks where one used to be.")
      elif "magic paper" not in inventory:
        roll_text("You don't have any kind of magic paper that would beat a rock this size.")
      else:
        inventory.remove("magic paper")
        roll_text("You threw the magic paper onto the rock.")
        sleep(0.25)
        roll_text("*crack*, *CRACK*...")
        sleep(0.25)
        roll_text("*CRASH!!!*")
        roll_text("The giant stone fist breaks apart and falls to the ground in pieces.")
        roll_text("Deep in the heart of what used to be the fist, one of the rocks glows magically.")
      
    # Pick up magic rock actions
    elif answer in ["get rock", "get glowing rock", "get magic rock", "get magical rock",
                    "pick up rock", "pick up glowing rock", "pick up magic rock", "pick up magical rock",
                    "take rock", "take glowing rock", "take magic rock", "take magical rock"]:
      if locked_doors["stone fist"]:
        roll_text("What rock? That fist? That's too big for you to carry!")
      elif items_taken["magic rock"]:
        roll_text("There's no significant rock to take here, just a pile of regular ol' rocks.")
      else:
        inventory.append("magic rock")
        items_taken["magic rock"] = True
        item_descriptions["magic rock"] = "This looks really nice to throw at someone. Or something. Or just not be so violent with."
        roll_text("You took the magic rock.")
      
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(32)
      else:
        roll_text("You're not going to find a self-help book here. At least, if you do, it'll be all frozen and stuff.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken


# -------------------
# ----- Room 33 -----
# -------------------
# Started by Christian: 11-30-2017
# Finished by Christian: 11-30-2017
def _33():
  global end
  roll_text("You walk into the cave to find a hooded figure facing you, their face is hidden in the shadow of their hood.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(33)
      else:
        roll_text("Do you really need a map at this point?")
    
    # Navigation
    elif answer in north:
      roll_text("There's only a cave wall, and you can't go through cave walls...")
      
    elif answer in east:
      next_room = 32
      break
      
    elif answer in south:
      roll_text("It's wall, of stone, which is solid, and, not, passable...")
      
    elif answer in west:
      roll_text("You just can't go that way, there isn't anything...")
      
    # Actions
    #look at hooded figure Action
    elif answer in ["look at hooded figure", "look at figure"]:
      roll_text("They're just standing there patiently.")
    
    #talk to hooded figure Action
    elif answer in ["talk to hooded figure", "talk to figure"] and not list_complete:
      roll_text("???? : You're back? But you don't have everything yet? Come on... I told you to not come back until you got everyhting, I even gave you a list...")
      roll_text("???? : Well go on then, go get everything then come back.")
    
    elif answer in ["talk to hooded figure", "talk to figure"] and list_complete:
      roll_text("???? : Wait, you have everything? Well good job! We can finally have dinner. Took you long enough though, I'm practically starving to death now.")
      roll_text("The figure pulls down their hood to reveal the face of a girl, roughly your age.")
      sleep(1)
      roll_text("You : Wait, you took your hood off Lizz?")
      sleep(.5)
      roll_text("Lizz : Well I don't want to get my hood dirty do I? Well anyways, let's get to cooking!")
      sleep(1)
      roll_text("Lizz : I look forward to the meal!")
      
      end = 2
      break
      
    
    # If you need help from Koob, cause why not? # *** EDIT GUIDE AND HELP MESSAGE *** #
    elif answer in _help:
      if items_taken["koob"]:
      	guide(33)
      else:
        roll_text("I don't think you need help at this point.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

# -------------------
# ----- Room 34 -----
# -------------------
# LAST ROOOOOOOOMMMM!!!!
# Started by Luke: 11-30-2017
# Completed by Luke: 11-30-2017
def _34():
  roll_text("You reach the peak of the mountain, finding a flat plane in a blanket of snow. A small man in a white robe appears to be meditating in the middle of it all.")
  
  while True:
    answer = input(">").lower()
    
    # Map command
    if answer in _map:
      if items_taken["koob"]:
        display_map(34)
      else:
        roll_text("What map? You don't have a map, silly goose.")
    
    # Navigation
    elif answer in north:
      roll_text("That edge over there looks too spooky. Don't wanna go over there.")
    elif answer in east:
      roll_text("You peer over the ledge. You are terrified of slipping. You return to safe grounds.")
    elif answer in south:
      roll_text("There's an ice wall down there. You'll have to climb down it to go south.")
    elif answer in west:
      roll_text("There doesn't appear to be safe passage down that way. Can't really go there.")
      
    # Talk to man actions
    elif answer in ["look at man", "look at small man", "look at little man",
                    "talk to man", "talk to small man", "talk to little man",
                    "interact with man", "interact with small man", "interact with little man"]:
      if not locked_doors["mountain man"]:
        roll_text("Small man: \"I already gave you what you needed. Now shoo, go away my child.\"")
      else:
        roll_text("The man rises up and addresses you.")
        roll_text("Small man: *with strange accent* \"Hello there. You have come here out of curiosity, but I know all things. I know just what you need.\"")
        sleep(0.25)
        roll_text("The man offers you a river rock embedded in a stick.")
        roll_text("This is exactly what you need to fulfill your destiny. Now take it.")
        sleep(0.25)
        roll_text("You accept the river rock stick.")
        acquire_cane("river rock cane")
    
    # Descending ice wall actions
    elif answer in ["climb down", "climb down ice wall", "climb down ice wall with ice picks", "climb down with ice picks",
                    "descend ice wall", "descend ice wall with ice picks", "descend with ice picks"]:
      roll_text("You climbed down the ice wall.")
      next_room = 33
      break
    
    # If you need help from Koob, cause why not?
    elif answer in _help:
      if items_taken["koob"]:
      	guide(34)
      else:
        roll_text("That little man is not going to give you a book, though one of those things might help a lot.")
    
    # Look into backpack action
    elif answer in ["look in backpack", "backpack", "inventory", "look in inventory"]:
      backpack()

    # If answer doesn't fit anything
    else:
      roll_text(random.choice(unknown_responses))

  return inventory, next_room, locked_doors, items_taken

                  
# Actual Game Starts After This Comment
roll_text("Welcome!")
roll_text("Here are the Instructions!")
if input("Press Enter... Or type skip to skip tutorial.").lower() not in ["skip", " skip", "skip tutorial", "skip instructions", "s"]:
  roll_text("Ok, so, here is all of the commands you will be using -")
  sleep(1)
  roll_text("Look at \"object\" : Use this command to look at things and find out more about them, you're going to need to use this to find items and figure at puzzles.")
  roll_text("Pick up / Take \"Object\" : Use this to take or pick up items, pretty self explanatory.")
  roll_text("Talk to \"thing or person\" : Type in this command to talk to a person or thing, although it will only work for living things.")
  roll_text("Give \"item\" to \"thing or person\" : This will allow you to give items to entities to complete so called quests.")
  roll_text("Use \"item\" on \"thing or person\" : You can use items on things to, although it's not as vast as you may like it to be. In other words, you can't use anything on anything.")
  roll_text("You can also check you inventory/backpac by typing \"backpack\" or \"inventory\".")
  roll_text("???? : Then there are generic commands, which are, well, obvious. Like opening something.")
  sleep(1)
  roll_text("???? : Oh yeah! You can also move about the world by typing in a specific direction, such as North, East, South or West.")

  roll_text("???? : That should be everything, and make sure to look everywhere! Cya soon!")
  sleep(1)
  roll_text("???? : Maybe...")
  input("Press Enter...")

game = True
end = 0
rooms = [_01, _02, _03, _04, _05, _06, _07, _08, _09, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _20, _21, _22, _23, _24, _25, _26, _27, _28, _29, _30, _31, _32, _33, _34]

while game:
  print("-------------------------")
  # Checking if Grocery List is complete
  if items_taken["tomato"] and items_taken["bacon"] and items_taken["dozen eggs"] and items_taken["blue berries"] and items_taken["banana"] and items_taken["oranges"] and items_taken["rotisserie chicken"] and items_taken["watermelon"] and items_taken["apple"]:
    list_complete = True
  
  if next_room not in rooms_visited:
  	rooms_visited.append(next_room)
  inventory, next_room, locked_doors, items_taken = rooms[next_room-1]()
  print() #Seperate rooms= text stuff
  if end:
    game = False

#Put ending or something for when the game ends
if end == 1:
  if items_taken["koob"]:
  	roll_text("Koob : Welp, guess I should go find another adventure to bug through out their journey. Maybe the who died will restart the game and I can bug them some more...")
  
  else:
    roll_text("You are all alone now, except inside a magical old man.")
    sleep(1)
    roll_text("Ethereal Lüke : You still have a second chance. You can always just...")
    sleep(1.5)
    roll_text("Reset The Game.")

elif end == 2:
  roll_text("You sit down at the dinner table. The smell of hot food fills your nostrils.")
  sleep(1)
  roll_text("You feel fulfilled, your journey is complete.")

roll_text("In the game - Roshambo Quest")
