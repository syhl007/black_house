from constant import game_schedule
from item_card import armor
from room_card import room_card_set
from util import ahead_one, backward_one, draw_card, user_input, dice


class Role:
    def __init__(self, name, power, power_strip, speed, speed_strip, san, san_strip, know, know_strip):
        self.name = name
        self.power = power
        self.max_power = power
        self.power_strip = power
        self.speed = speed
        self.max_speed = speed
        self.speed_strip = speed_strip
        self.san = san
        self.max_san = san
        self.san_strip = san_strip
        self.know = know
        self.max_know = know
        self.know_strip = know_strip
        self.move = speed
        self.x = 2
        self.y = 4
        self.floor = 1
        self.buff = []
        self.items = []
        self.events = []
        self.omens = []
        self.sign = 0
        self.goal = '失忆中....'

    # 获取属性列表
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
                self.power = len(self.power_strip)
        elif ability == '速度':
            self.speed += num
            if self.speed > len(self.speed_strip):
                self.speed = len(self.speed_strip)
        elif ability == '意志':
            self.san += num
            if self.san > len(self.san_strip):
                self.san = len(self.san_strip)
        elif ability == '精神':
            self.know += num
            if self.know > len(self.know_strip):
                self.know = len(self.know_strip)
        else:
            pass

    # 降低属性
    def reduce(self, ability, num=1):
        if ability == '力量':
            self.power -= num
        elif ability == '速度':
            self.speed -= num
        elif ability == '意志':
            self.san -= num
        elif ability == '精神':
            self.know -= num
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

    # 行动力复原
    def rest(self):
        print('行动力回复了')
        self.move = self.speed

    # 受伤骰点
    def hurt(self, type, n=1):
        res = dice(role=self, n=n)
        if type == '肉体' and armor in self.items:
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

    # 探险
    def explore(self):
        new_room = room_card_set.pop()
        while new_room.floor[self.floor] == 0:
            room_card_set.add(new_room)
            new_room = room_card_set.pop()
        return new_room

    # 对抗
    def combat(self, ability='力量', n=0):
        num = self.get(ability=ability) + n
        # 最多8个骰子
        if num >= 8:
            num = 8
        res = dice(role=self, n=num)
        return res

    # 能力挑战
    def ability_challenge(self, ability, n=0, type='room'):
        if type == 'event' and "蜡烛" in self.buff:
            n += 1
        if "天使的羽毛（生效中）" in self.buff:
            self.buff.remove("天使的羽毛（生效中）")
            res = [int(user_input())]
            return res
        num = self.get(ability=ability) + n
        # 最多8个骰子
        if num >= 8:
            num = 8
        res = dice(role=self, n=num)
        if "肾上腺素（生效中）" in self.buff:
            self.buff.remove("肾上腺素（生效中）")
            res.append(4)
        return res


class Map:
    def __init__(self, floor):
        self.floor = floor
        self.map = [[None, None, None, None, None] for i in range(5)]
        if floor == 0:
            self.map[2][2] = HouseCard(name='下台阶',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       item_type=None,
                                       floor=0,
                                       describtion=None)
        elif floor == 2:
            self.map[2][2] = HouseCard(name='上台阶',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       item_type=None,
                                       floor=2,
                                       describtion=None)
        else:
            self.map[2][2] = HouseCard(name='大厅楼梯间',
                                       door=[0, 0, 1, 0],
                                       window=[0, 0, 0, 2],
                                       card_img=None,
                                       item_type=None,
                                       floor=1,
                                       describtion=None)
            self.map[2][3] = HouseCard(name='大厅02',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       item_type=None,
                                       floor=1,
                                       describtion=None)
            self.map[2][4] = HouseCard(name='大厅01',
                                       door=[1, 1, 0, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       item_type=None,
                                       floor=1,
                                       describtion=None)
            self.floor = 1


class Link:
    def __init__(self, start, end, one_way=False, flag=True, times=-1):
        self.start = start
        self.end = end
        self.one_way = one_way
        self.flag = flag
        self.times = times


class HouseCard:
    def __init__(self, name, door, window, card_img, describtion, item_type, floor, sign=None):
        self.name = name
        self.door = door
        self.window = window
        self.card_img = card_img
        self.describtion = describtion
        self.item_type = item_type
        self.floor = floor
        self.sign = sign
        self.role = []
        self.enemy = []
        self.links = []
        self.items = []

    def rotate_room(self, type=1):
        if type == 1:
            self.door = ahead_one(self.door)
            self.window = ahead_one(self.window)
        else:
            self.door = backward_one(self.door)
            self.window = backward_one(self.window)

    def set_link(self, link):
        self.links.append(link)

    def into(self, role):
        if self.item_type is not None:
            if self.item_type == '事件':
                role.events.append(draw_card(self.item_type))
            elif self.item_type == '预兆':
                role.omens.append(draw_card(self.item_type))
            elif self.item_type == '物品':
                role.items.append(draw_card(self.item_type))
            self.item_type = None
        pass

    def stay(self, role):
        pass

    def leave(self, role):
        pass

    def passaway(self, role):
        pass

    def use(self, role):
        pass


class Item:
    def __init__(self, name, card_img):
        self.name = name
        self.card_img = card_img
        self.owner = None

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

