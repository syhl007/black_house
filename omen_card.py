import random

from card import Item
from util import dice, challenge

omen_card_set = []


# -------------------------------脏狗-------------------------------------
class Dog(Item):
    def __init__(self):
        super(Dog, self).__init__(name="脏狗", card_img=None)

    def get(self):
        super(Dog, self).get()
        self.owner.promote(ability="力量")
        self.owner.promote(ability="意志")

    def lost(self):
        self.owner.reduce(ability="力量")
        self.owner.reduce(ability="意志")
        super(Dog, self).lost()

    def use(self):
        super(Dog, self).use()


dog = Dog()
omen_card_set.append(dog)


# -------------------------------疯汉-------------------------------------
class Crazy(Item):
    def __init__(self):
        super(Crazy, self).__init__(name="疯汉", card_img=None)

    def get(self):
        super(Crazy, self).get()
        self.owner.promote(ability="力量", num=2)
        self.owner.reduce(ability="意志")

    def lost(self):
        self.owner.reduce(ability="力量", num=2)
        self.owner.promote(ability="意志")
        super(Crazy, self).lost()


crazy = Crazy()
omen_card_set.append(crazy)


# -------------------------------书本-------------------------------------
class Book(Item):
    def __init__(self):
        super(Book, self).__init__(name="书本", card_img=None)

    def get(self):
        super(Book, self).get()
        self.owner.promote(ability="知识", num=2)

    def lost(self):
        self.owner.reduce(ability="知识", num=2)
        super(Book, self).lost()


book = Book()
omen_card_set.append(book)


# -------------------------------徽章-------------------------------------
class Badge(Item):
    def __init__(self):
        super(Badge, self).__init__(name="徽章", card_img=None)


badge = Badge()
omen_card_set.append(badge)


# -------------------------------圣符-------------------------------------
class Rune(Item):
    def __init__(self):
        super(Rune, self).__init__(name="圣符", card_img=None)

    def get(self):
        super(Rune, self).get()
        self.owner.promote(ability="意志", num=2)

    def lost(self):
        self.owner.reduce(ability="意志", num=2)
        super(Rune, self).lost()


rune = Rune()
omen_card_set.append(rune)


# -------------------------------指环-------------------------------------
class Ring(Item):
    def __init__(self):
        super(Ring, self).__init__(name="指环", card_img=None)

    def use(self):
        self.owner.combat(ability='意志', n=0)


ring = Ring()
omen_card_set.append(ring)


# -------------------------------颅骨-------------------------------------
class Skull(Item):
    def __init__(self):
        super(Skull, self).__init__(name="颅骨", card_img=None)


skull = Skull()
omen_card_set.append(skull)


# -------------------------------噬咬-------------------------------------
class Bite(Item):
    def __init__(self):
        super(Bite, self).__init__(name="噬咬", card_img=None)

    def get(self):
        super(Bite, self).get()
        act = [random.randint(0, 2) for i in range(4)]
        dice(self.owner, self.owner.get(ability='力量'))

    def lost(self):
        pass

    def discard(self):
        pass


bite = Bite()
omen_card_set.append(bite)


# -------------------------------面具-------------------------------------
class Mask(Item):
    def __init__(self):
        super(Mask, self).__init__(name="面具", card_img=None)

    def use(self):
        super(Mask, self).use()
        if challenge(self.owner, ability='意志', goal=4):
            if "面具（生效中）" not in self.owner.buff:
                self.owner.reduce(ability='意志', num=2)
                self.owner.promote(ability='知识', num=2)
                self.owner.buff.append("面具（生效中）")
            elif "面具（生效中）" in self.owner.buff:
                self.owner.promote(ability='意志', num=2)
                self.owner.reduce(ability='知识', num=2)
                self.owner.buff.remove("面具（生效中）")


mask = Mask()
omen_card_set.append(mask)


# -------------------------------女孩-------------------------------------
class Gril(Item):
    def __init__(self):
        super(Gril, self).__init__(name="女孩", card_img=None)

    def get(self):
        super(Gril, self).get()
        self.owner.promote(ability="知识")
        self.owner.promote(ability="意志")

    def lost(self):
        self.owner.reduce(ability="知识")
        self.owner.reduce(ability="意志")
        super(Gril, self).lost()


gril = Gril()
omen_card_set.append(gril)


# -------------------------------灵板-------------------------------------
class SpiritBoard(Item):
    def __init__(self):
        super(SpiritBoard, self).__init__(name="灵板", card_img=None)

    def use(self):
        pass


spirit_board = SpiritBoard()
omen_card_set.append(spirit_board)


# -------------------------------长矛-------------------------------------
class Spear(Item):
    def __init__(self):
        super(Spear, self).__init__(name="长矛", card_img=None)

    def use(self):
        self.owner.combat(ability='力量', n=2)


spear = Spear()
omen_card_set.append(spear)


# -------------------------------水晶球-------------------------------------
class CrystalBall(Item):
    def __init__(self):
        super(CrystalBall, self).__init__(name="水晶球", card_img=None)

    def use(self):
        pass


crystal_ball = CrystalBall()
omen_card_set.append(crystal_ball)
