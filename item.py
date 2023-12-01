class Item():
    def __init__(self, name, description, value, damage, defence):
        self.name = name
        self.description = description
        self.value = value
        self.damage = damage
        self.defence = defence
    
    def __str__(self):
        string = "Name: {}\n=========\nDescription: {}\n=========\nValue: {}\n=========\n".format(self.name, self.description, self.value)
        if self.damage!=0:
            string+="Damage: {}     ".format(self.damage)
        if self.defence!=0:
            string+="Defence: {}".format(self.defence)
        return string
class Dagger(Item):
    def __init__(self):
        super().__init__(name="Dagger", description="A sharp if sligtly chipped knife", value=5, damage=5, defence=0)

class Sword(Item):
    def __init__(self):
        super().__init__(name="Sword", description="A rusted sword, it'll have to do", value=10, damage=6, defence=0)

class Spear(Item):
    def __init__(self):
        super().__init__(name="Spear", description="The weapon of war and mighty warrior, it need some maintenance", value=15, damage=6, defence=1)

class Breastplate(Item):
    def __init__(self):
        super().__init__(name="Breastplate", description="A preety nice breastplate, who knows why it has no rust", value=10, damage=0, defence=2)

class Boots(Item):
    def __init__(self):
        super().__init__(name="Boots", description="A dusty pair of leather boots, surely better than the ones you're wearing", value=5, damage=0, defence=1)

class Shield(Item):
    def __init__(self):
        super().__init__(name="Shield", description="A cutting board with a leather strap attached, it'll still keep a knife from your kidneys", value=3, damage=0, defence=1)
