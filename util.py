from constant import game_map, item_card_set, event_card_set, game_schedule

# 玩家输入
from item_card import gun
from omen_card import omen_card_set


def user_input(*args, **kwargs):
    return input("请输入：")


# 顺时针旋转
def ahead_one(l):
    x = l.pop(len(l) - 1)
    l.insert(0, x)
    return l


# 逆时针旋转
def backward_one(l):
    x = l.pop(0)
    l.append(x)
    return l


# 揭示真相
def haunt_roll(role):
    if game_schedule < 1:
        res = (13 - len(omen_card_set)) - sum(role.dice(n=999))
        if res < 0:
            return True
        else:
            return False


# 枪械远程袭击
def gun_check(x, y, floor, direction=None, ):
    l = []
    room = game_map[floor].map[x][y]
    if room is None:
        return list
    if direction is None:
        for d in range(4):
            if room.door[d] == 0:
                continue
            else:
                try:
                    new_x = x + [0, 1, 0, -1][d]
                    new_y = y + [-1, 0, 1, 0][d]
                    new_room = game_map[floor].map[new_x][new_y]
                    if new_room.door[[2, 3, 0, 1][d]] == 0:
                        continue
                    else:
                        l += gun_check(new_x, new_y, floor, direction=d)
                except Exception:
                    continue
        return l
    else:
        l += room.get_creatures()
        try:
            new_x = x + [0, 1, 0, -1][direction]
            new_y = y + [-1, 0, 1, 0][direction]
            new_room = game_map[floor].map[new_x][new_y]
            if new_room.door[[2, 3, 0, 1][direction]] == 0:
                return l
            else:
                return l + gun_check(new_x, new_y, floor, direction=direction)
        except Exception:
            return l


# 脏狗判断
def dog_check(x, y, floor, n=6, direction=None):
    l = []
    room = game_map[floor].map[x][y]
    l.append(room)
    directions = [0, 1, 2, 3]
    if direction is not None:
        directions.remove([2, 3, 0, 1][direction])
    for d in directions:
        if room.door[d] == 0:
            continue
        else:
            try:
                new_x = x + [0, 1, 0, -1][d]
                new_y = y + [-1, 0, 1, 0][d]
                new_room = game_map[floor].map[new_x][new_y]
                if new_room.door[[2, 3, 0, 1][d]] == 0:
                    continue
                else:
                    n -= 1
                    if n < 0:
                        return l
                    else:
                        return l + dog_check(new_x, new_y, floor, n=n, direction=d)
            except Exception:
                continue
    return l


# 袭击
def attack(attacker):
    l = attacker.get_weapon_list()
    print(l)
    index = int(user_input())
    arms = l[index]
    l = [r for r in attacker.room.get_creatures(attacker) if r != attacker]
    if arms == gun:
        l2 = gun_check
        print(l2)
    index = int(user_input())
    tar = l[index]
    print(tar)
    None.attack(target=tar, arms=arms)


# 抽卡
def draw_card(type):
    if type == '物品':
        s = item_card_set
    elif type == '预兆':
        s = omen_card_set
    elif type == '事件':
        s = event_card_set
    else:
        s = event_card_set
    return s.pop()


# 设置房间卡
def set_room(room, floor, x, y):
    game_map[floor].map[x][y] = room
    room.x = x
    room.y = y


# 遍历地图版
def room_search(names=None, sign=None, floor=None):
    room_list = []
    if floor is None:
        floor = range(3)
    else:
        floor = [floor]
    for i in floor:
        for x in range(len(game_map[i].map)):
            for y in range(len(game_map[i].map[x])):
                room = game_map[i].map[x][y]
                if room is None:
                    continue
                if names is None and sign is None:
                    room_list.append({'x': x, 'y': y, 'floor': floor, 'room': room})
                else:
                    if names is not None:
                        if room.name in names:
                            room_list.append({'x': x, 'y': y, 'floor': floor, 'room': room})
                    if sign is not None:
                        if sign in room.sign:
                            room_list.append({'x': x, 'y': y, 'floor': floor, 'room': room})
    return room_list


# 地图版‘气’判断
def live_map_cheak(floor=None):
    count = 0
    map = game_map[floor].map
    for x in range(len(map)):
        for y in range(len(map[x])):
            room = map[x][y]
            if room is None:
                continue
            for i in range(4):
                if room.door[i] == 0:
                    continue
                try:
                    next_room = map[x + [0, 1, 0, -1][i]][y + [-1, 0, 1, 0][i]]
                except:
                    continue
                if next_room is None:
                    count += 1
    return count
    pass

