import json
import random

from constant import game_map, item_card_set, event_card_set

# 玩家输入
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


# 设置房间卡
def set_room(role, new_room, direction, rotate, map):
    pass


# 行动
def action(role, act, room_set, map, first=False, direction=None):
    room = map[role.x][role.y]
    if act.startswith("移动"):
        if role.move <= 0 and first:
            role.move = 1
        if role.move <= 0:
            print('行动力不足')
            return
        if room.door[direction] == 0:
            print("没门")
        else:
            if act.endswith('经过'):
                role.passaway(room)
            x = role.x
            y = role.y
            if direction == 0:
                y = role.y - 1
            elif direction == 1:
                x = role.x + 1
            elif direction == 2:
                y = role.y + 1
            elif direction == 3:
                x = role.x - 1
            try:
                next_room = map[x][y]
            except:
                print('移动失败')
                raise Exception()
            role.move -= 1
            if next_room is not None:
                role.x = x
                role.y = y
                role.leave(room)
                role.into(next_room)
            else:
                print('你打开了一扇通向未知区域的门')
                next_room = role.explore(room_set)
                return next_room
    elif act == "互动":
        role.use(room)
    elif act == "挑战":
        role.challenge(room)
    elif act == "停留":
        role.stay(room)
        role.recover()


# 挑战
def challenge(role, ability, goal=0):
    res = role.ability_challenge(ability=ability)


# 偷窃
def steal(winner, loser, item):
    if winner.floor == loser.floor and winner.x == loser.x and winner.y == loser.y and item in loser.items:
        item.lose()
        item.set_owner(winner)
        return True
    else:
        return False


# 袭击
def attack(attacker, retaliator, arms=None):
    if arms is not None and arms not in attacker.items:
        return
    if arms is None:
        a = attacker.combat()
    else:
        a = arms.use()
    ability = a.get('ability')
    b = retaliator.combat(ability=ability)
    res_a = sum(a.get('result'))
    res_b = sum(b.get('result'))
    if res_a > res_b:
        return True
    else:
        return False


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
