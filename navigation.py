#create player
#create map
#put player in map start
#show intro text and attack/pickup if possible
#show directions available
#move to one direction
#repeat steps till player leaves dungeon
#navigation looks ok, add combat and control console to clear each time before printing

from Map import Mappa
from character import Character
import MapTile
from combat import Encounter
from item import Item

endGame = False

class Navigation:
    def __init__(self) -> None:
        self.map = Mappa()
        self.char = Character("Player", 50, 50, 0, 2)
        self.position = self.map.start

    def start(self):
        global endGame
        while not endGame:
            print("\033c", end='')
            self.map.printWorld()
            print(self.position)
            answer = self.map._world[self.position].intro_text()
            #check if the tile is an encounter
            if isinstance(self.map._world[self.position], MapTile.EnemyRoom):
                encounter = Encounter(self.char, self.map._world[self.position].enemy)
                encounter.fight()
            #check if the tile is a loot room
            if isinstance(answer, Item):
                self.char.pickup(answer)
            if isinstance(self.map._world[self.position], MapTile.Campfire):
                print("You have {}/{} HP".format(self.char.hp, self.char.maxhp))
                self.map._world[self.position].rest(self.char)
            #check if the tile returned true meaning it's an end room and the user chose to leave
            if answer==True:
                endGame=True
                break
            self.step()
    #allow user to take a step on the map
    def step(self):
        directions = self.showDirections()
        choice = input("You can go {}\n".format(directions))
        if choice.upper() in directions:
            if choice.upper() == "UP":
                self.position = (self.position[0]-1, self.position[1])
            if choice.upper() == "DOWN":
                self.position = (self.position[0]+1, self.position[1])
            if choice.upper() == "LEFT":
                self.position = (self.position[0], self.position[1]-1)
            if choice.upper() == "RIGHT":
                self.position = (self.position[0], self.position[1]+1)
    #check the directions available from the current position
    def showDirections(self):
        rooms = [1,2,3,6,5]
        directions = ""
        if self.check_up() in rooms:
            directions += "UP "
        if self.check_down() in rooms:
            directions += "DOWN "
        if self.check_left() in rooms:
            directions += "LEFT "
        if self.check_right() in rooms:
            directions += "RIGHT "
        return directions.split(' ')

    def check_up(self):
        return self.map.up(self.map.fullMap, self.position[0], self.position[1])
    def check_down(self):
        return self.map.down(self.map.fullMap, self.position[0], self.position[1])
    def check_left(self):
        return self.map.left(self.map.fullMap, self.position[0], self.position[1])
    def check_right(self):
        return self.map.right(self.map.fullMap, self.position[0], self.position[1])

    

