class Character:
    def __init__(self, name,maxhp, hp, defence, damage, gold=0):
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
        print("Ahh, you are healing by ", amount)
        print("Total HP: ", self.hp)
        self.hp+=amount
        if self.hp>self.maxhp:
            self.hp = self.maxhp

    def pickup(self, item):
        print(item)
        if not item in self.items:
            self.items.append(item)
            if item.damage!=0:
                res=input("You already have a weapon, change your current one? (Y/N)")
                if res.upper()=='Y':
                    self.damage=item.damage
                    print("Weapon changed, current damage: ",self.damage)
            if item.defence!=0:
                print("Defence increased by: {}".format(item.defence))
                self.defence+=item.defence
        else:
            print("You already have that item, you scrap it for its value")
            self.gold +=item.value
            print("Total gold : {}. Maybe you can eat it in a pinch".format(self.gold))

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
            print("{} took {} damage".format(self.name, taken))
        else:
            print("The blow glances off your armour")

    def attack(self):
        return self.damage
