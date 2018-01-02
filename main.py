from card import *
from room_card import lobby_0
from util import *


class Main:
    def __init__(self):
        pass

    # 游戏开始
    def game(self):
        bj = Role(name='Brandon Jaspers',
                  san=5, san_strip=[0, 3, 3, 3, 4, 5, 6, 7, 8],
                  power=5, power_strip=[0, 2, 3, 3, 4, 5, 6, 6, 7],
                  know=5, know_strip=[0, 1, 3, 3, 5, 6, 6, 7],
                  speed=2, speed_strip=[0, 3, 4, 4, 4, 5, 6, 7, 8])
        bj.room=lobby_0
        while True:
            if bj.move_bar >= 0:
                print("请选择行动：1、移动|2、休息")
            else:
                print("请选择行动：2、休息")
            inp = user_input()
            if int(inp) == 1:
                print("方向：0-↑|1-→|2-↓|3-←")
                bj.move(direction=int(user_input()))



m = Main()
m.game()
pass
