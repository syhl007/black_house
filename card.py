import json
import random

from constant import room_card_set, game_map, game_schedule
from item_card import Item
from omen_card import Omen
from util import user_input, live_map_cheak, set_room


class Map:
    def __init__(self, floor):
        self.floor = floor
        self.map = [[None for n in range(10)] for i in range(10)]


# 角色
class Role:
    def __init__(self, name, power, power_strip, speed, speed_strip, san, san_strip, know, know_strip):
        self.name = name
        self.power = power
        self.max_power = power
        self.power_strip = power_strip
        self.extra_power = 0
        self.speed = speed
        self.max_speed = speed
        self.speed_strip = speed_strip
        self.extra_speed = 0
        self.san = san
        self.max_san = san
        self.san_strip = san_strip
        self.extra_san = 0
        self.know = know
        self.max_know = know
        self.know_strip = know_strip
        self.extra_know = 0
        self.move_bar = speed
        self.floor = 1
        self.room = None
        self.buff = []
        self.items = []
        self.events = []
        self.omens = []
        self.camp = 0
        self.goal = '失忆中....'
        self.first_move = True

    def __repr__(self):
        return self.name

    # 骰点
    def dice(self, min=0, max=2, n=1):
        res = [random.randint(min, max) for i in range(n)]
        # 幸运石判断
        if "幸运石" in self.buff:
            choose = bool(user_input())
            if choose:
                self.buff.remove("幸运石")
                index = json.load(user_input())
                for i in index:
                    res[i] = random.randint(0, 2)
        # 幸运兔脚判断
        if "幸运兔脚" in self.buff:
            choose = bool(user_input())
            if choose:
                index = int(user_input())
                res[index] = random.randint(0, 2)
        print("[骰点结果为]", res)
        return res

    # 获取属性
    def get(self, ability):
        if ability == '力量':
            return self.power_strip[self.power]
        elif ability == '速度':
            return self.speed_strip[self.speed]
        elif ability == '意志':
            return self.san_strip[self.san]
        elif ability == '知识':
            return self.know_strip[self.know]
        else:
            return 0

    # 提升属性
    def promote(self, ability, num=1):
        if ability == '力量':
            self.power += num
            if self.power > len(self.power_strip):
                self.extra_power += self.power - len(self.power_strip)
                self.power = len(self.power_strip)
        elif ability == '速度':
            self.speed += num
            if self.speed > len(self.speed_strip):
                self.extra_speed += self.speed - len(self.speed_strip)
                self.speed = len(self.speed_strip)
        elif ability == '意志':
            self.san += num
            if self.san > len(self.san_strip):
                self.extra_san += self.san - len(self.san_strip)
                self.san = len(self.san_strip)
        elif ability == '精神':
            self.know += num
            if self.know > len(self.know_strip):
                self.extra_know += self.know - len(self.know_strip)
                self.know = len(self.know_strip)
        else:
            pass

    # 降低属性
    def reduce(self, ability, num=1):
        if ability == '力量':
            self.extra_power -= num
            if self.extra_power < 0:
                self.power += self.extra_power
                self.extra_power = 0
        elif ability == '速度':
            self.extra_speed -= num
            if self.extra_speed < 0:
                self.speed += self.extra_speed
                self.extra_speed = 0
        elif ability == '意志':
            self.extra_san -= num
            if self.extra_san < 0:
                self.san += self.extra_san
                self.extra_san = 0
        elif ability == '知识':
            self.extra_know -= num
            if self.extra_know < 0:
                self.know += self.extra_know
                self.extra_know = 0
        else:
            pass
        # 第一游戏阶段不会死亡
        if game_schedule < 1:
            if self.power <= 0:
                self.power = 1
            if self.speed <= 0:
                self.speed = 1
            if self.san <= 0:
                self.san = 1
            if self.know <= 0:
                self.know = 1
        else:
            self.die()

    # 能力值复原（治疗）
    def recover(self, ability):
        if ability == '力量' and self.power < self.max_power:
            self.power = self.max_power
        elif ability == '速度' and self.speed < self.max_speed:
            self.speed = self.max_speed
        elif ability == '意志' and self.san < self.max_san:
            self.san = self.max_san
        elif ability == '知识' and self.know < self.max_know:
            self.know = self.max_know
        else:
            pass

    # 行动力复原（休息）
    def rest(self):
        print('行动力回复了')
        if "灯灭" in self.buff:
            self.move_bar = 1
        self.first_move = True
        self.move_bar = self.get(ability='速度')
        self.room.stay(self)

    # 受伤骰点
    def hurt(self, type, n=1, value=None):
        if value is None:
            res = self.dice(n=n)
        else:
            res = [value]
        if type == '精神' and '颅骨' in self.buff:
            print("你手上的颅骨闪烁着诡异的光芒，那些精神上的冲击似乎化作了实体伤害打在你的身上。")
            if bool(user_input()):
                type = '肉体'
        # 铠甲判断
        if type == '肉体' and '铠甲' in self.buff:
            res.append(-1)
        print('受到', res, '=', sum(res), '点的', type, '伤害')
        while True:
            if sum(res) <= 0:
                break
            print("(身体伤害分配到【力量】与【速度】上|精神伤害分配到【意志】与【知识】上)")
            num1 = int(input("扣除第一属性: "))
            if abs(num1) == sum(res):
                self.injured(type=type, num1=sum(res), num2=0)
                break
            elif abs(num1) == 0:
                self.injured(type=type, num1=0, num2=sum(res))
                break
            num2 = int(input("扣除第二属性: "))
            if abs(num1) + abs(num2) == sum(res):
                self.injured(type=type, num1=num1, num2=num2)
                break
            else:
                print('输入值错误')

    # 受伤减值
    def injured(self, type, num1, num2):
        if type == '肉体':
            self.power -= num1
            self.speed -= num2
        elif type == '精神':
            self.san -= num1
            self.know -= num2
        else:
            pass
        # 第一游戏阶段不会死亡
        if game_schedule < 1:
            if self.power <= 0:
                self.power = 1
            if self.speed <= 0:
                self.speed = 1
            if self.san <= 0:
                self.san = 1
            if self.know <= 0:
                self.know = 1

    # 挣扎脱困
    def struggle(self, name, ability, goal, role=None):
        if name + "3" in self.buff or name + "2" in self.buff or name + "1" in self.buff:
            print(self.name, "被", name, "困住，无法移动")
            if role is None:
                res = self.ability_challenge(ability=ability, type="事件")
                print(self.name, "尝试挣脱，结果为：", res)
            else:
                res = role.ability_challenge(ability=ability, type="事件")
                print(role.name, "尝试帮助", self.name, "，结果为：", res)
            if sum(res) >= goal:
                self.buff.remove(name + "3") if name + "3" in self.buff else None
                self.buff.remove(name + "2") if name + "2" in self.buff else None
                self.buff.remove(name + "1") if name + "1" in self.buff else None
                return True
            else:
                print(self.name, "没能脱出，但似乎松动了些。")
                if name + "3" in self.buff:
                    self.buff.remove(name + "3")
                    self.buff.append(name + "2")
                elif name + "2" in self.buff:
                    self.buff.remove(name + "2")
                    self.buff.append(name + "1")
                elif name + "1" in self.buff:
                    print("剩余的", name, "不再阻难你，但你看来也需要休息一下才能行动了。")
                    self.buff.remove(name + "1")
                self.move_bar = 0
                self.first_move = False
                return False
        else:
            return True

    # 移动
    def move(self, direction):
        # 丝网判断
        self.struggle(name="丝网", ability="力量", goal=4)
        # 瓦砾判断
        self.struggle(name="瓦砾", ability="力量", goal=4)
        # 敌对干扰判断
        enemy = len([x for x in self.room.get_creatures(self) if x.camp != self.camp])
        self.move_bar -= enemy
        # 首次移动判断
        if not self.first_move and self.move_bar <= 0:
            print("行动力不足")
            return
        # 房间门判断
        if self.room.door[direction] >= 1:
            if self.room.door[direction] == 9:
                if not self.room.across(self, direction):
                    self.first_move = False
                    self.move_bar = 0
                    return
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
                new_room = game_map[self.floor].map[x][y]
            except:
                print("这扇门似乎和空间牢牢的固定在一起。")
                return
            if new_room is None:
                while True:
                    new_room = self.explore(direction)
                    set_room(new_room, self.floor, x, y)
                    if live_map_cheak(floor=self.floor) > 0:
                        break
                    else:
                        room_card_set.append(new_room)
                        random.shuffle(room_card_set)
                        set_room(None, self.floor, x, y)
                self.move_bar = 0
            else:
                if new_room.door[[2, 3, 0, 1][direction]] == 0:
                    print("这扇门似乎和空间牢牢的固定在一起。")
                    return
                self.move_bar -= 1
            self.first_move = False
            self.room.leave(self)
            new_room.into(role=self, direction=direction)

    # 获得道具/预兆
    def gain_obj(self, obj):
        if isinstance(obj, Item):
            self.items.append(obj)
            obj.set_owner(self)
        elif isinstance(obj, Omen):
            self.omens.append(obj)
            obj.set_owner(self)

    # 丢失道具
    def lost_obj(self, obj):
        if isinstance(obj, Item):
            self.items.remove(obj)
            obj.lost()
        elif isinstance(obj, Omen):
            self.omens.remove(obj)
            obj.lost()

    # 探险
    def explore(self, direction):
        new_room = room_card_set.pop()
        while new_room.floor[self.floor] == 0:
            room_card_set.append(new_room)
            new_room = room_card_set.pop()
        while new_room.door[[2, 3, 0, 1][direction]] == 0:
            new_room.rotate()
        return new_room

    # 袭击
    def attack(self, target, ability='力量', n=0, arms=None):
        if arms is None and arms != "空手":
            return arms.use()
        else:
            num = self.get(ability=ability) + n
            # 最多8个骰子
            if num >= 8:
                num = 8
            res1 = {'ability': ability, 'result': self.dice(n=num)}
            print("[进攻]", res1)
            if target.counter(ability=ability) is None:
                print(self.name, "的攻击对目标没有任何效果。")
                return
            res2 = target.counter(ability=ability)
            print("[防守]", res2)
            diff = sum(res1.get('result')) - sum(res2.get('result'))
            if ability == '力量' or ability == '速度':
                type = '肉体'
            else:
                type = '精神'
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

    # 反击
    def counter(self, ability='力量'):
        res = {'ability': ability, 'result': self.dice(n=self.get(ability=ability))}
        return res

    # 武器列表
    def get_weapon_list(self):
        return ["空手"] + [x for x in self.items if x.is_weapon] + [x for x in self.omens if x.is_weapon]

    # 物品列表
    def get_items_list(self, type=None):
        if type == "使用":
            l = [x for x in self.items if x.is_use]
        elif type == "偷窃":
            l = [x for x in self.items if x.is_steal]
        elif type == "丢弃":
            l = [x for x in self.items if x.is_discard]
        elif type == "给予":
            l = [x for x in self.items if x.is_give]
        else:
            l = self.items
        return l

    # 预兆列表
    def get_omens_list(self, type=None):
        if type == "使用":
            l = [x for x in self.omens if x.is_use]
        elif type == "偷窃":
            l = [x for x in self.omens if x.is_steal]
        elif type == "丢弃":
            l = [x for x in self.omens if x.is_discard]
        elif type == "给予":
            l = [x for x in self.omens if x.is_give]
        else:
            l = self.omens
        return l

    # buff列表
    def get_buff_list(self, type=None):
        return self.buff

    # 能力挑战
    def ability_challenge(self, ability, n=0, type='房间'):
        if type == '事件' and '蜡烛' in self.buff:
            n += 1
        if "水滴" in self.room.get_sign(self):
            print("停不下来的滴答声让你无法集中精神，骰子-1")
            n -= 1
        if "祝福" in self.room.get_sign(self):
            print("神圣的气息让你大有增益，骰子+1")
            n += 1
        if '天使的羽毛（生效中）' in self.buff:
            self.buff.remove('天使的羽毛（生效中）')
            res = [int(user_input())]
            return res
        num = self.get(ability=ability) + n
        # 最多8个骰子
        if num >= 8:
            num = 8
        res = self.dice(n=num)
        if '肾上腺素（生效中）' in self.buff:
            self.buff.remove('肾上腺素（生效中）')
            res.append(4)
        print(self.name, "[", ability, "]挑战结果为：", res)
        return res

    # 死亡
    def die(self):
        self.room.items += self.items
        self.room.otems += self.omens
        self.events = []

    def __str__(self):
        dict = {"基础属性": {"人物名称": self.name, "力量": self.get(ability="力量"), "速度": self.get(ability="速度"),
                         "知识": self.get(ability="知识"), "意志": self.get(ability="意志")},
                "物品列表": self.get_items_list(),
                "预兆列表": self.get_omens_list(),
                "buff列表": self.get_buff_list()}
        return json.dumps(dict, ensure_ascii=False)
