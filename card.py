import json
import random

from constant import room_card_set, game_map
from util import user_input, live_map_cheak

# 游戏进度
game_schedule = 0


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
        self.x = 4
        self.y = 9
        self.floor = 1
        self.room = None
        self.buff = []
        self.items = []
        self.events = []
        self.omens = []
        self.camp = 0
        self.goal = '失忆中....'
        self.first_move = True

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

    # 移动
    def move(self, direction):
        if "丝网" in self.buff:
            print("")
        enemy = len([x for x in self.room.get_creatures(self) if x.camp != self.camp])
        self.move_bar -= enemy
        if not self.first_move and self.move_bar <= 0:
            print("行动力不足")
            return
        if self.room.door[direction] >= 1:
            if self.room.door[direction] == 9:
                if not self.room.across(self, direction):
                    self.first_move = False
                    return
            if direction == 0:
                x = self.x
                y = self.y - 1
            elif direction == 1:
                x = self.x + 1
                y = self.y
            elif direction == 2:
                x = self.x
                y = self.y + 1
            elif direction == 3:
                x = self.x - 1
                y = self.y
            else:
                x = self.x
                y = self.y
            try:
                new_room = game_map[self.floor].map[x][y]
            except:
                print("这扇门似乎和空间牢牢的固定在一起。")
                return
            if new_room is None:
                while True:
                    new_room = self.explore(direction)
                    game_map[self.floor].map[x][y] = new_room
                    if live_map_cheak(floor=self.floor) > 0:
                        break
                    else:
                        room_card_set.append(new_room)
                        random.shuffle(room_card_set)
                        game_map[self.floor].map[x][y] = None
                self.x = x
                self.y = y
                self.move_bar = 0
            else:
                if new_room.door[[2, 3, 0, 1][direction]] == 0:
                    print("这扇门似乎和空间牢牢的固定在一起。")
                    return
                self.x = x
                self.y = y
                self.move_bar -= 1
            self.first_move = False
            self.room.leave(self)
            new_room.into(role=self, direction=direction)


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
        if arms != None:
            return arms.use()
        else:
            num = self.get(ability=ability) + n
            # 最多8个骰子
            if num >= 8:
                num = 8
            res1 = {'ability': ability, 'result': self.dice(n=num)}
            print("[进攻]", res1)
            if target.get(ability=ability) is None:
                raise Exception()
            res2 = target.counter(ability=ability)
            print("[防守]", res2)
            diff = sum(res1.get('result')) - sum(res2.get('result'))
            if ability == '力量' or ability == '速度':
                type = '肉体'
            else:
                type = '精神'
            if diff >= 0:
                if diff > 2:
                    if user_input():
                        return target.steal_list()
                target.hurt(type=type, value=diff)
            elif diff < 0:
                if diff < -2:
                    if user_input():
                        return self.steal_list()
                self.hurt(type=type, value=diff)
            return res1

    # 反击
    def counter(self, ability='力量'):
        res = {'ability': ability, 'result': self.dice(n=self.get(ability=ability))}
        return res

    # 物品列表
    def items_list(self, type=None):
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
    def omens_list(self, type=None):
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
    def buff_list(self, type=None):
        return self.buff

    # 能力挑战
    def ability_challenge(self, ability, n=0, type='房间'):
        if type == '事件' and '蜡烛' in self.buff:
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
