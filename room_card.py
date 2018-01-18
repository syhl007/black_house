import random

from card import Map
from constant import room_card_set, game_map
from sign_function import sign_func_dict
from util import draw_card, room_search, user_input, ahead_one, backward_one, set_room


# 房间卡基类
class RoomCard:
    def __init__(self, name, door, window, card_img, describtion, item_type, floor):
        self.name = name
        self.door = door
        self.window = window
        self.card_img = card_img
        self.describtion = describtion
        self.item_type = item_type
        self.floor = floor
        self.x = None
        self.y = None
        self.used = False
        self.sign = []
        self.creatures = []
        self.omens = []
        self.items = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def rotate(self, type=1):
        if type == 1:
            self.door = ahead_one(self.door)
            self.window = ahead_one(self.window)
        else:
            self.door = backward_one(self.door)
            self.window = backward_one(self.window)

    def get_creatures(self, role=None):
        return self.creatures

    def get_sign(self, role):
        return self.sign

    def into(self, role, direction=None):
        print(role.name, "进入了", self.name)
        role.room = self
        self.creatures.append(role)
        if self.item_type is not None and not self.used:
            card = draw_card(self.item_type)
            if self.item_type == '事件':
                print("事件:", card.name)
                card.do(role=role)
                role.events.append(card)
            elif self.item_type == '预兆':
                print(role.name, "找到了", card.name, "[预兆]")
                role.omens.append(card)
            elif self.item_type == '物品':
                print(role.name, "找到了", card.name, "[物品]")
                role.items.append(card)
            self.used = True

    def stay(self, role):
        pass

    def leave(self, role):
        role.room = None
        self.creatures.remove(role)

    def use(self, role):
        signs = self.get_sign(role)
        for key in signs:
            func = sign_func_dict.get(key)
            if func(role=role, room=self):
                self.get_sign(role).remove(key)
            pass


# 隔断房间基类
class PartitionRoom(RoomCard):
    def __init__(self, name, door, window, card_img, describtion, item_type, floor):
        super(PartitionRoom, self).__init__(name, [x * 9 for x in door], window, card_img, describtion, item_type,
                                            floor)
        self.sign = [['隔断'], ['隔断']]
        self.creatures = [[], []]
        self.omens = [[], []]
        self.items = [[], []]

    def __get_role_pos(self, role):
        if role in self.creatures[0]:
            return 0
        else:
            return 1

    def get_creatures(self, role=None):
        if role is None:
            return self.creatures[0] + self.creatures[1]
        index = self.__get_role_pos(role)
        return self.creatures[index]

    def get_sign(self, role):
        index = self.__get_role_pos(role)
        return self.sign[index]

    def across(self, role, direction):
        index = self.__get_role_pos(role)
        if (direction in (2, 3) and index == 0) or (direction in (0, 1) and index == 1):
            return True
        else:
            return self.challenge(role)

    def challenge(self, role):
        return False

    def into(self, role, direction=None):
        self.creatures[[0, 0, 1, 1][direction]].append(role)
        role.room = self
        print(role.name, "进入了", self.name)

    def leave(self, role):
        for l in self.creatures:
            l.remove(role) if role in l else None


# ------------------------------------下台阶------------------------------------
down_steps = RoomCard(name='下台阶',
                      door=[1, 1, 1, 1],
                      window=[0, 0, 0, 0],
                      card_img=None,
                      item_type=None,
                      floor=0,
                      describtion=None)

# ------------------------------------上台阶------------------------------------
up_steps = RoomCard(name='上台阶',
                    door=[1, 1, 1, 1],
                    window=[0, 0, 0, 0],
                    card_img=None,
                    item_type=None,
                    floor=2,
                    describtion=None)
up_steps.sign.append("下楼")

# ------------------------------------大厅楼梯间------------------------------------
staircase_0 = RoomCard(name='大厅楼梯间',
                       door=[0, 0, 1, 0],
                       window=[0, 0, 0, 2],
                       card_img=None,
                       item_type=None,
                       floor=1,
                       describtion=None)
