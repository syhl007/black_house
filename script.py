import random

import constant
from monsters import Mummy
import pandas as pd

from omen_card import girl
from util import dog_check, room_search

room_index = ["荒废的房间", "露台", "陵墓", "熏黑的房间", "餐厅", "暖炉房", "楼座", "健身房", "破烂的房间", "厨房", "主人房", "五芒星阵", "佣人房"]
omen_columns = ["噬咬", "书本", "水晶球", "脏狗", "女孩", "圣符", "疯汉", "面具", "徽章", "指环", "颅骨", "长矛", "灵板"]
truth_table = pd.DataFrame([[18, 7, 12, 38, 1, 9, 45, 42, 49, 28, 34, 43, 48],
                            [24, 7, 32, 5, 16, 6, 11, 25, 49, 20, 47, 39, 2],
                            [4, 7, 23, 46, 1, 13, 10, 25, 49, 41, 37, 43, 48],
                            [24, 33, 23, 38, 30, 13, 31, 48, 44, 20, 47, 15, 8],
                            [24, 3, 27, 5, 16, 6, 45, 42, 21, 20, 37, 39, 40],
                            [4, 33, 32, 38, 30, 13, 10, 42, 36, 28, 34, 15, 2],
                            [18, 3, 19, 19, 19, 22, 10, 25, 36, 41, 37, 15, 8],
                            [35, 29, 12, 46, 1, 22, 11, 22, 21, 41, 47, 43, 48],
                            [4, 33, 27, 46, 1, 9, 11, 25, 44, 17, 17, 17, 40],
                            [18, 3, 23, 46, 16, 22, 31, 32, 36, 41, 37, 39, 2],
                            [35, 29, 27, 5, 16, 6, 10, 35, 44, 20, 47, 43, 2],
                            [26, 50, 32, 50, 26, 26, 45, 14, 14, 26, 14, 50, 40],
                            [35, 29, 12, 5, 30, 9, 31, 42, 21, 28, 34, 15, 8], ],
                           columns=omen_columns, index=room_index)


# 真相表
def get_truth(role, omen):
    num = truth_table[omen.name][role.room.name]
    if num >= 0:
        role.room.sign.append("石棺")
        mummy = Mummy(floor=role.floor, room=role.room)
        role.room.into(mummy)
        constant.role_list.append(mummy)
        if girl not in role.omens:
            role.gain_obj(girl)
        role.lost_obj(girl)
        all_list = room_search(floor=role.floor)
        n = 6
        while True:
            extra_list = dog_check(x=role.room.x, y=role.room.y, floor=role.floor, n=n)
            if len(all_list) > len(extra_list):
                room_list = [room for room in all_list if room.get("room") not in extra_list]
                break
            else:
                n -= 1
        random.shuffle(room_list)
        room = room_list.pop().get("room")
        room.omens.append(girl)
        print("女孩逃到了", room.name)
        pass
