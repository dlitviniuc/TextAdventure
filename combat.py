import yaml

charDef = 0 #additional defence in case the user defends
charCharge = 1 #additional damage multiplier in case of charge

class Encounter:
    def __init__(self, char, npc) -> None:
        self.character = char
        self.npc = npc
        self.fighting = False
    
    def fight(self, action):
        self.fighting=True
        #fought = False #check if the user has fought this enemy or it was already dead to not heal each time
        global charCharge
        global charDef
        #while both parties are alive, let em fight
        #while self.character.is_alive() and self.npc.is_alive():
        #mark that the player really fought
        if not self.character.is_alive():
            self.fighting=False
            return "You died!\n"
        if not self.npc.is_alive():
            self.fighting=False
            #self.character.heal(self.character.maxhp/10)
            return "You made it!\n"
        #Character turn
        #loop till a valid choice is made
        #check which action was taken and apply it
        answer = ""
        if action == 1:
            answer = self.npc.attacked(self.character.attack()*charCharge)
            charCharge = 1
            if not self.npc.is_alive():
                self.fighting=False
                return "You made it!\n"
        if action == 2:
            charDef = 5
            answer= "You are defending"
        if action == 5:
            answer= self.character.heal(self.character.maxhp/5)
        if action == 3:
            charCharge = 3
            answer= "You are charging an attack"
        if action == 4:
            self.character.attacked(self.npc.attack() - charDef)
            answer = "You escape the encounter but take a last blow to your back"
        answer+="\n"
        #Enemy turn simple attack
        answer += self.character.attacked(self.npc.attack() - charDef)
        #reset the defend buff
        charDef = 0
        return answer
        