staircase_0.sign.append("上楼")

# ------------------------------------大厅1------------------------------------
lobby_1 = RoomCard(name='大厅1',
                   door=[1, 1, 1, 1],
                   window=[0, 0, 0, 0],
                   card_img=None,
                   item_type=None,
                   floor=1,
                   describtion=None)
# ------------------------------------大厅0------------------------------------
lobby_0 = RoomCard(name='大厅0',
                   door=[1, 1, 1, 1],
                   window=[0, 0, 0, 0],
                   card_img=None,
                   item_type=None,
                   floor=1,
                   describtion=None)


# ------------------------------------设置上下楼梯------------------------------------
def up2overground(self, *args, **kwargs):
    role = kwargs.get('role')
    self.leave(role)
    role.floor = 2
    up_steps.into(role)


def back2ground(self, *args, **kwargs):
    role = kwargs.get('role')
    self.leave(role)
    role.floor = 1
    staircase_0.into(role)


from types import MethodType

staircase_0.use = MethodType(up2overground, staircase_0)
up_steps.use = MethodType(back2ground, up_steps)


# ------------------------------------崩塌的房间------------------------------------
class Collapse(RoomCard):
    def __init__(self):
        super(Collapse, self).__init__(name='崩塌的房间',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type=None,
                                       describtion=None)
        self.force = True

    def into(self, role, direction=None):
        super(Collapse, self).into(role)
        print("第一个进入本房间的玩家必须以'速度'进行'能力考验'。若骰数大于或等于5，则人物无恙。否则翻开一张地下室卡，放到地下，玩家坠落至此，并需要骰1，点数为玩家'肉体伤害'")
        if self.force:
            print('当你一脚踏进这个房间时，显然没有注意到地板上的破洞.')
            if sum(role.ability_challenge(ability='速度')) >= 5:
                print('但是你灵巧的稳住了身形，避免了掉落')
            else:
                print('你一脚踩空，下落到地下室随机地点')
                role.hurt(type='肉体')
                role.floor = 0
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                if game_map[0].map[x][y] is None:
                    set_room(role.explore(direction=random.randint(0, 3)), role.floor, x, y)
                new_room = game_map[0].map[x][y]
                self.leave(role)
                if isinstance(new_room, PartitionRoom):
                    new_room.into(role, direction=random.randint(0, 3))
                    new_room.get_sign(role).append("崩塌的房间")
                else:
                    new_room.sign.append("崩塌的房间")
                    new_room.into(role)
            self.force = False

    def use(self, role):
        super(Collapse, self).use(role)
        print('你从房间跳下')
        role.hurt(type='肉体')
        room_list = room_search(sign='崩塌的房间', floor=0)
        if len(room_list) == 0:
            role.hurt(type='肉体')
            role.floor = 0
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if game_map[0].map[x][y] is None:
                set_room(role.explore(direction=random.randint(0, 3)), role.floor, x, y)
            new_room = game_map[0].map[x][y]
            self.leave(role)
            if isinstance(new_room, PartitionRoom):
                new_room.into(role, direction=random.randint(0, 3))
                new_room.get_sign(role).append("崩塌的房间")
            else:
                new_room.sign.append("崩塌的房间")
                new_room.into(role)
        else:
            new_room = room_list[0]
            role.floor = new_room.get('floor')
            self.leave(role)
            new_room.get('room').into(role)


# ------------------------------------煤导槽-----------------------------------
class Chute(RoomCard):
    def __init__(self):
        super(Chute, self).__init__(name='煤导槽',
                                    door=[1, 0, 0, 0],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type=None,
                                    describtion=None)

    def use(self, role):
        super(Chute, self).use(role)
        print("这是一条单向通向'下台阶'的特殊通道")
        self.leave(role)
        down_steps.into(role)
        role.floor = 0
        down_steps.into(role)

    def stay(self, role):
        super(Chute, self).stay(role)
        print("这是一条单向通向'下台阶'的特殊通道")
        self.leave(role)
        down_steps.into(role)
        role.floor = 0
        down_steps.into(role)


