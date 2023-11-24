from PIL import ImageTk, Image

#generic enemy
class Enemy:
    def __init__(self, name, hp, defence, damage, image):
        self.image = ImageTk.PhotoImage(Image.open("./images"+image).resize((200,250)))
        self.name = name
        self.hp = hp
        self.defence=defence
        self.damage=damage
    
    def is_alive(self):
        return self.hp>0

    def attack(self):
        return self.damage
    
    def attacked(self, dmg):
        if self.defence<dmg:
            taken = (dmg - self.defence)
            self.hp -= taken
            return "{} took {} damage".format(self.name, taken)
        else:
            return "You could not pierce the enemy's armour"

    def __str__(self) -> str:
        return "{}\nHP: {}".format(self.name, self.hp)
        
#Spider
class Spider(Enemy):
    def __init__(self):
        super().__init__(name="Giant Spider", hp=10, defence=1, damage=3, image="/spider.jpg")

#Goblin
class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", hp=15, defence=3, damage=2, image="/goblin.jpg")

#Skeleton
class Skeleton(Enemy):
    def __init__(self):
        super().__init__(name="Skeleton", hp=10, defence=0, damage=4, image="/skeleton.jpg")

#Imp 
class Imp(Enemy):
    def __init__(self):
        super().__init__(name="Imp", hp=5, defence=2, damage=2, image="/imp.jpg")

#Giant
class Giant(Enemy):
    def __init__(self):
        super().__init__(name="Giant", hp=30, defence=5, damage=5, image="/giant.jpg")