from constant import game_map, item_card_set


# 道具
class Item:
    def __init__(self, name, card_img, is_weapen=False, is_use=True, is_steal=True, is_discard=True, is_give=True):
        self.name = name
        self.card_img = card_img
        self.owner = None
        self.is_weapen = is_weapen
        self.is_use = is_use
        self.is_steal = is_steal
        self.is_discard = is_discard
        self.is_give = is_give

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

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


# ------------------------------------血剑------------------------------------
from util import challenge


class BloodSword(Item):
    def __init__(self, is_weapen=True):
        super(BloodSword, self).__init__(name="血剑", card_img=None)

    def use(self):
        super(BloodSword, self).use()
        self.owner.reduce(ability='速度')
        self.owner.attack(ability='力量', n=3)

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


blood_sword = BloodSword()
item_card_set.append(blood_sword)


# -------------------------------年代久远的护符------------------------------------
class Talisman(Item):
    def __init__(self):
        super(Talisman, self).__init__(name="年代久远的护符", card_img=None)

    def get(self):
        super(Talisman, self).get()
        self.owner.promote(ability='力量')
        self.owner.promote(ability='速度')
        self.owner.promote(ability='意志')
        self.owner.promote(ability='知识')

    def lost(self):
        self.owner.reduce(ability='力量', num=3)
        self.owner.reduce(ability='速度', num=3)
        self.owner.reduce(ability='意志', num=3)
        self.owner.reduce(ability='知识', num=3)
        super(Talisman, self).lost()


talisman = Talisman()
item_card_set.append(talisman)


# -------------------------------督伊德教的小首饰------------------------------------
class Jewellery(Item):
    def __init__(self):
        super(Jewellery, self).__init__(name="督伊德教的小首饰", card_img=None)

    def get(self):
        super(Jewellery, self).get()
        self.owner.promote(ability='速度')

    def lost(self):
        self.owner.reduce(ability='速度')
        super(Jewellery, self).lost()

    def use(self):
        room = self.owner.room
        for e in room.enemy:
            e.get_coma()
        self.lost()


jewellery = Jewellery()
item_card_set.append(jewellery)


# -------------------------------治疗药膏------------------------------------
class Ointment(Item):
    def __init__(self):
        super(Ointment, self).__init__(name="治疗药膏", card_img=None)

    def use(self):
        # target.recover(ability=ability)
        self.lost()


ointment = Ointment()
item_card_set.append(ointment)


# -------------------------------绳索------------------------------------
class Rope(Item):
    def __init__(self):
        super(Rope, self).__init__(name="绳索", card_img=None)

    def use(self):
        room = game_map[self.owner.floor].map[self.owner.x][self.owner.y]
        pass


rope = Rope()
item_card_set.append(rope)


# -------------------------------蜡烛-------------------------------------
class Candle(Item):
    def __init__(self):
        super(Candle, self).__init__(name="蜡烛", card_img=None)

    def have(self):
        pass


candle = Candle()
item_card_set.append(candle)


# -------------------------------肾上腺素-------------------------------------
class Adrenaline(Item):
    def __init__(self):
        super(Adrenaline, self).__init__(name="肾上腺素", card_img=None)

    def use(self):
        self.owner.buff.append('肾上腺素（生效中）')
        self.lost()


adrenaline = Adrenaline()
item_card_set.append(adrenaline)


# -------------------------------天使的羽毛-------------------------------------
class Feather(Item):
    def __init__(self):
        super(Feather, self).__init__(name="天使的羽毛", card_img=None)

    def use(self):
        self.owner.buff.append('天使的羽毛（生效中）')
        self.lost()


feather = Feather()
item_card_set.append(feather)


# -------------------------------炸药-------------------------------------
class Explosive(Item):
    def __init__(self):
        super(Explosive, self).__init__(name="炸药", card_img=None)

    def use(self):
        self.lost()


explosive = Explosive()
item_card_set.append(explosive)


# -------------------------------幸运石-------------------------------------
class LuckStone(Item):
    def __init__(self):
        super(LuckStone, self).__init__(name="幸运石", card_img=None)

    def use(self):
        self.lost()


luck_stone = LuckStone()
item_card_set.append(luck_stone)


# -------------------------------玩具猴-------------------------------------
class Monkey(Item):
    def __init__(self):
        super(Monkey, self).__init__(name="玩具猴", card_img=None)

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


monkey = Monkey()
item_card_set.append(monkey)


# -------------------------------手斧-------------------------------------
class Axe(Item):
    def __init__(self):
        super(Axe, self).__init__(name="手斧", card_img=None)

    def use(self):
        super(Axe, self).use()
        self.owner.attack(ability='力量', n=1)


axe = Axe()
item_card_set.append(axe)


# -------------------------------铠甲-------------------------------------
class Armor(Item):
    def __init__(self):
        super(Armor, self).__init__(name="铠甲", card_img=None)

    def have(self):
        pass

    def discard(self):
        self.owner.buff.remove("铠甲")
        self.owner = None

    def lost(self):
        return


armor = Armor()
item_card_set.append(armor)


# -------------------------------幸运兔脚-------------------------------------
class RabbitFoot(Item):
    def __init__(self):
        super(RabbitFoot, self).__init__(name="幸运兔脚", card_img=None)


rabbit_foot = RabbitFoot()
item_card_set.append(rabbit_foot)


# -------------------------------魔术盒子-------------------------------------
class MagicBox(Item):
    def __init__(self):
        super(MagicBox, self).__init__(name="魔术盒子", card_img=None)

    def use(self):
        if challenge(self.owner, ability='知识', goal=6):
            pass
        else:
            pass


magic_box = MagicBox()
item_card_set.append(magic_box)


# -------------------------------左轮手枪-------------------------------------
class Gun(Item):
    def __init__(self):
        super(Gun, self).__init__(name="左轮手枪", card_img=None)

    def use(self):
        self.owner.attack(ability='速度', n=1)


gun = Gun()
item_card_set.append(gun)