# ------------------------------------舞厅------------------------------------
class Ballroom(RoomCard):
    def __init__(self):
        super(Ballroom, self).__init__(name='舞厅',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type='事件',
                                       describtion=None)
        self.sign.append("舞厅")


# ------------------------------------破烂的房间-----------------------------------
class Broken(RoomCard):
    def __init__(self):
        super(Broken, self).__init__(name='破烂的房间',
                                     door=[1, 0, 0, 0],
                                     window=[0, 0, 0, 0],
                                     card_img=None,
                                     floor=[1, 1, 1],
                                     item_type='预兆',
                                     describtion=None)

    def leave(self, role):
        print("离开房间时，需要以'力量'进行'能力考验'，骰数大于3，则无恙；否则'速度'下降1级，无论成功与否，人物都能离开房间。")
        print('当你准备离开这个房间时，你发现这里乱成一团，你需要费大力气开辟一条路。')
        if sum(role.ability_challenge(ability="力量")) >= 3:
            print('这很轻松，你在杂物之间分开了一条路。')
        else:
            print('杂物似乎比你想象的重得多，你费了大力气才弄出一条路，为此还弄伤了你的脚（速度减1）')
            role.reduce(ability='速度')
        super(Broken, self).leave(role)


# ------------------------------------酒窖------------------------------------
class Wine(RoomCard):
    def __init__(self):
        super(Wine, self).__init__(name='酒窖',
                                   door=[1, 0, 1, 0],
                                   window=[0, 0, 0, 0],
                                   card_img=None,
                                   floor=[1, 1, 1],
                                   item_type='物品',
                                   describtion=None)


# ------------------------------------储藏室------------------------------------
class Store(RoomCard):
    def __init__(self):
        super(Store, self).__init__(name='储藏室',
                                    door=[1, 0, 0, 0],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type='物品',
                                    describtion=None)


# ------------------------------------保险库------------------------------------
class Vault(RoomCard):
    def __init__(self):
        super(Vault, self).__init__(name='保险库',
                                    door=[1, 0, 0, 0],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type='物品',
                                    describtion=None)
        self.trigger = 1
        self.detail = "你可以以'知识'进行'能力挑战'来尝试开启保险库，大于等于6时，开启保险库，抽取2张'物品'"

    def use(self, role):
        if self.trigger == 1:
            print('你决定试试能否开启保险柜门。')
            if sum(role.ability_challenge(ability="知识")) >= 6:
                print('易如反掌！')
                role.items.append(draw_card(type='物品'))
                role.items.append(draw_card(type='物品'))
                self.detail = '保险库空空如也'
                self.trigger = 0
            else:
                print('这太难了！')


# ------------------------------------老朽的门廊------------------------------------
class OldPorch(RoomCard):
    def __init__(self):
        super(OldPorch, self).__init__(name='老朽的门廊',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type=None,
                                       describtion=None)


