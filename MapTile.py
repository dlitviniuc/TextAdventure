import enemy

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Campfire(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.used = False
    def intro_text(self):
        if not self.used:
            print( "You see a flickering light down the corridor, it looks like a fire, you approach carefully and indeed it is a well put-together campfire")
        else:
            print( "You enter the room and see a used campfire, only ash remains of the wood and no food in sight. There is some water tho, rejoyce")
    def rest(self, character):
        if not self.used:
            res = input("Would you like to rest up? You can return later if you don't (Y/N)")
            if res.upper() == "Y":
                character.heal(30)
                print("You now have {} HP".format(character.hp))
                self.used = True
            if res.upper() == "N":
                print("You go further in the cave, knowing you have a place to rest in case you need it")
            
class StartRoom(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
    def intro_text(self):
        print("You enter the infamous dungeon, riches surely await further in!!")

class EndRoom(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
    def intro_text(self):
        print("At long last, the exit!!")
        res = input("Do you want to leave? (Y/N)")
        if res.upper() == "Y":
            print("You leave the dungeon! But are you free?")
            return True
        if res.upper() == "N":
            print("You turn back, greed written on your eyes, will you be able to get back?")
        else:
            self.intro_text()

class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.present = True
        self.item = item
        super().__init__(x, y)
    
    def intro_text(self):
        if self.present:
            res = input("Wow, you found: {}\n {} \n Pick up? (Y/N)".format(self.item.name, self.item.description))
            if res.upper() == "Y":
                self.present = False
                return self.item
            else:
                print("You leave it on the floor, maybe it was cursed")
        else:
            print("You already took all the treasure in this room")
    
    def character_pickup(self):
        return self.item
class EmptyCavePath(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def intro_text(self):
        print("The same old moist walls and dark corners, you should check what's further in")
    
class SpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Spider())

    def intro_text(self):
        if self.enemy.is_alive():
            print("A giant, hairy and monstrous spider looks down on you from the ceiling, it's about to jump on you")
        else:
            print("The putrid corpse of a spider lays in the corner, something took a bite out of it, keep an eye out")
    
class GoblinRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Goblin())

    def intro_text(self):
        if self.enemy.is_alive():
            print( """A little green creature is wimpering in the corner, maybe you should help it.
            \n You go and try to ask if it's ok when it turns around, grinning and attacking you with a knife""")
        else:
            print("This room is really gross, the walls are covered in blood. You notice a green pointy ear in the mess")
        
class SkeletonRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Skeleton())

    def intro_text(self):
        if self.enemy.is_alive():
            print( """You hear the rattling of bones and see two red dots rapidly aproaching""")
        else:
            print( "Just a dusty pile of bones, maybe it was a brave warrior like yourself")

class ImpRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Imp())

    def intro_text(self):
        if self.enemy.is_alive():
            print( """A little red ball hovers in the air, kept airborne by two small wings\n
            As it turns toward you, attracted by the delicious smell of your soul, you see that it's face is one big mounth full of jagged teeth""")
        else:
            print("Hey, a kicking ball is just layinh there finally something fun in this nightmare.\nAs you kick it you hear a splosh uppon it kicking the wall \n you just made art?")

class GiantRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Giant())

    def intro_text(self):
        if self.enemy.is_alive():
            print( """You hear breathing from the hall, you run in, maybe it's a fellow adventurer to keep you company in this hole.\n
            You run up and start getting suspicious, there is no fire, it's totally dark and it smells soo bad you start retching.\n
            You understand that something is terribly wrong. As you try to turn around you hear the shuffling of steps,\n
            as you turn to see what it is, you mouth hangs open involuntarily, it's a GIANT, fully 5mt tall and running to you with a big bone in hand, RUN!""")
        else:
            print( "A lumbering figure is masked by the shadows, you hear nothing but your steps.\n As you get closer you see it's dead and really smelly.\nA giant, surely felled by a mighty warrior")

