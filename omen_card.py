import random

from constant import omen_card_set


# 预兆
class Omen:
    def __init__(self, name, card_img, is_use=True, is_steal=True, is_discard=True, is_give=True):
        self.name = name
        self.card_img = card_img
        self.owner = None
        self.is_use = is_use
        self.is_steal = is_steal
        self.is_discard = is_discard
        self.is_give = is_give

    # 转交/获得
    def set_owner(self, owner):
        if self.owner is not None:
            self.lost()
        self.owner = owner
        self.get()

    # 获得
    def get(self):
        self.owner.buff.append(self.name)
        pass

    # 持有
    def own(self):
        pass

    # 使用
    def use(self):
        pass

    # 丢弃
    def discard(self):
        self.lost()
        pass

    # 失去
    def lost(self):
        self.owner.buff.remove(self.name)
        self.owner = None
        pass


# -------------------------------脏狗-------------------------------------
class Dog(Omen):
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
class Crazy(Omen):
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
class Book(Omen):
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
class Badge(Omen):
    def __init__(self):
        super(Badge, self).__init__(name="徽章", card_img=None)


badge = Badge()
omen_card_set.append(badge)


# -------------------------------圣符-------------------------------------
class Rune(Omen):
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
class Ring(Omen):
    def __init__(self):
        super(Ring, self).__init__(name="指环", card_img=None)

    def use(self):
        self.owner.combat(ability='意志', n=0)


ring = Ring()
omen_card_set.append(ring)


# -------------------------------颅骨-------------------------------------
class Skull(Omen):
    def __init__(self):
        super(Skull, self).__init__(name="颅骨", card_img=None)


skull = Skull()
omen_card_set.append(skull)


# -------------------------------噬咬-------------------------------------
class Bite(Omen):
    def __init__(self):
        super(Bite, self).__init__(name="噬咬", card_img=None)

    def get(self):
        super(Bite, self).get()
        act = [random.randint(0, 2) for i in range(4)]
        self.owner.counter()

    def lost(self):
        pass

    def discard(self):
        pass


bite = Bite()
omen_card_set.append(bite)


# -------------------------------面具-------------------------------------
class Mask(Omen):
    def __init__(self):
        super(Mask, self).__init__(name="面具", card_img=None)

    def use(self):
        super(Mask, self).use()
        if self.owner.ability_challenge(ability='意志') == 4:
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
class Gril(Omen):
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
class SpiritBoard(Omen):
    def __init__(self):
        super(SpiritBoard, self).__init__(name="灵板", card_img=None)

    def use(self):
        pass


spirit_board = SpiritBoard()
omen_card_set.append(spirit_board)


# -------------------------------长矛-------------------------------------
class Spear(Omen):
    def __init__(self):
        super(Spear, self).__init__(name="长矛", card_img=None)

    def use(self):
        self.owner.combat(ability='力量', n=2)


spear = Spear()
omen_card_set.append(spear)


# -------------------------------水晶球-------------------------------------
class CrystalBall(Omen):
    def __init__(self):
        super(CrystalBall, self).__init__(name="水晶球", card_img=None)

    def use(self):
        pass


crystal_ball = CrystalBall()
omen_card_set.append(crystal_ball)

# 打乱
random.shuffle(omen_card_set)
