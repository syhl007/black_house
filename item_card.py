from card import Item

from constant import game_map


# ------------------------------------血剑------------------------------------
class BloodSword(Item):
    def __init__(self):
        super(BloodSword, self).__init__(card_img=None)

    def use(self):
        super(BloodSword, self).use()
        self.owner.combat(ability='力量', n=3)

    def set_owner(self, owner):
        if owner is None:
            super(BloodSword, self).set_owner(owner)
        else:
            print("无法转交")

    def discard(self):
        print("无法丢弃")

    def lost(self):
        self.owner.hurt(type='肉体', n=2)
        super(BloodSword, self).lost()


# -------------------------------年代久远的护符------------------------------------
class Talisman(Item):
    def __init__(self):
        super(Talisman, self).__init__(card_img=None)

    def get(self):
        super(Talisman, self).get()
        self.owner.promote(ability='力量')
        self.owner.promote(ability='速度')
        self.owner.promote(ability='意志')
        self.owner.promote(ability='知识')

    def lost(self):
        self.owner.reduce(ability='力量')
        self.owner.reduce(ability='速度')
        self.owner.reduce(ability='意志')
        self.owner.reduce(ability='知识')
        super(Talisman, self).lost()


# -------------------------------督伊德教的小首饰------------------------------------
class Jewellery(Item):
    def __init__(self):
        super(Jewellery, self).__init__(card_img=None)

    def get(self):
        super(Jewellery, self).get()
        self.owner.promote(ability='速度')

    def lost(self):
        self.owner.reduce(ability='速度')
        super(Jewellery, self).lost()

    def use(self):
        room = game_map[self.owner.floor].map[self.owner.x][self.owner.y]
        for e in room.enemy:
            e.get_coma()
        self.lost()


# -------------------------------治疗药膏------------------------------------
class Ointment(Item):
    def __init__(self):
        super(Ointment, self).__init__(card_img=None)

    def use(self, ability):
        self.owner.recover(ability=ability)
        self.lost()


# -------------------------------治疗药膏------------------------------------
class Rope(Item):
    def __init__(self):
        super(Rope, self).__init__(card_img=None)

    def have(self):
        pass


# -------------------------------蜡烛-------------------------------------
class Candle(Item):
    def __init__(self):
        super(Candle, self).__init__(card_img=None)

    def have(self):
        pass


# -------------------------------肾上腺素-------------------------------------
class Adrenaline(Item):
    def __init__(self):
        super(Adrenaline, self).__init__(card_img=None)

    def use(self):
        self.lost()


# -------------------------------天使的羽毛-------------------------------------
class Feather(Item):
    def __init__(self):
        super(Feather, self).__init__(card_img=None)

    def use(self):
        self.lost()


# -------------------------------炸药-------------------------------------
class Explosive(Item):
    def __init__(self):
        super(Explosive, self).__init__(card_img=None)

    def use(self):
        self.lost()


# -------------------------------幸运石-------------------------------------
class LuckStone(Item):
    def __init__(self):
        super(LuckStone, self).__init__(card_img=None)

    def use(self):
        self.lost()


# -------------------------------玩具猴-------------------------------------
class Monkey(Item):
    def __init__(self):
        super(Monkey, self).__init__(card_img=None)

    def get(self):
        super(Monkey, self).get()
        self.owner.promote(ability='速度')
        self.owner.promote(ability='知识')

    def lost(self):
        self.owner.reduce(ability='速度')
        self.owner.reduce(ability='知识')
        super(Monkey, self).lost()

    def have(self):
        pass


# -------------------------------手斧-------------------------------------
class Axe(Item):
    def __init__(self):
        super(Axe, self).__init__(card_img=None)

    def use(self):
        super(Axe, self).use()
        self.owner.combat(ability='力量', n=1)


# -------------------------------铠甲-------------------------------------
class Armor(Item):
    def __init__(self):
        super(Armor, self).__init__(card_img=None)

    def have(self):
        pass

    def discard(self):
        self.owner = None

    def lost(self):
        return


# -------------------------------幸运兔脚-------------------------------------
class RabbitFoot(Item):
    def __init__(self):
        super(RabbitFoot, self).__init__(card_img=None)

    def use(self):
        pass


# -------------------------------魔术盒子-------------------------------------
class MagicBox(Item):
    def __init__(self):
        super(MagicBox, self).__init__(card_img=None)

    def use(self):
        if self.owner.ability_challenge(ability='知识', goal=6):
            pass
        else:
            pass


# -------------------------------左轮手枪-------------------------------------
class Gun(Item):
    def __init__(self):
        super(Gun, self).__init__(card_img=None)

    def use(self):
        self.owner.combat(ability='速度', n=1)