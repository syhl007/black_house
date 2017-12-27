import constant
from card import *
from util import *


class Main:
    def __init__(self):
        self.event_dict = {}
        self.role_list = []
        self.map_init()
        self.event_init()
        self.room_init()

    # 地图层初始化
    def map_init(self):
        self.map = [Map(floor=0), Map(floor=1), Map(floor=2)]
        self.map[1].map[2][2].set_link(link=Link(start=self.map[1].map[2][2], end=self.map[0].map[2][2]))
        self.map[0].map[2][2].set_link(link=Link(start=self.map[0].map[2][2], end=self.map[1].map[2][2]))

    # 事件初始化
    def event_init(self):
        from types import MethodType  # 动态绑定方法
        event = RoomEvent(detail=constant.strings.get('崩塌的房间'), trigger=0, force=True)

        def do(self, role):
            if self.force:
                print('你尝试通过这个房间.')
                if ability_challenge(role, ability='速度', goal=5):
                    print('你成功通过了这个房间')
                    self.force = False
                else:
                    print('失败')
                    hurt(role, type='肉体')
                    self.force = False

        event.do = MethodType(do, event)
        self.event_dict['崩塌的房间'] = event
        event = RoomEvent(detail=constant.strings.get('煤导槽'), trigger=0, force=True)

        def do(self, role):
            if self.force:
                print('你一脚踩空，掉了下去')
                role.floor = 0
                role.x = 2
                role.y = 2
                hurt(role, type='肉体')
                self.force = False

        event.do = MethodType(do, event)
        self.event_dict['煤导槽'] = event
        event = RoomEvent(detail=constant.strings.get('礼拜堂'), trigger=0, force=True)

        def do(self, role):
            pass

        event.do = MethodType(do, event)
        self.event_dict['礼拜堂'] = event

    # 房间卡初始化
    def room_init(self):
        room_set = []
        room_set.append(HouseCard(name='崩塌的房间', door=[1, 1, 1, 1], window=[0, 0, 0, 0],
                                  card_img=None,
                                  floor=[1, 1, 1],
                                  item_type=None,
                                  event=self.event_dict['崩塌的房间']))
        coal_chute = HouseCard(name='煤导槽', door=[1, 1, 1, 1], window=[0, 0, 0, 0],
                               card_img=None,
                               floor=[0, 1, 1],
                               item_type=None,
                               event=self.event_dict['煤导槽'])
        coal_chute.set_link(link=Link(start=coal_chute, end=self.map[0].map[2][2], one_way=True))
        room_set.append(coal_chute)
        room_set.append(HouseCard(name='礼拜堂', door=[0, 1, 0, 1], window=[0, 0, 1, 0],
                                  card_img=None,
                                  floor=[1, 0, 1],
                                  item_type='事件',
                                  event=self.event_dict['礼拜堂']))
        # room_set.append(HouseCard(name='舞厅', door=[1, 1, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 1, 1],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name='破烂的房间', door=[1, 1, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 1, 0],
        #                      item_type='预兆',
        #                      event=Event(
        #                          detail=constant.strings.get('破烂的房间'),
        #                          check=constant.events.get('破烂的房间'),
        #                          force=True, trigger=2)))
        # room_set.append(HouseCard(name='酒窖', door=[1, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 0, 1],
        #                      item_type='物品',
        #                      event=None))
        # room_set.append(HouseCard(name='酒窖', door=[1, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 0, 1],
        #                      item_type='物品',
        #                      event=None))
        # room_set.append(HouseCard(name='储藏室', door=[1, 0, 0, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 0, 0],
        #                      item_type='物品',
        #                      event=None))
        # room_set.append(HouseCard(name='保险库', door=[1, 0, 0, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 1, 1],
        #                      item_type='事件',
        #                      event=Event(
        #                          detail=constant.strings.get('保险库'),
        #                          check=constant.events.get('保险库'),
        #                          force=False, trigger=1)))
        # room_set.append(HouseCard(name='老朽的门廊', door=[1, 1, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 1, 1],
        #                      item_type=None,
        #                      event=None))
        # room_set.append(HouseCard(name='风琴室', door=[0, 0, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 0, 0],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name='研究室', door=[1, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 1, 0],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name='主卧室', door=[1, 0, 0, 1], window=[0, 0, 2, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='预兆',
        #                      event=None))
        # room_set.append(HouseCard(name='餐厅', door=[1, 1, 0, 0], window=[0, 0, 0, 2],
        #                      card_img=None,
        #                      floor=[1, 0, 0],
        #                      item_type='预兆',
        #                      event=None))
        # room_set.append(HouseCard(name='图书馆', door=[0, 0, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 1, 1],
        #                      item_type='事件',
        #                      event=Event(
        #                          detail=constant.strings.get('图书馆'),
        #                          check=constant.events.get('图书馆'),
        #                          force=True, trigger=1)))
        # room_set.append(HouseCard(name='雕塑长廊', door=[1, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 0, 1],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name='厨房', door=[1, 1, 0, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 0, 1],
        #                      item_type='预兆',
        #                      event=None))
        # room_set.append(HouseCard(name='陵墓', door=[1, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[1, 1, 1],
        #                      item_type='预兆',
        #                      event=Event(
        #                          detail=constant.strings.get('陵墓'),
        #                          check=constant.events.get('陵墓'),
        #                          force=True, trigger=2)))
        # room_set.append(HouseCard(name='地窖', door=[1, 0, 0, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 1, 0],
        #                      item_type='事件',
        #                      event=Event(
        #                          detail=constant.strings.get('地窖'),
        #                          check=constant.events.get('地窖'),
        #                          force=True, trigger=1)))
        # room_set.append(HouseCard(name='阁楼', door=[0, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='事件',
        #                      event=Event(
        #                          detail=constant.strings.get('阁楼'),
        #                          check=constant.events.get('阁楼'),
        #                          force=True, trigger=2)))
        # room_set.append(HouseCard(name="寝室", door=[1, 0, 0, 0], window=[0, 0, 5, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name="露台", door=[1, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='预兆',
        #                      event=None))
        # room_set.append(HouseCard(name="墓园", door=[0, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='事件',
        #                      event=Event(
        #                          detail=constant.strings.get('墓园'),
        #                          check=constant.events.get('墓园'),
        #                          force=True, trigger=2)))
        # room_set.append(HouseCard(name="手术室", door=[0, 1, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name="地下湖", door=[1, 1, 0, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name="沾血的房间", door=[1, 1, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='物品',
        #                      event=None))
        # room_set.append(HouseCard(name="佣人房", door=[1, 1, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='预兆',
        #                      event=None))
        # room_set.append(HouseCard(name="裂缝", door=[0, 1, 0, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type=None,
        #                      event=Event(
        #                          detail=constant.strings.get('裂缝'),
        #                          check=constant.events.get('裂缝'),
        #                          force=True, trigger=2)))
        # room_set.append(HouseCard(name="楼座", door=[1, 0, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='预兆',
        #                      event=Event(
        #                          detail=constant.strings.get('楼座'),
        #                          check=constant.events.get('楼座'),
        #                          force=False, trigger=1)))
        # room_set.append(HouseCard(name="游戏室", door=[1, 1, 1, 0], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='事件',
        #                      event=None))
        # room_set.append(HouseCard(name="熏黑的房间", door=[1, 1, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='预兆',
        #                      event=None))
        # room_set.append(HouseCard(name="尘封的门廊", door=[1, 1, 1, 1], window=[0, 0, 0, 0],
        #                      card_img=None,
        #                      floor=[0, 0, 1],
        #                      item_type='预兆',
        #                      event=None))
        # ....
        self.room_set = set(room_set)

    # 游戏开始
    def game(self):
        test = Role(name='test', san=5, power=5, know=5, speed=2)
        test.floor = 1
        test.x = 2
        test.y = 4
        self.role_list.append(test)
        while True:
            for r in self.role_list:
                direction = None
                string = input("输入行动: ")
                if string == "移动-经过":
                    direction = int(input("决定方向: "))
                new_room = action(role=r, act=string, direction=direction, room_set=self.room_set, map=self.map[r.floor].map)
                if new_room is not None and isinstance(new_room, HouseCard):
                    print('新房间是：', new_room.name)
                    while True:
                        rotate = int(input("旋转房间卡完成放置: "))
                        if set_room(role=r, new_room=new_room, direction=1, rotate=rotate, map=self.map[r.floor].map):
                            break


m = Main()
m.game()
pass
