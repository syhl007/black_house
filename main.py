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
