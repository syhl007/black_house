import random

import constant
from item_card import Item
from omen_card import Omen
from util import user_input


class Monster:
    def __init__(self, name, power, speed, san, know):
        self.name = name
        self.power = power
        self.speed = speed
        self.san = san
        self.know = know
        self.move_bar = speed
        self.camp = -1
        self.attack_times = 1
        self.buff = []
        self.room = None
        self.floor = None

    def __repr__(self):
        return self.name

    # 骰点
    def dice(self, min=0, max=2, n=1):
        res = [random.randint(min, max) for i in range(n)]
        return res

    # 获取属性
    def get(self, ability):
        if ability == '力量':
            return self.power
        elif ability == '速度':
            return self.speed
        elif ability == '意志':
            return self.san
        elif ability == '知识':
            return self.know
        else:
            return None

    # 袭击
    def attack(self, target):
        self.attack_times -= 1
        pass

    # 反击
    def counter(self, ability='力量'):
        pass

    # 受伤
    def hurt(self, type):
        self.buff.append("昏迷")

    # 行动前置
    def before_move(self):
        if "昏迷" in self.buff:
            self.buff.remove("昏迷")
            self.move_bar = 0

    # 移动
    def move(self, direction):
        self.before_move()
        # 敌对干扰判断
        enemy = len([x for x in self.room.get_creatures(self) if x.camp != self.camp])
        self.move_bar -= enemy
        # 首次移动判断
        if self.move_bar <= 0:
            print("行动力不足")
            return
        # 房间门判断
        if self.room.door[direction] >= 1:
            if direction == 0:
                x = self.room.x
                y = self.room.y - 1
            elif direction == 1:
                x = self.room.x + 1
                y = self.room.y
            elif direction == 2:
                x = self.room.x
                y = self.room.y + 1
            elif direction == 3:
                x = self.room.x - 1
                y = self.room.y
            else:
                x = self.room.x
                y = self.room.y
            try:
                new_room = constant.game_map[self.floor].map[x][y]
                if new_room is None:
                    print("不可进行探险")
                    return
            except:
                print("这扇门似乎和空间牢牢的固定在一起。")
                return
            else:
                if new_room.door[[2, 3, 0, 1][direction]] == 0:
                    print("这扇门似乎和空间牢牢的固定在一起。")
                    return
                self.move_bar -= 1
            new_room.into(role=self, direction=direction)

    # 行动力复原（休息）
    def rest(self):
        self.move_bar = self.get(ability='速度')
        self.attack_times = 1
        self.room.stay(self)

    pass


class Mummy(Monster):
    def __init__(self, room, floor):
        super(Mummy, self).__init__(name="木乃伊", power=8, san=5, speed=3, know=None)
        self.room = room
        self.floor = floor
        self.items = []
        self.omens = []

    def before_move(self):
        super(Mummy, self).before_move()
        enemy = [role for role in self.room.get_creatures() if role.camp != self.camp]
        if len(enemy) > 0:
            print("敌人列表：", enemy)
            index = user_input()
            self.attack(target=enemy[index])

    def attack(self, target):
        super(Mummy, self).attack(target=target)
        res1 = {'ability': '力量', 'result': self.dice(n=self.get(ability="力量"))}
        res2 = target.counter(ability="力量")
        print("[防守]", res2)
        diff = sum(res1.get('result')) - sum(res2.get('result'))
        type = '肉体'
        if diff >= 0:
            print(self.name, "攻击成功，造成", diff, "点伤害。")
            if diff >= 2:
                print(self.name, "的攻击让", target.name, "失去平衡。")
                print("你可以选择放弃伤害值，转为偷窃目标一件道具")
                print("（注意：若目标无可被偷窃的道具，则无效。）")
                if user_input() == "y":
                    l = target.get_items_list(type="偷窃")
                    if l:
                        print(l)
                        index = int(user_input())
                        item = l[index]
                        target.lost_obj(item)
                        self.gain_obj(item)
                        return
            target.hurt(type=type, value=diff)
        elif diff < 0:
            print(target.name, "反击成功，造成", abs(diff), "点伤害。")
            if diff <= -2:
                print(target.name, "的反击让", self.name, "失去平衡。")
                print("你可以选择放弃伤害值，转为偷窃目标一件道具")
                print("（注意：若目标无可被偷窃的道具，则无效。）")
                if user_input() == "y":
                    l = self.get_items_list(type="偷窃")
                    if l:
                        print(l)
                        index = int(user_input())
                        item = l[index]
                        self.lost_obj(item)
                        target.gain_obj(item)
                        return
            self.hurt(type=type, value=abs(diff))
        return

    def counter(self, ability='力量'):
        if ability == "速度" or ability == "知识":
            return None
        else:
            res = {'ability': ability, 'result': self.dice(n=self.get(ability=ability))}
            return res

    # 获得道具/预兆
    def gain_obj(self, obj):
        if isinstance(obj, Item):
            self.items.append(obj)
        elif isinstance(obj, Omen):
            self.omens.append(obj)

    # 丢失道具
    def lost_obj(self, obj):
        if isinstance(obj, Item):
            self.items.remove(obj)
        elif isinstance(obj, Omen):
            self.omens.remove(obj)

    def __str__(self):
        dict = {"基础属性": {"人物名称": self.name, "力量": self.get(ability="力量"), "速度": self.get(ability="速度"),
                         "知识": self.get(ability="知识"), "意志": self.get(ability="意志")},}
        return json.dumps(dict, ensure_ascii=False)
