#dictionary with the options usable in combat, the value is used for logic
choices = {
    "ATTACK":1,
    "DEFEND":2,
    "HEAL":3,
    "CHARGE":4,
    "RUN":5
}

class Encounter:
    def __init__(self, char, npc) -> None:
        self.character = char
        self.npc = npc
    
    def fight(self):
        fought = False #check if the user has fought this enemy or it was already dead to not heal each time
        charDef = 0 #additional defence in case the user defends
        charCharge = 1 #additional damage multiplier in case of charge
        #while both parties are alive, let em fight
        while self.character.is_alive() and self.npc.is_alive():
            #mark that the player really fought
            fought = True
            #print("\033c", end='')
            #Character turn
            choice = ""
            #loop till a valid choice is made
            while not choice.upper() in choices.keys():
                #print("\033c", end='')
                print("HP: {}    Enemy HP: {}".format(self.character.hp, self.npc.hp))
                print("What will you do?")
                choice = input("Attack - Defend - Heal - Charge - Run")
            #check which action was taken and apply it
            action = 0
            if choice.upper() in choices.keys():
                action = choices[choice.upper()]
                print("action: ",action)
            if action == 1:
                self.npc.attacked(self.character.attack()*charCharge)
                charCharge = 1
            if action == 2:
                charDef = 5
            if action == 3:
                self.character.heal(self.character.maxhp/5)
            if action == 4:
                charCharge = 3
            if action == 5:
                print("You escape the encounter but take a last blow to your back")
                self.character.attacked(self.npc.attack() - charDef)
                break
            #Enemy turn simple attack
            self.character.attacked(self.npc.attack() - charDef)
            #reset the defend buff
            charDef = 0
        if not self.character.is_alive():
            print("You died!")
        if not self.npc.is_alive() and fought:
            print("You made it!")
            self.character.heal(self.character.maxhp/10)