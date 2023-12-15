import random
#from pandas import DataFrame
import copy
import yaml
import pprint
from typing import TypeAlias, NamedTuple
import MapTile
import math
import networkx as nx

Node: TypeAlias = MapTile.MapTile

rooms = {
    #"Campfire":-5,
    #"LootRoom":1,
    #"EmptyCavePath":0,
    #"SpiderRoom":3,
    #"GoblinRoom":2,
    #"SkeletonRoom":4,
    #"ImpRoom":1,
    #"GiantRoom":15,
}

items = [
    #"Dagger", "Sword","Spear", "Shield", "BreastPlate", "Boots"
]

roomSign={
    "StartRoom":1,
    "EndRoom":2,
    "EmptyCavePath":5,
    "EnemyRoom":6,
    "Campfire":6,
    "LootRoom":6
}

EnemyRooms=["GoblinRoom", "SpiderRoom", "SkeletonRoom", "ImpRoom", "GiantRoom"]

campfire = True #should only allow one campfire per map
#validRooms=[3,2,1] #the valid rooms, used in checks

class Mappa:
    def __init__(self, savedGame, loadout=None):
        global rooms
        global items
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        rooms = config['rooms']
        items = config['items']
        self._world = {}
        self.start = (0,0)
        self.end = (0,0)
        self.fullMap = []
        self.rows = config['map_size']['rows']
        self.cols = config['map_size']['columns']
        self.mana = config['mana']
        if not savedGame:
            for i in range(self.rows):
                for j in range(self.cols):
                    self._world[(i,j)] = None
            #print("setting start and end")
            self.setStart()#set start and end rooms at random
            #print("starting to create the map")
            self.loadMap()#set some rooms at random up to a weight set in global vars
            #print("Map created, connecting rooms")
            self.connectRooms()#connect the rooms and get a map with the places that will be corridors(empty rooms)
            #print("Placing corridors in the world")
            #self.placeCorridors(self.fullMap)#place the corridors
            #print("Printing the map")
            #self.printWorld()#print the map
        else:
            self.fromFile(loadout)
    
    def fromFile(self,loadout):
        self.fullMap = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                key = "{}_{}".format(i,j)
                if key in loadout.keys():
                    #print(loadout[key])
                    name = loadout[key]['name']
                    if name == "LootRoom":
                        val=6
                        item = getattr(__import__('item'), loadout[key]['item'])()
                        self._world[(i,j)] = getattr(__import__('MapTile'), loadout[key]['name'])(i,j,item)
                        self._world[(i,j)].present = loadout[key]['info']
                    elif name in EnemyRooms:
                        val = 6
                        self._world[(i,j)] = getattr(__import__('MapTile'), loadout[key]['name'])(i,j)
                        self._world[(i,j)].enemy.hp = loadout[key]['info']
                    else:
                        val = roomSign[loadout[key]['name']]
                        self._world[(i,j)] = getattr(__import__('MapTile'), loadout[key]['name'])(i,j)
                        if loadout[key]['name'] == "StartRoom":
                            self.start=(i,j)
                        elif loadout[key]['name'] == "Campfire":
                            self._world[(i,j)].used = loadout[key]['info']
                    if loadout[key]['name'] == "EnemyRoom":
                        self._world[(i,j)].enemy.hp = int(loadout[key]['info'])
                else:
                    val = 0
                    self._world[(i,j)] = None
                self.fullMap[i][j] = val

    def setStart(self):#set the start and finish locations at random
        x = random.randint(0,self.rows-1)
        y = random.randint(0,self.cols-1)
        self.start = (x,y)
        self._world[(x,y)] = getattr(__import__('MapTile'), "StartRoom")(x,y)
        x = random.randint(0,self.rows-1)
        y = random.randint(0,self.cols-1)
        if (x,y) != self.start:
            self._world[(x,y)] = getattr(__import__('MapTile'), "EndRoom")(x,y)
            self.end = (x,y)
    #add the event rooms to the map
    def loadMap(self):
        global campfire
        while self.mana>0:
            #choose a random number to select a random room
            rand = random.randint(0,rooms.__len__()-1)
            #check to make sure only 1 campfire is allowed
            if list(rooms.keys())[rand]=="Campfire" and campfire:
                campfire = False
            else:
                if list(rooms.keys())[rand]=="Campfire" and not campfire:
                    continue
            #if the cost of the selected room is over mana, skip iteration, selecting another room
            if list(rooms.values())[rand] > self.mana:
                continue
            #decrease mana available
            self.mana -= list(rooms.values())[rand]
            #choose a location for the room
            x = random.randint(0,self.rows-1)
            y = random.randint(0,self.cols-1)
            #check that the location is empty, otherwise skip iteration
            if self._world[(x,y)] is not None:
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
        self.fullMap = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.placeCorridors()
        nodes = []
        for node in self._world.values():
            if not isinstance(node, MapTile.Wall) and not isinstance(node, MapTile.EndRoom) and not isinstance(node, MapTile.StartRoom):
                nodes.append(node)
        nodes.insert(0, self._world[self.start])
        nodes.append(self._world[self.end])
        #print("Nodes: ",nodes)
        path = []
        for i in range(nodes.__len__()-1):
            path += solve(self, nodes[i], nodes[i+1])
        #print("Path: ",path)
        for cave in path:
            if isinstance(self._world[(cave.x, cave.y)], MapTile.Wall) or isinstance(self._world[(cave.x, cave.y)], MapTile.EmptyCavePath):
                self._world[(cave.x, cave.y)] = getattr(__import__('MapTile'), "EmptyCavePath")(cave.x,cave.y)
                self.fullMap[cave.x][cave.y] = 5
            elif isinstance(self._world[(cave.x, cave.y)], MapTile.StartRoom):
                self.fullMap[cave.x][cave.y] = 1
            elif isinstance(self._world[(cave.x, cave.y)], MapTile.EndRoom):
                self.fullMap[cave.x][cave.y] = 2
            else:
                #print(self._world[(cave.x, cave.y)])
                self.fullMap[cave.x][cave.y] = 6
        

    #method to place the corridors added to connect the rooms to the world
    def placeCorridors(self):
        for x in range(self.rows):#mark connected corridors
            for y in range(self.cols):
                if self._world[(x,y)]==None:
                    self._world[(x,y)] = getattr(__import__('MapTile'), "Wall")(x,y)
    
    def up(self,map,x,y): #return the value on the map from a particular direction, -1 if it's out of bounds
        if x-1>=0:
            return map[x-1][y]
        return -1
    def down(self,map,x,y):
        if x+1<=self.rows-1:
            return map[x+1][y]
        return -1
    def left(self,map,x,y):
        if y-1>=0:
            return map[x][y-1]
        return -1
    def right(self,map,x,y):
        if y+1<=self.cols-1:
            return map[x][y+1]
        return -1

    #method to print the map on console
    def printWorld(self):
        #print("Full map")
        #print(DataFrame(fullMap))
        printMap=[["#" for _ in range(self.cols)] for _ in range(self.rows)]
        #print(self.fullMap)
        for x in range(self.rows):#mark reached rooms
            for y in range(self.cols):
                #print(f"x: {x}, y: {y}")
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
        stringMap = ""
        for i in range(self.rows):
            for j in range(self.cols):
                stringMap+=printMap[i][j]+" "
            stringMap+="\n"
        return stringMap
        
    #method to check for disconnected rooms
    def saveLayout(self):
        data = {}
        for room in self._world.values():
            if room is not None:
                info = room.get_data()
                #print(info)
                data["{}_{}".format(info[0]['x'], info[0]['y'])] = info[1]
        return data
        
