import tkinter as tk
from tkinter import *
from typing import Any
from navigation import Navigation
import MapTile
from combat import Encounter
import yaml

#variable to check if the game is still going
endGame = False
#customization variables
customization = {}
#save or not on closing game
save = False

class Window(Frame):
    #initializing the window
    def __init__(self, root):
        self.root = root
        tk.Frame.__init__(self, height=500, width=500, name="mainFrame")
        self.master.title("Adventure")
        self.nav = Navigation()
        self.setup()
        self.dialogChoice = tk.IntVar(value=-1)
        self.directionChoice = tk.IntVar(value=-1)
        self.combatChoice = tk.IntVar(value=-1)

    #setting up the interface pieces
    def setup(self):
        self.configure(bg=customization["mainBackgroundColor"])
        self.setMap()
        self.setDirections()
        self.setDialogs()
        self.setText()
        
    #setting up the direction buttons
    def setDirections(self):
        directions = Frame(self, name="directions")
        up = Button(directions, text="^",name="up", command=lambda: self.directionChoice.set(1), width=3, height=2)
        down = Button(directions, text="v", name="down", command=lambda: self.directionChoice.set(2), width=3, height=2)
        left = Button(directions, text="<", name="left", command=lambda: self.directionChoice.set(3), width=3, height=2)
        right = Button(directions, text=">", name="right", command=lambda: self.directionChoice.set(4), width=3, height=2)
        up.configure(activebackground=customization['activeButtonColor'], background=customization['inactiveButtonColor'])
        down.configure(activebackground=customization['activeButtonColor'], background=customization['inactiveButtonColor'])
        left.configure(activebackground=customization['activeButtonColor'], background=customization['inactiveButtonColor'])
        right.configure(activebackground=customization['activeButtonColor'], background=customization['inactiveButtonColor'])
        directions.configure(bg=customization["mainBackgroundColor"])
        up.grid(column=1,row=0)
        down.grid(column=1,row=2)
        left.grid(column=0,row=1)
        right.grid(column=2,row=1)
        directions.grid(column=0,row=1)
    #setting up the dialog buttons
    def setDialogs(self):
        dialogs = Frame(self, name="dialogs")
        yes = Button(dialogs, text="Yes", name="yes", command=lambda: self.dialogChoice.set(1), width=4, height=2)
        no = Button(dialogs, text="No", name="no", command=lambda: self.dialogChoice.set(2), width=4, height=2)
        yes.grid(column=0, row=0)
        no.grid(column=1,row=0)
        no.configure(background=customization['activeButtonColor'])
        yes.configure(background=customization['activeButtonColor'])
        dialogs.grid(column=0,row=2)
        dialogs.configure(background=customization["mainBackgroundColor"])
    #setting up the map and character stats
    def setMap(self):
        map = tk.Text(self, height=self.nav.map.rows, width=self.nav.map.cols*2, name="map", font=("Arial", 12))
        map.grid(column=0, row=0)
        mapText = self.nav.map.printWorld()
        map.delete('1.0',END)
        map.insert('end',mapText)
        map.configure(background=customization['secBackgroundColor'], state="disabled")
        self.combattant(self.nav.char.hp, self.nav.char.damage, self.nav.char.defence, [0,3])
    #setting up the main text frame
    def setText(self, dialog=""):
        text = tk.Text(self,height=15, width=60, name="mainText", font=("Arial", 15))
        text.grid(column=1, row=0, columnspan=3, rowspan=3)
        text.configure(background=customization["mainBackgroundColor"])
        text.delete('1.0',END)
        text.insert('end',dialog)
    #setting up the combat stats
    def combat(self):
        enemy = self.nav.map._world[self.nav.position].enemy
        self.combattant(enemy.hp, enemy.damage, enemy.defence, [2,3])
        commands = Frame(self, name="commands")
        attack = Button(commands, text="Attack", name="attack", command=lambda: self.combatChoice.set(1))
        defend = Button(commands, text="Defend", name="defend", command=lambda: self.combatChoice.set(2))
        charge = Button(commands, text="Charge", name="charge", command=lambda: self.combatChoice.set(3))
        run = Button(commands, text="Run", name="run", command=lambda: self.combatChoice.set(4))
        attack.configure(background=customization["mainBackgroundColor"])
        defend.configure(background=customization["mainBackgroundColor"])
        charge.configure(background=customization["mainBackgroundColor"])
        run.configure(background=customization["mainBackgroundColor"])
        commands.configure(background=customization["mainBackgroundColor"])
        attack.grid(column=0, row=0)
        defend.grid(column=1, row=0)
        charge.grid(column=2, row=0)
        run.grid(column=3, row=0)
        commands.grid(column=1, row=3, rowspan=1)
        combatLogs = Text(commands, height=10, width=40, name="logs", font=("Arial", 14))
        combatLogs.grid(column=0, row=4, columnspan=4)
        combatLogs.configure(background=customization["mainBackgroundColor"])
    #creating a combattant [3,3] indicates an enemy as it will be on the right side
    def combattant(self, hp, damage, defence, position):
        if position == [2,3]:
            stats = Frame(self, name="enemystats")
            img = self.nav.map._world[self.nav.position].enemy.image
        else:
            stats = Frame(self, name="charstats")
            img = self.nav.char.image
        panel = tk.Label(stats, image=img)
        panel.grid(column=0, row=2, columnspan=3)
        hplabel = Label(stats, text="HP")
        dmglabel = Label(stats, text="DMG")
        deflabel = Label(stats, text="DEF")
        hplabel.grid(column=0, row=0)
        hplabel.configure( background=customization['secBackgroundColor'])
        dmglabel.grid(column=1,row=0)
        dmglabel.configure( background=customization['secBackgroundColor'])
        deflabel.grid(column=2, row=0)
        deflabel.configure( background=customization['secBackgroundColor'])
        hitp = Text(stats, width=3, height=1, name="hp")
        dmg = Text(stats, width=3, height=1, name="dmg")
        dfc = Text(stats, width=3, height=1, name="dfc")
        hitp.grid(column=0, row=1)
        dmg.grid(column=1,row=1)
        dfc.grid(column=2,row=1)
        hitp.delete('1.0',END)
        dmg.delete('1.0',END)
        dfc.delete('1.0',END)
        hitp.insert('end', str(hp))
        dmg.insert('end', str(damage))
        dfc.insert('end', str(defence))
        hitp.configure(state="disabled", background=customization['secBackgroundColor'])
        dmg.configure(state="disabled", background=customization['secBackgroundColor'])
        dfc.configure(state="disabled", background=customization['secBackgroundColor'])
        stats.grid(column=position[0], row=position[1],rowspan=6)
        stats.configure( background=customization['secBackgroundColor'])
    #main loop of the game, using this method with manual update instead of mainloop
    def loop(self):
        global endGame
        #check if fight is still going
        fighting = False
        #check if an event is going on
        event = False
        #last position, used to check if player moved
        lastpos = (-1,-1)
        #bool variable to check if player is choosing to stay or leave in an ending room
        ending = False
        #placeholder variable to contain a possible encounter
        encounter = None
        #starting up the window to show it's shown
        self.update()
        #while the game is going
        try:
            while not endGame and self.root.winfo_ismapped():
                #checking if the window was closed to stop the loop
                try:
                    endGame = endGame or not self.winfo_exists()
                except:
                    endGame = True
                #check if player moved
                if self.directionChoice.get()!=-1:
                    self.nav.step(self.directionChoice.get())
                    self.directionChoice.set(-1)
                #updating ui
                self.update()
                #checking if a step was taken
                if(lastpos!=self.nav.position):
                    lastpos = self.nav.position
                    #getting intro text from new room
                    #print(self.nav.map.printWorld())
                    answer = self.nav.map._world[self.nav.position].intro_text()
                    #putting intro text in the maintext widget
                    self.nametowidget("mainText").insert('end', answer)
                    #check if the tile is an encounter
                    if isinstance(self.nav.map._world[self.nav.position], MapTile.EnemyRoom):
                        #setup combat widgets
                        self.combat()
                        encounter = Encounter(self.nav.char, self.nav.map._world[self.nav.position].enemy)
                        if encounter.npc.is_alive():
                            fighting = True
                    #check if it's a campfire
                    elif isinstance(self.nav.map._world[self.nav.position], MapTile.Campfire) and self.nav.map._world[self.nav.position].valid():
                        self.nav.map._world[self.nav.position].rest()
                        event = True
                    #check if it's a loot room
                    elif isinstance(self.nav.map._world[self.nav.position], MapTile.LootRoom) and self.nav.map._world[self.nav.position].valid():
                        event = True
                    #check if it's the exit room
                    elif isinstance(self.nav.map._world[self.nav.position], MapTile.EndRoom):
                        ending = True
                    else:
                        event = False
                        fighting = False
                #event clause
                if event:
                    self.disableMovement()
                    #if a choice was made
                    if self.dialogChoice.get()!=-1:
                        #yes case 
                        if self.dialogChoice.get()==1:
                            answer = self.nav.map._world[self.nav.position].choice(self.nav.char,True)
                        #no case
                        elif self.dialogChoice.get()==2:
                            answer = self.nav.map._world[self.nav.position].choice(self.nav.char,False)
                        self.nametowidget("mainText").insert('end', answer)
                        self.dialogChoice.set(-1)
                        self.updateStats(1, self.nav.char)
                        event = False
                #fighting clause
                elif fighting:
                    self.disableMovement()
                    if self.combatChoice.get()!=-1:
                        answer = encounter.fight(self.combatChoice.get())
                        self.nametowidget("commands").nametowidget("logs").insert('end', answer)
                        fighting=encounter.fighting
                        #if the player ran
                        if self.combatChoice.get()==4:
                            fighting=False
                        self.combatChoice.set(-1)
                        self.nametowidget("commands").nametowidget("logs").yview_moveto(1)
                        self.updateStats(1, encounter.character)
                        self.updateStats(2, encounter.npc)
                #ending clause
                elif ending:
                    self.disableMovement()
                    if self.dialogChoice.get()!=-1:
                        #yes case 
                        if self.dialogChoice.get()==1:
                            answer = self.nav.map._world[self.nav.position].choice(self.nav.char,True)
                            endGame=True
                            ending=False
                        #no case
                        elif self.dialogChoice.get()==2:
                            answer = self.nav.map._world[self.nav.position].choice(self.nav.char,False)
                            ending=False
                        self.nametowidget("mainText").insert('end', answer)
                        self.dialogChoice.set(-1)
                #if no active event, check which way the player can move
                elif not event and not fighting and not ending:
                    self.checkDirections()
                self.autoScroll()
        except Exception as e:
            print("exception: ", e)
    
    #disable movement buttons
    def disableMovement(self):
        frame = self.nametowidget("directions")
        for element in frame.winfo_children():
            element.configure(state="disable")
    #enable movement buttons not used as it was replaced by checkdirections
    def enableMovement(self):
        frame = self.nametowidget("directions")
        for element in frame.winfo_children():
            element.configure(state="active")
    #check the available directions in which the player can move and enable correct buttons
    def checkDirections(self):
        directions = self.nav.showDirections()
        frame = self.nametowidget("directions")
        for element in frame.winfo_children():
            if element.winfo_name().upper() in directions:
                element.configure(state="active")
            else:
                element.configure(state="disable")
    #update the stats of the character or the npc player=1 means character
    def updateStats(self, player, character):
        if player==1:
            stats = self.nametowidget('charstats')
        else:
            stats = self.nametowidget('enemystats')
        hp = character.hp
        damage = character.damage
        defence = character.defence
        hitp = stats.nametowidget('hp')
        dmg = stats.nametowidget('dmg')
        dfc = stats.nametowidget('dfc')
        hitp.configure(state="normal")
        dmg.configure(state="normal")
        dfc.configure(state="normal")
        hitp.delete('1.0',END)
        dmg.delete('1.0',END)
        dfc.delete('1.0',END)
        hitp.insert('end', str(hp))
        dmg.insert('end', str(damage))
        dfc.insert('end', str(defence))
        hitp.configure(state="disabled")
        dmg.configure(state="disabled")
        dfc.configure(state="disabled")
    #autoscrolling function for main text frame
    def autoScroll(self):
        self.nametowidget("mainText").yview_moveto(1)
    
    def save(self):
        #if game ended or user chose to not save
        if endGame:
            return False
        #get map layout
        mapInfo = main.nav.map.saveLayout()
        #get character info
        charinfo= main.nav.char.info()
        postition = {"x":main.nav.position[0], "y":main.nav.position[1]}
        #put together in a dict to dump in a yaml file
        dump = {
            "map":mapInfo,
            "char":charinfo,
            "position":postition
        }
        #dump the dict in the file
        with open('savefile.yaml', "w") as f:
            yaml.safe_dump(dump, f)
        #updating config file to mark if a game was saved and relative savefile
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        config['save'] = save
        config['savefile'] = 'savefile.yaml'
        with open('config.yaml', "w") as f:
            yaml.safe_dump(config, f)
        return True
        

