import random

from card import HouseCard
from constant import game_map
from util import draw_card, challenge, dice

# 房间卡堆
room_card_set = []


# ------------------------------------崩塌的房间------------------------------------
class Collapse(HouseCard):
    def __init__(self):
        super(Collapse, self).__init__(name='崩塌的房间',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type=None,
                                       describtion=None)

    def into(self, role):
        super(Collapse, self).into(role)
        print("第一个进入本房间的玩家必须以'速度'进行'能力考验'。若骰数大于或等于5，则人物无恙。否则翻开一张地下室卡，放到地下，玩家坠落至此，并需要骰1，点数为玩家'肉体伤害'")
        if self.force:
            print('当你一脚踏进这个房间时，显然没有注意到地板上的破洞.')
            if challenge(role, ability='速度', goal=5):
                print('但是你灵巧的稳住了身形，避免了掉落')
            else:
                print('你一脚踩空，下落到地下室随机地点')
                role.hurt(type='肉体')
                role.floor = 0
                role.x = random.randint(0, 4)
                role.y = random.randint(0, 4)
                if game_map[0].map[role.x][role.y] is None:
                    new_room = role.explore()
                    game_map[0].map[role.x][role.y] = new_room
                else:
                    new_room = game_map[0].map[role.x][role.y]
                role.into(new_room)
            self.force = False


collapse = Collapse()
room_card_set.append(collapse)


# ------------------------------------煤导槽-----------------------------------
class Chute(HouseCard):
    def __init__(self):
        super(Chute, self).__init__(name='煤导槽',
                                    door=[1, 0, 0, 0],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type=None,
                                    describtion=None)

    def into(self, role):
        super(Chute, self).into(role)
        if "绳索" in role.items:
            pass
        else:
            print("这是一条单向通向'下台阶'的特殊通道")
            role.floor = 0
            role.x = 2
            role.y = 2

    def use(self, role):
        super(Chute, self).use(role)
        print("这是一条单向通向'下台阶'的特殊通道")
        role.floor = 0
        role.x = 2
        role.y = 2

    def stay(self, role):
        super(Chute, self).stay(role)
        print("这是一条单向通向'下台阶'的特殊通道")
        role.floor = 0
        role.x = 2
        role.y = 2


chute = Chute()
room_card_set.append(chute)


# ------------------------------------舞厅------------------------------------
class Ballroom(HouseCard):
    def __init__(self):
        super(Ballroom, self).__init__(name='舞厅',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type='事件',
                                       describtion=None)


ballroom = Ballroom()
room_card_set.append(ballroom)


# ------------------------------------破烂的房间-----------------------------------
class Broken(HouseCard):
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
        if challenge(role, ability='力量', goal=3):
            print('这很轻松，你在杂物之间分开了一条路。')
        else:
            print('杂物似乎比你想象的重得多，你费了大力气才弄出一条路，为此还弄伤了你的脚（速度减1）')
            role.reduce(ability='速度')


broken = Broken()
room_card_set.append(broken)


# ------------------------------------酒窖------------------------------------
class Wine(HouseCard):
    def __init__(self):
        super(Wine, self).__init__(name='酒窖',
                                   door=[1, 0, 1, 0],
                                   window=[0, 0, 0, 0],
                                   card_img=None,
                                   floor=[1, 1, 1],
                                   item_type='物品',
                                   describtion=None)


wine = Wine()
room_card_set.append(wine)


# ------------------------------------储藏室------------------------------------
class Store(HouseCard):
    def __init__(self):
        super(Store, self).__init__(name='储藏室',
                                    door=[1, 0, 0, 0],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type='物品',
                                    describtion=None)


store = Store()
room_card_set.append(store)


# ------------------------------------保险库------------------------------------
class Vault(HouseCard):
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
            if challenge(role, ability='知识', goal=6):
                print('易如反掌！')
                role.items.append(draw_card(type='物品'))
                role.items.append(draw_card(type='物品'))
                self.detail = '保险库空空如也'
                self.trigger = 0
            else:
                print('这太难了！')


vault = Vault()
room_card_set.append(vault)


# ------------------------------------老朽的门廊------------------------------------
class OldPorch(HouseCard):
    def __init__(self):
        super(OldPorch, self).__init__(name='老朽的门廊',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type=None,
                                       describtion=None)


old_porch = OldPorch()
room_card_set.append(old_porch)


