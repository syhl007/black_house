from card import *
from constant import role_list
from event_card import event_init
from omen_card import omen_init
from room_card import lobby_0, room_init, lobby_1, staircase_0
from util import *


class Main:
    def __init__(self):
        room_init()
        omen_init()
        event_init()

    # 游戏开始
    def game(self):
        bj = Role(name='Brandon Jaspers',
                  san=5, san_strip=[0, 3, 3, 3, 4, 5, 6, 7, 8],
                  power=5, power_strip=[0, 2, 3, 3, 4, 5, 6, 6, 7],
                  know=5, know_strip=[0, 1, 3, 3, 5, 6, 6, 7],
                  speed=2, speed_strip=[0, 3, 4, 4, 4, 5, 6, 7, 8])
        role_list.append(bj)
        lobby_0.into(bj)
        emey = Role(name='你的死敌',
                  san=5, san_strip=[0, 3, 3, 3, 4, 5, 6, 7, 8],
                  power=5, power_strip=[0, 2, 3, 3, 4, 5, 6, 6, 7],
                  know=5, know_strip=[0, 1, 3, 3, 5, 6, 6, 7],
                  speed=5, speed_strip=[0, 3, 4, 4, 4, 5, 6, 7, 8])
        emey.camp = -999
        lobby_0.into(emey)
        lobby_1.into(emey)
        staircase_0.into(emey)
        print(dog_check(bj.room.x,bj.room.y,bj.floor))
        print("基本操作：i、查看物品|o、查看预兆列表|b、查看buff|f、房屋互动")
        while True:
            try:
                if bj.move_bar > 0:
                    print("请选择行动：1、移动|2、休息")
                else:
                    print("请选择行动：2、休息")
                inp = user_input()
                # 移动&休息
                if inp == "1":
                    dir_str = ""
                    if bj.room.door[0] >= 1:
                        dir_str += "0-↑|"
                    if bj.room.door[1] >= 1:
                        dir_str += "1-→|"
                    if bj.room.door[2] >= 1:
                        dir_str += "2-↓|"
                    if bj.room.door[3] >= 1:
                        dir_str += "3-←|"
                    print("方向：", dir_str)
                    try:
                        bj.move(direction=int(user_input()))
                    except:
                        continue
                elif inp == "2":
                    bj.rest()
                if inp == "r":
                    print("[所在房间]:", bj.room)
                if inp == "i":
                    print("[物品栏]:", bj.get_items_list())
                if inp == "o":
                    print("[预兆栏]:", bj.get_omens_list())
                if inp == "b":
                    print("[buff]:", bj.get_buff_list())
                if inp == "a":  # 袭击
                    l = bj.get_weapon_list()
                    print(l)
                    index = int(user_input())
                    arms = l[index]
                    l = [r for r in bj.room.get_creatures(bj) if r != bj]
                    print(l)
                    index = int(user_input())
                    tar = l[index]
                    print(tar)
                    bj.attack(target=tar, arms=arms)
                if inp == "f":
                    bj.room.use(role=bj)
            except Exception as e:
                print(e.args)
                # continue
                raise e


m = Main()
m.game()
pass
