from PIL import ImageTk, Image

class Character:
    def __init__(self, name,maxhp, hp, defence, damage, gold=0):
        self.image = ImageTk.PhotoImage(Image.open("./images/adventurer.jpg").resize((200,250)))
        self.name = name
        self.maxhp = maxhp
        self.hp = hp
        self.defence = defence
        self.damage = damage
        self.gold = gold
        self.items = []
    
    def is_alive(self):
        return self.hp>0

    def heal(self, amount):
        self.hp+=amount
        if self.hp>self.maxhp:
            self.hp = self.maxhp
        return "Ahh, you are healing by {}\n".format(amount)

    def pickup(self, item):
        answer = ""
        #print(item)
        if not item in self.items:
            self.items.append(item)
            if item.damage!=0:
                self.damage = item.damage
                answer += "Weapon changed, current damage: {}\n".format(self.damage)
            if item.defence!=0:
                answer+="Defence increased by: {}\n".format(item.defence)
                self.defence+=item.defence
        else:
            answer += "You already have that item, you scrap it for its value\n"
            self.gold +=item.value
            return answer+"\n"+"Total gold : {}. Maybe you can eat it in a pinch\n".format(self.gold)

    def drop(self, item):
        self.items.remove(item)
        if item.damage!=0:
            self.damage-=item.damage
        if item.defence!=0:
            self.defence-=item.defence
    
    def attacked(self, dmg):
        if self.defence<dmg:
            taken = (dmg - self.defence)
            self.hp -= taken
            return "{} took {} damage\n".format(self.name, taken)
        else:
            return "The blow glances off your armour\n"

    def attack(self):
        return self.damage
    
    def info(self):
        return {
            "name":self.name,
            "maxhp":self.maxhp,
            "hp":self.hp,
            "defence":self.defence,
            "damage":self.damage,
            "gold":self.gold
        }