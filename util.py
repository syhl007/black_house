import random


# 顺时针旋转
from constant import card_set


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
    room = map[role.x][role.y]
    for i in range(rotate):
        new_room.rotate_room()
    d = [2, 3, 0, 1][direction]
    if new_room.door[d] == 0:
        return False
    else:
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
            map[x][y] = new_room
        except:
            print('设置失败')
            raise Exception()
        role.x = x
        role.y = y
        role.leave(room)
        role.into(new_room)
        return True


# 行动
def action(role, act, room_set, map, direction=None):
    room = map[role.x][role.y]
    if act.startswith("移动"):
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
                next_room = explore(role, room_set)
                return next_room
    elif act == "互动":
        role.use(room)
    elif act == "挑战":
        role.challenge(room)
    elif act == "停留":
        role.stay(room)
        role.recover()




# 抽卡
def draw_card(type):
    s = card_set.get(type)
    return s.pop()