class ClosingWindow:
    def __init__(self, parent) -> None:
        self.root = parent
        self.top = tk.Toplevel(self.root)
        frame = tk.Frame(self.top)
        text = tk.Label(frame, text="Would you like to save your game?")
        saveButton = tk.Button(frame, text="Save", command=lambda: self.close(True))
        noSaveButton = tk.Button(frame, text="Don't Save", command=lambda: self.close(False))
        text.pack()
        saveButton.pack()
        noSaveButton.pack()
        frame.pack(fill='both', expand=True)

    def close(self, choice):
        global save
        save = choice
        self.top.destroy()

def closing():
    global save
    saveDialog = ClosingWindow(root)
    root.wait_window(saveDialog.top)
    print("User chose to save? ",save)
    main.save()
    root.destroy()

def gameEnded():
    with open('config.yaml', "r") as f:
        data = yaml.safe_load(f)
    data['save']=False
    with open('config.yaml', "w") as f:
        yaml.safe_dump(data, f)

if __name__=="__main__":
    with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
    customization = config['customization']
    root = tk.Tk()
    root.geometry("{}x{}".format(config['windowSize']['width'],config['windowSize']['height']))
    root.protocol('WM_DELETE_WINDOW', closing)
    main = Window(root)
    main.pack(side = "top", fill="both", expand=True)
    main.loop()
    if endGame:
        gameEnded()



