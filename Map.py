import random
from pandas import DataFrame
import copy

rows = 5 #can be changed to make the map bigger
cols = 5 #can be changed to make the map bigger
mana = 20 #can be changed to allow more rooms in the map

rooms = {
    "Campfire":-5,
    "LootRoom":1,
    #"EmptyCavePath":0,
    "SpiderRoom":3,
    "GoblinRoom":2,
    "SkeletonRoom":4,
    "ImpRoom":1,
    "GiantRoom":15,
}

items = [
    "Dagger", "Sword","Spear", "Shield", "BreastPlate", "Boots"
]

campfire = True #should only allow one campfire per map
validRooms=[3,2,1] #the valid rooms, used in checks

class Mappa:
    def __init__(self):
        self._world = {}
        self.start = (0,0)
        self.end = (0,0)
        self.fullMap = []
        for i in range(rows):
            for j in range(cols):
                self._world[(i,j)] = None
        #print("setting start and end")
        self.setStart()#set start and end rooms at random
        #print("starting to create the map")
        self.loadMap()#set some rooms at random up to a weight set in global vars
        #print("Map created, connecting rooms")
        self.fullMap=self.connectRooms()#connect the rooms and get a map with the places that will be corridors(empty rooms)
        #print("Placing corridors in the world")
        self.placeCorridors(self.fullMap)#place the corridors
        #print("Printing the map")
        self.printWorld()#print the map
    
    def setStart(self):#set the start and finish locations at random
        x = random.randint(0,rows-1)
        y = random.randint(0,cols-1)
        self.start = (x,y)
        self._world[(x,y)] = getattr(__import__('MapTile'), "StartRoom")(x,y)
        x = random.randint(0,rows-1)
        y = random.randint(0,cols-1)
        if (x,y) != self.start:
            self._world[(x,y)] = getattr(__import__('MapTile'), "EndRoom")(x,y)
            self.end = (x,y)
    #add the event rooms to the map
    def loadMap(self):
        global mana
        global campfire
        global rooms
        while mana>0:
            #choose a random number to select a random room
            rand = random.randint(0,6)
            #check to make sure only 1 campfire is allowed
            if list(rooms.keys())[rand]=="Campfire" and campfire:
                campfire = False
            else:
                if list(rooms.keys())[rand]=="Campfire" and not campfire:
                    continue
            #if the cost of the selected room is over mana, skip iteration, selecting another room
            if list(rooms.values())[rand] > mana:
                continue
            #decrease mana available
            mana -= list(rooms.values())[rand]
            #choose a location for the room
            x = random.randint(0,rows-1)
            y = random.randint(0,cols-1)
            #check that the location is empty, otherwise skip iteration
            if self._world[(x,y)]!=None:
                continue
            #if a loot room was selected, choose a random item to place inside and place the room
            if list(rooms.keys())[rand]=="LootRoom":
                randomItem = random.randint(0, items.__len__()-1)
                item = getattr(__import__('item'), items[randomItem])()
                self._world[(x,y)] = getattr(__import__('MapTile'), list(rooms.keys())[rand])(x,y, item)
            #if the selected room is not loot place it directly
            else:
                self._world[(x,y)] = getattr(__import__('MapTile'), list(rooms.keys())[rand])(x,y)
    #method to connect the rooms
    def connectRooms(self):
        map = [[0 for _ in range(cols)] for _ in range(rows)] #initializing matrix to use for connecting the rooms
        #if in the world there's a room at location pos, place 3 on the map to mark it
        for pos, room in self._world.items():
            if room != None:
                map[pos[0]][pos[1]] = 3 #marking rooms
        #save the map in the class for future use
        self.fullMap=map
        #print(map)
        map[self.start[0]][self.start[1]] = 1 #marking start
        map[self.end[0]][self.end[1]]=2 #marking finish
        #for each room, start expanding corridors in all cardinal directions
        for pos, room in self._world.items():
            if room != None:
                self.expandSearch(map, pos[0],pos[1])
        #check for connected corridors
        self.corridorsConnected(map)
        #check for rooms reached idk if it's still needed but meh
        self.roomsReached(map)
        #limit length of the corridors, increasing at each iteration till all rooms are connected
        limit = 1
        #check if any room is disconnected from the rest by counting the rooms connected to any of them and seeing if that number is less than the total number of rooms
        expand = self.disconnected(map)
        #print("expand? ", expand)
        loops = 0
        while expand and loops<10:
            loops+=1
            print("expansion")
            for x in range(rows):#mark connected corridors
                for y in range(cols):
                    if map[x][y] in [4,5]:
                        #lenghten the corridors till limit, it's by 1 each time this iteration loops
                        self.expandCorridors(map,x,y,limit)
            #increase max length of each corridor
            limit+=1
            #recheck for connected corridors
            self.corridorsConnected(map)
            #check if an additional expansion is needed
            expand = self.disconnected(map)
        #return the map created
        return map
    #method to place the corridors added to connect the rooms to the world
    def placeCorridors(self,map):
        for x in range(rows):#mark connected corridors
            for y in range(cols):
                if map[x][y]==5:
                    self._world[(x,y)] = getattr(__import__('MapTile'), "EmptyCavePath")(x,y)
                
    def expandCorridors(self,map,x,y,limit):#expand a corridor's length to reach an intersection
        valid = [4,5,0]
        if self.up(map,x,y) in valid:
            self.lengthenCorridor(map,x-limit,y,-limit,0)
        if self.down(map,x,y) in valid:
            self.lengthenCorridor(map,x+limit,y,limit,0)
        if self.left(map,x,y) in valid:
            self.lengthenCorridor(map,x,y-limit,0,-limit)
        if self.right(map,x,y) in valid:
            self.lengthenCorridor(map,x,y+limit,0,limit)

    def lengthenCorridor(self,map,x,y,i,j):#mark the next cell in line as a corridor if it's possible
        if x+i<rows and x+i>=0 and y+j<cols and y+j>=0:
            if map[x+i][y+j] == 0:
                map[x+i][y+j] = 4

    def expandSearch(self, map, x, y): #on a cell, add corridors to all possible sides
        if self.up(map,x,y)==0:
            map[x-1][y]=4
        if self.down(map,x,y)==0:
            map[x+1][y]=4
        if self.left(map,x,y)==0:
            map[x][y-1]=4
        if self.right(map,x,y)==0:
            map[x][y+1]=4
    
    def up(self,map,x,y): #return the value on the map from a particular direction, -1 if it's out of bounds
        if x-1>=0:
            return map[x-1][y]
        else:
            return -1
    def down(self,map,x,y):
        if x+1<=rows-1:
            return map[x+1][y]
        else:
            return -1
    def left(self,map,x,y):
        if y-1>=0:
            return map[x][y-1]
        else:
            return -1
    def right(self,map,x,y):
        if y+1<=cols-1:
            return map[x][y+1]
        else:
            return -1

    def corridorsConnected(self, map):#mark corridors that connect to another one with 5 on the map
        connected = [5,6,3,4,1,2]
        for x in range(rows):#mark connected corridors
            for y in range(cols):
                matches = 0
                if map[x][y]==4:
                    if self.up(map,x,y) in connected:
                        if self.up(map,x,y) == 4:
                            map[x-1][y]=5
                        matches +=1
                    if self.down(map,x,y) in connected:
                        if self.down(map,x,y) == 4:
                            map[x+1][y]=5
                        matches +=1
                    if self.left(map,x,y) in connected:
                        if self.left(map,x,y) == 4:
                            map[x][y-1]=5
                        matches +=1
                    if self.right(map,x,y) in connected:
                        if self.right(map,x,y) == 4:
                            map[x][y+1]=5
                        matches +=1
                    if matches > 1:
                        map[x][y]=5

    def roomsReached(self, map):#mark rooms(start and end too) that are connected by connected corridors with 6 on the map(to change numbers)
        connected = [1,2,5,6]
        for x in range(rows):#mark reached rooms
            for y in range(cols):
                if map[x][y] == 3:
                    if self.up(map,x,y) in connected:
                        map[x][y]=6
                    if self.down(map,x,y) in connected:
                        map[x][y]=6
                    if self.left(map,x,y) in connected:
                        map[x][y]=6
                    if self.right(map,x,y) in connected:
                        map[x][y]=6
    #method to print the map on console
    def printWorld(self):
        #print("Full map")
        #print(DataFrame(fullMap))
        printMap=[["#" for _ in range(cols)] for _ in range(rows)]
        for x in range(rows):#mark reached rooms
            for y in range(cols):
                if self.fullMap[x][y]==1:
                    printMap[x][y]="S"
                elif self.fullMap[x][y]==2:
                    printMap[x][y]="E"
                elif self.fullMap[x][y]==6:
                    printMap[x][y]="R"
                elif self.fullMap[x][y]==5:
                    printMap[x][y]="="
                elif self.fullMap[x][y]==0:
                    printMap[x][y]="#"
                else:
                    printMap[x][y]="#"
        print(DataFrame(printMap))
    #method to check for disconnected rooms
    def disconnected(self, mat):
        tempmat = copy.deepcopy(mat)
        pos = (0,0)
        rooms = 0
        for i in range(rows):
            for j in range(cols):
                if mat[i][j]>0:
                    rooms+=1
                    pos = (i,j)
        self.findRooms(tempmat, pos[0], pos[1])
        #print(DataFrame(tempmat))
        discRooms =0
        for i in range(rows):
            for j in range(cols):
                if tempmat[i][j]<0:
                    discRooms+=1
        #print("rooms: {} foundRooms: {}".format(rooms, discRooms))
        return rooms>discRooms
    #method to mark connected rooms marking them with -1 (corridors included)
    def findRooms(self, mat, x,y):
        mat[x][y]=-1
        if x-1>=0 :
            if mat[x-1][y]>0:
                self.findRooms(mat,x-1,y)
        if x+1<rows :
            if mat[x+1][y]>0:
                self.findRooms(mat,x+1,y)
        if y-1>=0 :
            if mat[x][y-1]>0:
                self.findRooms(mat,x,y-1)
        if y+1<cols :
            if mat[x][y+1]>0:
                self.findRooms(mat,x,y+1)
        