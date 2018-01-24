from omen_card import *
from room_card import *
import pandas as pd

room_index = [waste_room, terrace, mausoleum, black_room, restaurant, stove_room, balcony, gym, master_bedroom,
              pentacle, maid_room]
omen_columns = [bite, book, crystal_ball, dog, girl, rune, crazy, mask, badge, ring, skull, spear, spirit_board]
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
    num = truth_table[role.room][omen]
    pass