class Edge(NamedTuple):
    node1 : Node
    node2 : Node
    @property
    def distance(self)->float:
        return math.dist((self.node1.x, self.node1.y),(self.node2.x, self.node2.y))
    def weight(self, bonus=0)->float:
        if self.node2 is None:
            return self.distance
        else:
            return self.distance-bonus
    
    @property
    def flip(self)->"Edge":
        return Edge(self.node2, self.node1)
        
def get_nodes(map: Mappa)->set[Node]:
    nodes: set[Node]= set()
    for tile in map._world.values():
        nodes.add(tile)
    #print("Nodes : ", nodes)
    return nodes

def get_edges(map: Mappa, nodes: set[Node])->set[Edge]:
    edges: set[Edge] = set()
    for source_node in nodes:
        node = source_node
        #print("Node: ", node)
        if node.x+1<map.cols:
            node = map._world[(node.x+1,node.y)]
            if node in nodes:
                edges.add(Edge(source_node, node))
        elif node.y+1<map.rows:
            node = map._world[(node.x,node.y+1)]
            if node in nodes:
                edges.add(Edge(source_node, node))
    #print("Returning edges: ", edges)
    return edges

def make_graph(map: Mappa)->nx.Graph:
    return nx.Graph(
        (edge.node1, edge.node2, {"weight": edge.weight()})
        for edge in get_edges(map, get_nodes(map))
    )

def solve(map: Mappa, source: Node, target: Node)->list[MapTile.MapTile] | None:
    try:
        return nx.shortest_path(
            make_graph(map),
            source = source,
            target = target,
            weight = "weight"
        )
    except nx.NetworkXException:
        print(nx.NetworkXException.__str__())
        return None