# ------------------------------------风琴室------------------------------------
class OrganRoom(HouseCard):
    def __init__(self):
        super(OrganRoom, self).__init__(name='风琴室',
                                        door=[0, 0, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='事件',
                                        describtion=None)


organ_room = OrganRoom()
room_card_set.append(organ_room)


# ------------------------------------研究室------------------------------------
class ResearchRoom(HouseCard):
    def __init__(self):
        super(ResearchRoom, self).__init__(name='研究室',
                                           door=[1, 0, 1, 0],
                                           window=[0, 0, 0, 0],
                                           card_img=None,
                                           floor=[1, 1, 1],
                                           item_type='事件',
                                           describtion=None)


research_room = ResearchRoom()
room_card_set.append(research_room)


# ------------------------------------主人房------------------------------------
class MasterBedRoom(HouseCard):
    def __init__(self):
        super(MasterBedRoom, self).__init__(name='主人房',
                                            door=[1, 0, 0, 1],
                                            window=[0, 0, 2, 0],
                                            card_img=None,
                                            floor=[1, 1, 1],
                                            item_type='预兆',
                                            describtion=None)


master_bedroom = MasterBedRoom()
room_card_set.append(master_bedroom)


# ------------------------------------餐厅------------------------------------
class Restaurant(HouseCard):
    def __init__(self):
        super(Restaurant, self).__init__(name='餐厅',
                                         door=[1, 1, 0, 0],
                                         window=[0, 0, 0, 2],
                                         card_img=None,
                                         floor=[1, 1, 1],
                                         item_type='预兆',
                                         describtion=None)


restaurant = Restaurant()
room_card_set.append(restaurant)


# ------------------------------------图书馆------------------------------------
class Libry(HouseCard):
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


libry = Libry()
room_card_set.append(libry)


# ------------------------------------雕塑长廊------------------------------------
class Gallery(HouseCard):
    def __init__(self):
        super(Gallery, self).__init__(name='雕塑长廊',
                                      door=[1, 0, 1, 0],
                                      window=[0, 0, 0, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='事件',
                                      describtion=None)


gallery = Gallery()
room_card_set.append(gallery)


# ------------------------------------厨房------------------------------------
class Kitchen(HouseCard):
    def __init__(self):
        super(Kitchen, self).__init__(name='厨房',
                                      door=[1, 1, 0, 0],
                                      window=[0, 0, 0, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='预兆',
                                      describtion=None)


kitchen = Kitchen()
room_card_set.append(kitchen)


# ------------------------------------陵墓------------------------------------
class Mausoleum(HouseCard):
    def __init__(self):
        super(Mausoleum, self).__init__(name='陵墓',
                                        door=[1, 0, 1, 0],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='预兆',
                                        describtion=None)
        self.role = [[], [], [], []]

    def passaway(self, role):
        print("若要从这里通过，需要以'意志'进行'能力挑战'，骰数大于等于6，则成功；否则停止移动。")
        if challenge(role, ability='意志', goal=6):
            print('你克服了自身的恐惧！')
        else:
            print('你的双腿不受自己的控制，无法行动')
            role.move = 0


mausoleum = Mausoleum()
room_card_set.append(mausoleum)


# ------------------------------------地窖------------------------------------
class Cellar(HouseCard):
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
        role.hurt(type='精神')


cellar = Cellar()
room_card_set.append(cellar)


# ------------------------------------阁楼------------------------------------
class Loft(HouseCard):
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
        if challenge(role, ability='速度', goal=3):
            print('这很轻松，你轻盈的踩在木板上离开了房间。')
        else:
            print('这对你来说有点吃力，你差点掉落下去，费力抱着木板才让你走回门口，这让你虚弱不少。')
            role.reduce(ability='力量')


loft = Loft()
room_card_set.append(loft)


# ------------------------------------礼拜堂------------------------------------
class Church(HouseCard):
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


church = Church()
room_card_set.append(church)


# ------------------------------------寝室------------------------------------
class BedRoom(HouseCard):
    def __init__(self):
        super(BedRoom, self).__init__(name='寝室',
                                      door=[0, 1, 0, 1],
                                      window=[0, 0, 1, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='事件',
                                      describtion=None)


bedroom = BedRoom()
room_card_set.append(bedroom)


# ------------------------------------露台------------------------------------
class Terrace(HouseCard):
    def __init__(self):
        super(Terrace, self).__init__(name='露台',
                                      door=[1, 0, 1, 0],
                                      window=[0, 0, 0, 0],
                                      card_img=None,
                                      floor=[1, 1, 1],
                                      item_type='预兆',
                                      describtion=None)


terrace = Terrace()
room_card_set.append(terrace)


# ------------------------------------墓园------------------------------------
class Graveyard(HouseCard):
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
        if challenge(role, ability='意志', goal=3):
            print('对，什么也没有，什么也没发生，很好，很好。')
        else:
            print('什么也没有，等等，那是什么？不，我不想看，我要离开，不要追我，啊。')
            role.reduce(ability='知识')


graveyard = Graveyard()
room_card_set.append(graveyard)


# ------------------------------------手术室------------------------------------
class OperationRoom(HouseCard):
    def __init__(self):
        super(OperationRoom, self).__init__(name='手术室',
                                            door=[0, 1, 1, 0],
                                            window=[0, 0, 0, 0],
                                            card_img=None,
                                            floor=[1, 1, 1],
                                            item_type='事件',
                                            describtion=None)


operation_room = OperationRoom()
room_card_set.append(operation_room)


# ------------------------------------地下湖------------------------------------
class Lake(HouseCard):
    def __init__(self):
        super(Lake, self).__init__(name='地下湖',
                                   door=[1, 1, 0, 0],
                                   window=[0, 0, 0, 0],
                                   card_img=None,
                                   floor=[1, 1, 1],
                                   item_type='事件',
                                   describtion=None)
        self.force = True

    def into(self, role):
        if self.force:
            print("进入时直接落入湖水中，随机落到地下空白位置")
            print('你一脚踩空，下落到一片冰冷的湖水中')
            role.floor = 0
            while True:
                role.x = random.randint(0, 4)
                role.y = random.randint(0, 4)
                if game_map[0].map[role.x][role.y] is None:
                    game_map[0].map[role.x][role.y] = self
                    break
            role.into(self)
        self.force = False


lake = Lake()
room_card_set.append(lake)


# ------------------------------------沾血的房间------------------------------------
class BloodRoom(HouseCard):
    def __init__(self):
        super(BloodRoom, self).__init__(name='沾血的房间',
                                        door=[1, 1, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='物品',
                                        describtion=None)


blood_room = BloodRoom()
room_card_set.append(blood_room)


# ------------------------------------佣人房------------------------------------
class MaidRoom(HouseCard):
    def __init__(self):
        super(MaidRoom, self).__init__(name='佣人房',
                                       door=[1, 1, 1, 1],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type='预兆',
                                       describtion=None)


maid_room = MaidRoom()
room_card_set.append(maid_room)


# ------------------------------------裂缝------------------------------------
class Crack(HouseCard):
    def __init__(self):
        super(Crack, self).__init__(name='裂缝',
                                    door=[0, 1, 0, 1],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type=None,
                                    describtion=None)
        self.role = [[], [], [], []]

    def passaway(self, role):
        print("若要从这里通过，需要以'速度'进行'能力挑战'，骰数大于等于3，则成功；否则停止移动。")
        print('破碎的索桥摇摇晃晃，要通过这里，可能需要一些速度的技巧')
        if challenge(role, ability='速度', goal=3):
            print('这对你来说不是难事。')
        else:
            print('你差点一脚踩空，看来，你只能停下另寻他路了')
            role.move = 0


crack = Crack()
room_card_set.append(crack)


# ------------------------------------楼座------------------------------------
class Balcony(HouseCard):
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
            role.hurt(type='肉体')


balcony = Balcony()
room_card_set.append(balcony)


# ------------------------------------游戏室------------------------------------
class GameRoom(HouseCard):
    def __init__(self):
        super(GameRoom, self).__init__(name='游戏室',
                                       door=[1, 1, 1, 0],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type='事件',
                                       describtion=None)


game_room = GameRoom()
room_card_set.append(game_room)


# ------------------------------------熏黑的房间------------------------------------
class BlackRoom(HouseCard):
    def __init__(self):
        super(BlackRoom, self).__init__(name='熏黑的房间',
                                        door=[1, 1, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='预兆',
                                        describtion=None)


black_room = BlackRoom()
room_card_set.append(black_room)


# ------------------------------------尘封的门廊------------------------------------
class Porch(HouseCard):
    def __init__(self):
        super(Porch, self).__init__(name='尘封的门廊',
                                    door=[1, 1, 1, 1],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type=None,
                                    describtion=None)


porch = Porch()
room_card_set.append(porch)


# ------------------------------------升降梯------------------------------------
class Elevator(HouseCard):
    def __init__(self):
        super(Elevator, self).__init__(name='升降梯',
                                       door=[1, 0, 0, 0],
                                       window=[0, 0, 0, 0],
                                       card_img=None,
                                       floor=[1, 1, 1],
                                       item_type=None,
                                       describtion=None)

    def into(self, role):
        super(Elevator, self).into(role)
        print("一进入升降梯会立即移动，骰2决定去处：4-任意位置，3-楼上，2-地面，1-地下，0-房间内全部人骰1肉体伤害")
        print('当你一脚踏进这个房间时，这个房间自己开始动了起来.')
        res = dice(role=role, n=2)
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


elevator = Elevator()
room_card_set.append(elevator)


# ------------------------------------地下楼梯------------------------------------
class Staircase(HouseCard):
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
        role.x = [2]
        role.y = [2]


staircase = Staircase()
room_card_set.append(staircase)


# ------------------------------------五芒星阵------------------------------------
class Pentacle(HouseCard):
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
        if challenge(role, ability='知识', goal=4):
            print('你充分了解这个符号的意义，这并没有对你造成什么影响。')
        else:
            print('诡异的气氛让你受了不小的刺激。')
            role.reduce(ability='意志')


pentacle = Pentacle()
room_card_set.append(pentacle)


# ------------------------------------塔楼------------------------------------
class Tower(HouseCard):
    def __init__(self):
        super(Tower, self).__init__(name='塔楼',
                                    door=[0, 1, 0, 1],
                                    window=[0, 0, 0, 0],
                                    card_img=None,
                                    floor=[1, 1, 1],
                                    item_type='预兆',
                                    describtion=None)
        self.role = [[], [], [], []]

    def passaway(self, role):
        print("若要从这里通过，需要以'力量'进行'能力挑战'，骰数大于等于3，则成功；否则停止移动。")
        print('破碎的石材阻挡了你的去路，看来需要费点力气移动石头才能前进。')
        if challenge(role, ability='力量', goal=3):
            print('这对你来说不是难事。')
        else:
            print('太沉了，看来你只能停下另找他路')
            role.move = 0


tower = Tower()
room_card_set.append(tower)


# ------------------------------------荒废的房间------------------------------------
class WasteRoom(HouseCard):
    def __init__(self):
        super(WasteRoom, self).__init__(name='荒废的房间',
                                        door=[1, 1, 1, 1],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='预兆',
                                        describtion=None)


waste_room = WasteRoom()
room_card_set.append(waste_room)


# ------------------------------------天井------------------------------------
class Yard(HouseCard):
    def __init__(self):
        super(Yard, self).__init__(name='天井',
                                   door=[1, 0, 1, 1],
                                   window=[0, 0, 0, 0],
                                   card_img=None,
                                   floor=[1, 1, 1],
                                   item_type='事件',
                                   describtion=None)


yard = Yard()
room_card_set.append(yard)


# ------------------------------------庭院------------------------------------
class Courtyard(HouseCard):
    def __init__(self):
        super(Courtyard, self).__init__(name='庭院',
                                        door=[1, 0, 1, 0],
                                        window=[0, 0, 0, 0],
                                        card_img=None,
                                        floor=[1, 1, 1],
                                        item_type='事件',
                                        describtion=None)


courtyard = Courtyard()
room_card_set.append(courtyard)


# ------------------------------------暖炉房------------------------------------
class StoveRoom(HouseCard):
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
        role.hurt(type='肉体')


stove_room = StoveRoom()
room_card_set.append(stove_room)


# ------------------------------------食品储藏室------------------------------------
class FoodStoreroom(HouseCard):
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


food_storeroom = FoodStoreroom()
room_card_set.append(food_storeroom)


# ------------------------------------温室------------------------------------
class Greenhouse(HouseCard):
    def __init__(self):
        super(Greenhouse, self).__init__(name='温室',
                                         door=[1, 0, 0, 0],
                                         window=[0, 0, 0, 0],
                                         card_img=None,
                                         floor=[1, 1, 1],
                                         item_type='事件',
                                         describtion=None)


greenroom = Greenhouse()
room_card_set.append(greenroom)


# ------------------------------------健身房------------------------------------
class Gym(HouseCard):
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


gym = Gym()
room_card_set.append(gym)
# ——————————————————————————————————————————————————————