# ------------------------------------风琴室------------------------------------
class OrganRoom(RoomCard):
    def __init__(self):
        super(OrganRoom, self).__init__(name='风琴室',
                                        door=[0, 0, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='事件',
                                        describtion=None)


# ------------------------------------研究室------------------------------------
class ResearchRoom(RoomCard):
    def __init__(self):
        super(ResearchRoom, self).__init__(name='研究室',
                                           door=[1, 0, 1, 0],
                                           window=[0, 0, 0, 0],
                                           card_img=None,
                                           floor=[1, 1, 1],
                                           item_type='事件',
                                           describtion=None)


# ------------------------------------主人房------------------------------------
class MasterBedRoom(RoomCard):
    def __init__(self):
        super(MasterBedRoom, self).__init__(name='主人房',
                                            door=[1, 0, 0, 1],
                                            window=[0, 0, 2, 0],
                                            card_img=None,
                                            floor=[1, 1, 1],
                                            item_type='预兆',
                                            describtion=None)


# ------------------------------------餐厅------------------------------------
class Restaurant(RoomCard):
    def __init__(self):
        super(Restaurant, self).__init__(name='餐厅',
                                         door=[1, 1, 0, 0],
                                         window=[0, 0, 0, 2],
                                         card_img=None,
                                         floor=[1, 1, 1],
                                         item_type='预兆',
                                         describtion=None)


# ------------------------------------图书馆------------------------------------
class Libry(RoomCard):
    def __init__(self):
        super(Libry, self).__init__(name='图书馆',
                                    door=[0, 0, 1, 1],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type='事件',
                                    describtion=None)

    def stay(self, role):
        print("若在此停留，则你的知识上升1级（每人仅一次）")
        if '图书馆' not in role.buff:
            print('你在此停留，浩瀚的书海让你学到了一些新的知识。')
            role.promote(ability='知识')
            role.buff.append('图书馆')
        else:
            print('显然的，你的提升很有限。')


# ------------------------------------雕塑长廊------------------------------------
class Gallery(RoomCard):
    def __init__(self):
        super(Gallery, self).__init__(name='雕塑长廊',
                                      door=[1, 0, 1, 0],
                                      window=[0, 0, 0, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='事件',
                                      describtion=None)


# ------------------------------------厨房------------------------------------
class Kitchen(RoomCard):
    def __init__(self):
        super(Kitchen, self).__init__(name='厨房',
                                      door=[1, 1, 0, 0],
                                      window=[0, 0, 0, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='预兆',
                                      describtion=None)


# ------------------------------------地窖------------------------------------
class Cellar(RoomCard):
    def __init__(self):
        super(Cellar, self).__init__(name='地窖',
                                     door=[1, 0, 0, 0],
                                     window=[0, 0, 0, 0],
                                     card_img=None,
                                     floor=[1, 1, 1],
                                     item_type='事件',
                                     describtion=None)

    def stay(self, role):
        print("若在此停留，则受到1点精神伤害。")
        role.hurt(type='精神', value=1)


# ------------------------------------阁楼------------------------------------
class Loft(RoomCard):
    def __init__(self):
        super(Loft, self).__init__(name='阁楼',
                                   door=[0, 0, 1, 0],
                                   window=[0, 0, 0, 0],
                                   card_img=None,
                                   floor=[1, 1, 1],
                                   item_type='事件',
                                   describtion=None)

    def leave(self, role):
        print("离开房间时，需要以'速度'进行'能力考验'，骰数大于3，则无恙；否则'力量'下降1级，无论成功与否，人物都能离开房间。")
        print('当你准备离开这个房间时，你发现这里地板滋滋作响，或许需要一点灵活的技巧。')
        if sum(role.ability_challenge(ability="速度")) >= 3:
            print('这很轻松，你轻盈的踩在木板上离开了房间。')
        else:
            print('这对你来说有点吃力，你差点掉落下去，费力抱着木板才让你走回门口，这让你虚弱不少。')
            role.reduce(ability='力量')


# ------------------------------------礼拜堂------------------------------------
class Church(RoomCard):
    def __init__(self):
        super(Church, self).__init__(name='礼拜堂',
                                     door=[1, 0, 0, 0],
                                     window=[0, 0, 5, 0],
                                     card_img=None,
                                     floor=[1, 1, 1],
                                     item_type='事件',
                                     describtion=None)

    def stay(self, role):
        print("若在此停留，则你的意志上升1级（每人仅一次）")
        if '礼拜堂' not in role.buff:
            print('你在此停留，圣洁的气氛让你精神为之一振。')
            role.promote(ability='意志')
            role.buff.append('礼拜堂')
        else:
            print('显然的，同样的风景并没有给你更多感受。')


# ------------------------------------寝室------------------------------------
class BedRoom(RoomCard):
    def __init__(self):
        super(BedRoom, self).__init__(name='寝室',
                                      door=[0, 1, 0, 1],
                                      window=[0, 0, 1, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='事件',
                                      describtion=None)


# ------------------------------------露台------------------------------------
class Terrace(RoomCard):
    def __init__(self):
        super(Terrace, self).__init__(name='露台',
                                      door=[1, 0, 1, 0],
                                      window=[0, 0, 0, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='预兆',
                                      describtion=None)


# ------------------------------------墓园------------------------------------
class Graveyard(RoomCard):
    def __init__(self):
        super(Graveyard, self).__init__(name='墓园',
                                        door=[0, 0, 1, 0],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='事件',
                                        describtion=None)

    def leave(self, role):
        print("离开房间时，需要以'意志'进行'能力考验'，骰数大于4，则无恙；否则'知识'下降1级，无论成功与否，人物都能离开房间。")
        print('这个地方太诡异了，你打算快点离开。')
        if sum(role.ability_challenge(ability="意志")) >= 3:
            print('对，什么也没有，什么也没发生，很好，很好。')
        else:
            print('什么也没有，等等，那是什么？不，我不想看，我要离开，不要追我，啊。')
            role.reduce(ability='知识')


# ------------------------------------手术室------------------------------------
class OperationRoom(RoomCard):
    def __init__(self):
        super(OperationRoom, self).__init__(name='手术室',
                                            door=[0, 1, 1, 0],
                                            window=[0, 0, 0, 0],
                                            card_img=None,
                                            floor=[1, 1, 1],
                                            item_type='事件',
                                            describtion=None)


# ------------------------------------地下湖------------------------------------
class Lake(RoomCard):
    def __init__(self):
        super(Lake, self).__init__(name='地下湖',
                                   door=[1, 1, 0, 0],
                                   window=[0, 0, 0, 0],
                                   card_img=None,
                                   floor=[1, 1, 1],
                                   item_type='事件',
                                   describtion=None)
        self.force = True

    def into(self, role, direction=None):
        super(Lake, self).into(role)
        if self.force:
            print("进入时直接落入湖水中，随机落到地下空白位置")
            print('你一脚踩空，下落到一片冰冷的湖水中')
            role.floor = 0
            while True:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                if game_map[0].map[x][y] is None:
                    set_room(self, 0, x, y)
                    break
            role.room = self
        self.force = False


# ------------------------------------沾血的房间------------------------------------
class BloodRoom(RoomCard):
    def __init__(self):
        super(BloodRoom, self).__init__(name='沾血的房间',
                                        door=[1, 1, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='物品',
                                        describtion=None)


# ------------------------------------佣人房------------------------------------
class MaidRoom(RoomCard):
    def __init__(self):
        super(MaidRoom, self).__init__(name='佣人房',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type='预兆',
                                       describtion=None)


# ------------------------------------楼座------------------------------------
class Balcony(RoomCard):
    def __init__(self):
        super(Balcony, self).__init__(name='楼座',
                                      door=[0, 1, 0, 1],
                                      window=[0, 0, 0, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='预兆',
                                      describtion=None)
        self.detail = "如果'舞厅'已放置，则可以选择从这里跳至'舞厅'，骰1作为肉体伤害"

    def use(self, role):
        if ballroom in room_card_set:
            pass
        else:
            role.hurt(type='肉体')


# ------------------------------------游戏室------------------------------------
class GameRoom(RoomCard):
    def __init__(self):
        super(GameRoom, self).__init__(name='游戏室',
                                       door=[1, 1, 1, 0],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type='事件',
                                       describtion=None)


# ------------------------------------熏黑的房间------------------------------------
class BlackRoom(RoomCard):
    def __init__(self):
        super(BlackRoom, self).__init__(name='熏黑的房间',
                                        door=[1, 1, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='预兆',
                                        describtion=None)


# ------------------------------------尘封的门廊------------------------------------
class Porch(RoomCard):
    def __init__(self):
        super(Porch, self).__init__(name='尘封的门廊',
                                    door=[1, 1, 1, 1],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type=None,
                                    describtion=None)


# ------------------------------------地下楼梯------------------------------------
class Staircase(RoomCard):
    def __init__(self):
        super(Staircase, self).__init__(name='地下楼梯',
                                        door=[0, 0, 1, 0],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 0, 0],
                                        item_type=None,
                                        describtion=None)

    def use(self, role):
        print("地下楼梯永远连接到门厅")
        role.floor = 1
        self.leave(role)
        lobby_0.into(role)


# ------------------------------------五芒星阵------------------------------------
class Pentacle(RoomCard):
    def __init__(self):
        super(Pentacle, self).__init__(name='五芒星阵',
                                       door=[0, 1, 0, 0],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type='预兆',
                                       describtion=None)

    def leave(self, role):
        print("离开房间时，需要以'知识'进行'能力考验'，骰数大于4，则无恙；否则'意志'下降1级，无论成功与否，人物都能离开房间。")
        print('诡异的五芒星阵，似乎隐隐有点微光。')
        if sum(role.ability_challenge(ability="知识")) >= 4:
            print('你充分了解这个符号的意义，这并没有对你造成什么影响。')
        else:
            print('诡异的气氛让你受了不小的刺激。')
            role.reduce(ability='意志')


# ------------------------------------荒废的房间------------------------------------
class WasteRoom(RoomCard):
    def __init__(self):
        super(WasteRoom, self).__init__(name='荒废的房间',
                                        door=[1, 1, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='预兆',
                                        describtion=None)


# ------------------------------------天井------------------------------------
class Yard(RoomCard):
    def __init__(self):
        super(Yard, self).__init__(name='天井',
                                   door=[1, 0, 1, 1],
                                   window=[0, 0, 0, 0],
                                   card_img=None,
                                   floor=[1, 1, 1],
                                   item_type='事件',
                                   describtion=None)


# ------------------------------------庭院------------------------------------
class Courtyard(RoomCard):
    def __init__(self):
        super(Courtyard, self).__init__(name='庭院',
                                        door=[1, 0, 1, 0],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='事件',
                                        describtion=None)


# ------------------------------------暖炉房------------------------------------
class StoveRoom(RoomCard):
    def __init__(self):
        super(StoveRoom, self).__init__(name='暖炉房',
                                        door=[1, 1, 0, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='预兆',
                                        describtion=None)

    def stay(self, role):
        print("若在此停留，则受到1点肉体伤害。")
        role.hurt(type='肉体', value=1)


# ------------------------------------食品储藏室------------------------------------
class FoodStoreroom(RoomCard):
    def __init__(self):
        super(FoodStoreroom, self).__init__(name='食品储藏室',
                                            door=[1, 0, 1, 0],
                                            window=[0, 0, 0, 0],
                                            card_img=None,
                                            floor=[1, 1, 1],
                                            item_type='物品',
                                            describtion=None)

    def stay(self, role):
        print("若在此停留，则你的力量上升1级（每人仅一次）")
        if '食品储藏室' not in role.buff:
            print('试吃了一些这里的食物，让你觉得自己力量提升了。')
            role.promote(ability='力量')
            role.buff.append('食品储藏室')
        else:
            print('显然的，你的提升很有限。')


# ------------------------------------温室------------------------------------
class Greenhouse(RoomCard):
    def __init__(self):
        super(Greenhouse, self).__init__(name='温室',
                                         door=[1, 0, 0, 0],
                                         window=[0, 0, 0, 0],
                                         card_img=None,
                                         floor=[1, 1, 1],
                                         item_type='事件',
                                         describtion=None)


# ------------------------------------健身房------------------------------------
class Gym(RoomCard):
    def __init__(self):
        super(Gym, self).__init__(name='健身房',
                                  door=[0, 1, 1, 0],
                                  window=[0, 0, 0, 0],
                                  card_img=None,
                                  floor=[1, 1, 1],
                                  item_type='预兆',
                                  describtion=None)

    def stay(self, role):
        print("若在此停留，则你的速度上升1级（每人仅一次）")
        if '健身房' not in role.buff:
            print('经过锻炼，你的速度提升了。')
            role.promote(ability='速度')
            role.buff.append('健身房')
        else:
            print('显然的，你的提升很有限。')


# ------------------------------------塔楼------------------------------------
class Tower(PartitionRoom):
    def __init__(self):
        super(Tower, self).__init__(name='塔楼',
                                    door=[0, 1, 0, 1],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type='预兆',
                                    describtion=None)

    def challenge(self, role):
        print("若要从这里通过，需要以'力量'进行'能力挑战'，骰数大于等于3，则成功；否则停止移动。")
        print('破碎的石材阻挡了你的去路，看来需要费点力气移动石头才能前进。')
        if sum(role.ability_challenge(ability='力量')) >= 3:
            print('这对你来说不是难事。')
            if role in self.creatures[0]:
                self.creatures[0].remove(role)
                self.creatures[1].append(role)
            elif role in self.creatures[1]:
                self.creatures[1].remove(role)
                self.creatures[0].append(role)
            return True
        else:
            print('太沉了，看来你只能停下另找他路')
            return False


# ------------------------------------裂缝------------------------------------
class Crack(PartitionRoom):
    def __init__(self):
        super(Crack, self).__init__(name='裂缝',
                                    door=[0, 1, 0, 1],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type=None,
                                    describtion=None)

    def challenge(self, role):
        super(Crack, self).challenge(role)
        print("若要从这里通过，需要以'速度'进行'能力挑战'，骰数大于等于3，则成功；否则停止移动。")
        print('破碎的索桥摇摇晃晃，要通过这里，可能需要一些速度的技巧')
        if sum(role.ability_challenge(ability="速度")) >= 3:
            print('这对你来说不是难事。')
            if role in self.creatures[0]:
                self.creatures[0].remove(role)
                self.creatures[1].append(role)
            elif role in self.creatures[1]:
                self.creatures[1].remove(role)
                self.creatures[0].append(role)
            return True
        else:
            print('你差点一脚踩空，看来，你只能停下另寻他路了')
            return False


# ------------------------------------陵墓------------------------------------
class Mausoleum(PartitionRoom):
    def __init__(self):
        super(Mausoleum, self).__init__(name='陵墓',
                                        door=[1, 0, 1, 0],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='预兆',
                                        describtion=None)

    def challenge(self, role):
        print("若要从这里通过，需要以'意志'进行'能力挑战'，骰数大于等于6，则成功；否则停止移动。")
        if sum(role.ability_challenge(ability="意志")) >= 6:
            print('你克服了自身的恐惧！')
            if role in self.creatures[0]:
                self.creatures[0].remove(role)
                self.creatures[1].append(role)
            elif role in self.creatures[1]:
                self.creatures[1].remove(role)
                self.creatures[0].append(role)
            return True
        else:
            print('你的双腿不受自己的控制，无法行动')
            return False


# ------------------------------------升降梯------------------------------------
class Elevator(RoomCard):
    def __init__(self):
        super(Elevator, self).__init__(name='升降梯',
                                       door=[1, 0, 0, 0],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type=None,
                                       describtion=None)

    def into(self, role, direction=None):
        super(Elevator, self).into(role)
        print("一进入升降梯会立即移动，骰2决定去处：4-任意位置，3-楼上，2-地面，1-地下，0-房间内全部人骰1肉体伤害")
        print('当你一脚踏进这个房间时，这个房间自己开始动了起来.')
        res = role.dice(n=2)
        if sum(res) == 4:
            print('似乎你能控制这个设备，停在哪？')
            while True:
                floor = int(input('floor:'))
                x = int(input('x:'))
                y = int(input('y:'))
                if 0 <= floor <= 2 and 0 <= x < 5 and 0 <= y < 5:
                    new_room = game_map[floor].map[x][y]
                    if new_room is None:
                        game_map[floor].map[x][y] = self
                        break
                    else:
                        print("格子被占用")
                else:
                    print("数值异常")
        elif sum(res) == 3:
            print('房间移动了')
            while True:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                new_room = game_map[2].map[x][y]
                if new_room is None:
                    game_map[2].map[x][y] = self
                    break
        elif sum(res) == 2:
            print('房间移动了')
            while True:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                new_room = game_map[1].map[x][y]
                if new_room is None:
                    game_map[1].map[x][y] = self
                    break
        elif sum(res) == 1:
            print('房间移动了')
            while True:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                new_room = game_map[0].map[x][y]
                if new_room is None:
                    game_map[0].map[x][y] = self
                    break
        else:
            print('房间剧烈震动，房间内的人物受伤了')


# ——————————————————————————————————————————————————————
collapse = Collapse()
chute = Chute()
ballroom = Ballroom()
broken = Broken()
wine = Wine()
store = Store()
vault = Vault()
old_porch = OldPorch()
organ_room = OrganRoom()
research_room = ResearchRoom()
master_bedroom = MasterBedRoom()
restaurant = Restaurant()
libry = Libry()
gallery = Gallery()
kitchen = Kitchen()
cellar = Cellar()
loft = Loft()
church = Church()
bedroom = BedRoom()
terrace = Terrace()
graveyard = Graveyard()
operation_room = OperationRoom()
lake = Lake()
blood_room = BloodRoom()
maid_room = MaidRoom()
balcony = Balcony()
game_room = GameRoom()
black_room = BlackRoom()
porch = Porch()
staircase = Staircase()
pentacle = Pentacle()
waste_room = WasteRoom()
yard = Yard()
courtyard = Courtyard()
stove_room = StoveRoom()
food_storeroom = FoodStoreroom()
greenroom = Greenhouse()
gym = Gym()
tower = Tower()
crack = Crack()
mausoleum = Mausoleum()
elevator = Elevator()


def room_init():
    room_card_set.append(collapse)
    room_card_set.append(chute)
    room_card_set.append(ballroom)
    room_card_set.append(broken)
    room_card_set.append(wine)
    room_card_set.append(store)
    room_card_set.append(vault)
    room_card_set.append(old_porch)
    room_card_set.append(organ_room)
    room_card_set.append(research_room)
    room_card_set.append(master_bedroom)
    room_card_set.append(restaurant)
    room_card_set.append(libry)
    room_card_set.append(gallery)
    room_card_set.append(kitchen)
    room_card_set.append(cellar)
    room_card_set.append(loft)
    room_card_set.append(church)
    room_card_set.append(bedroom)
    room_card_set.append(terrace)
    room_card_set.append(graveyard)
    room_card_set.append(operation_room)
    room_card_set.append(lake)
    room_card_set.append(blood_room)
    room_card_set.append(maid_room)
    room_card_set.append(balcony)
    room_card_set.append(game_room)
    room_card_set.append(black_room)
    room_card_set.append(porch)
    room_card_set.append(staircase)
    room_card_set.append(pentacle)
    room_card_set.append(waste_room)
    room_card_set.append(yard)
    room_card_set.append(courtyard)
    room_card_set.append(stove_room)
    room_card_set.append(food_storeroom)
    room_card_set.append(greenroom)
    room_card_set.append(gym)
    room_card_set.append(tower)
    room_card_set.append(crack)
    room_card_set.append(mausoleum)
    room_card_set.append(elevator)
    # 打乱
    random.shuffle(room_card_set)


# 地图初始化
underground = Map(floor=0)
game_map.append(underground)
ground = Map(floor=1)
game_map.append(ground)
overground = Map(floor=2)
game_map.append(overground)
underground.map[4][4] = down_steps
set_room(down_steps, 0, 4, 4)
set_room(staircase_0, 1, 4, 7)
set_room(lobby_1, 1, 4, 8)
set_room(lobby_0, 1, 4, 9)
set_room(up_steps, 2, 4, 4)
