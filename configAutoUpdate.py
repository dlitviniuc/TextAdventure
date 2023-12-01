import yaml
import ast
import tkinter as tk
#initializing tk to allow the initializzation of ImageTk.PhotoImage
root = tk.Tk()

with open('config.yaml', "r") as f:
    data = yaml.safe_load(f)

with open('./MapTile.py', "r") as mt:
    p = ast.parse(mt.read())
    mapTiles = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
mapTiles.pop(0)
print(mapTiles)

with open('./item.py', "r") as mt:
    p = ast.parse(mt.read())
    items = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
items.pop(0)
print(items)

rooms = {}
notValidRooms = ["EnemyRoom", "EmptyCavePath", "StartRoom", "EndRoom"]
for name in mapTiles:
    if name in notValidRooms:
        continue
    tile = getattr(__import__('MapTile'), name)(0, 0)
    rooms[name] = tile.cost

print(rooms)

data["rooms"] = rooms
data["items"] = items

with open('config.yaml', "w") as f:
    yaml.dump(data,f)