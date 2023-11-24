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
            return "You see a flickering light down the corridor, it looks like a fire, you approach carefully and indeed it is a well put-together campfire\nDo you want to take a rest?\n"
        else:
            return "You enter the room and see a used campfire, only ash remains of the wood and no food in sight. There is some water tho, rejoyce\n"
    def rest(self):
        if not self.used:
            #res = input("Would you like to rest up? You can return later if you don't (Y/N)")
            return "Would you like to rest up? You can return later if you don't"
    def choice(self, character, choice):
            if choice:
                character.heal(30)
                self.used = True
                return "You now have {} HP\n".format(character.hp)
            if not choice:
                return "You go further in the cave, knowing you have a place to rest in case you need it\n"
            
class StartRoom(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
    def intro_text(self):
        return "You enter the infamous dungeon, riches surely await further in!!\n"

class EndRoom(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
    def intro_text(self):
        return "At long last, the exit!!\nDo you want to leave?"
    def choice(self, character, choice):
        #res = input("Do you want to leave? (Y/N)")
        if choice:
            return "You leave the dungeon! But are you free?\n"
        else:
            return "You turn back, greed written on your eyes, will you be able to get back?\n"
            
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
            return "Wow, you found: {}\n {} \n Pick up?\n".format(self.item.name, self.item.description)
        else:
            return "You already took all the treasure in this room\n"
    def choice(self, character,choice):
        if choice:
            self.present = False
            character.pickup(self.item)
            return "You pick {} up!\n".format(self.item.name)
        else:
            return "You leave it on the floor, maybe it was cursed\n"
    
class EmptyCavePath(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def intro_text(self):
        return "The same old moist walls and dark corners, you should check what's further in\n"
    
class SpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Spider())

    def intro_text(self):
        if self.enemy.is_alive():
            return "A giant, hairy and monstrous spider looks down on you from the ceiling, it's about to jump on you\n"
        else:
            return "The putrid corpse of a spider lays in the corner, something took a bite out of it, keep an eye out\n"
    
class GoblinRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Goblin())

    def intro_text(self):
        if self.enemy.is_alive():
            return """A little green creature is wimpering in the corner, maybe you should help it.
You go and try to ask if it's ok when it turns around, grinning and attacking you with a knife\n"""
        else:
            return "This room is really gross, the walls are covered in blood. You notice a green pointy ear in the mess\n"
        
class SkeletonRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Skeleton())

    def intro_text(self):
        if self.enemy.is_alive():
            return """You hear the rattling of bones and see two red dots rapidly aproaching\n"""
        else:
            return "Just a dusty pile of bones, maybe it was a brave warrior like yourself\n"

class ImpRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Imp())

    def intro_text(self):
        if self.enemy.is_alive():
            return """A little red ball hovers in the air, kept airborne by two small wings
As it turns toward you, attracted by the delicious smell of your soul, you see that it's face is one big mounth full of jagged teeth\n"""
        else:
            return "Hey, a kicking ball is just layinh there finally something fun in this nightmare.\nAs you kick it you hear a splosh uppon it kicking the wall \nyou just made art?\n"

class GiantRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemy.Giant())

    def intro_text(self):
        if self.enemy.is_alive():
            return  """You hear breathing from the hall, you run in, maybe it's a fellow adventurer to keep you company in this hole.\n
You run up and start getting suspicious, there is no fire, it's totally dark and it smells soo bad you start retching.\n
You understand that something is terribly wrong. As you try to turn around you hear the shuffling of steps,\n
as you turn to see what it is, you mouth hangs open involuntarily, it's a GIANT, fully 5mt tall and running to you with a big bone in hand, RUN!\n"""
        else:
            return  "A lumbering figure is masked by the shadows, you hear nothing but your steps.\n As you get closer you see it's dead and really smelly.\nA giant, surely felled by a mighty warrior\n"

