import random

from constant import role_list, room_card_set, game_map, item_card_set, event_card_set
from item_card import monkey, magic_box
from room_card import yard, lobby_0, up_steps, stove_room
from util import room_search, draw_card, set_room


class Event:
    pass


# ------------------------------------骇人尖叫------------------------------------
class AHorribleScream(Event):
    def __init__(self):
        self.name = "骇人尖叫"

    def do(self, *args, **kwargs):
        print("屋内原本耳语版的呢喃之声逐渐变成撼动心灵的尖叫")
        for role in role_list:
            res = role.ability_challenge(ability="意志", type="事件")
            if sum(res) >= 4:
                print(role.name, "抵御了这让人心寒的呼喊")
            elif 1 <= sum(res) <= 3:
                print(role.name, "收到骰1点精神伤害")
                role.hurt(type="精神", n=1)
            else:
                print(role.name, "收到骰2点精神伤害")
                role.hurt(type="精神", n=2)


# ------------------------------------丝网------------------------------------
class SilkScreen(Event):
    def __init__(self):
        self.name = "丝网"

    def do(self, *args, **kwargs):
        print("你随手拨开阻挡前行的蛛网，然而这些细丝比你想象的更加强韧，它们黏在你的身上。")
        role = kwargs.get("role")
        res = role.ability_challenge(ability="力量", type="事件")
        if sum(res) >= 4:
            print(role.name, "挣脱了丝网，力量上升1个级别。")
            role.promote(ability='力量')
        else:
            print(role.name, "被丝网缠住了。")
            role.buff.append("丝网3")


# ------------------------------------狂暴本质------------------------------------
class NatureOfFrenzy(Event):
    def __init__(self):
        self.name = "狂暴本质"

    def do(self, *args, **kwargs):
        print("你身边的墙壁开始涌出大量的粘液，向你涌来")
        role = kwargs.get("role")
        res = role.ability_challenge(ability="速度", type="事件")
        if sum(res) >= 5:
            print(role.name, "灵巧的躲开了粘液。")
            role.promote(ability='速度')
        elif 2 <= sum(res) <= 4:
            print(role.name, "躲开了大部分粘液，但少量的粘液仍留在身上，骰1精神伤害。")
            role.hurt(type="精神", n=1)
        elif 0 <= sum(res) <= 1:
            print(role.name, "没能躲开，粘液恶心的附着皮肤，似乎还带着一定的腐蚀性，骰1精神伤害，骰1肉体伤害。")
            role.hurt(type="精神", n=1)
            role.hurt(type="肉体", n=1)


# ------------------------------------希望涌现------------------------------------
class Hope(Event):
    def __init__(self):
        self.name = "希望涌现"

    def do(self, *args, **kwargs):
        print("这个房间充满了圣洁祥和的气息。")
        role = kwargs.get("role")
        role.room.sign.append("祝福")


# ------------------------------------自由的呼唤------------------------------------
class Freedom(Event):
    def __init__(self):
        self.name = "自由的呼唤"

    def do(self, *args, **kwargs):
        print("身处[庭院],[墓园],[塔楼],[露台]的人们脑中突然传来了一个声音。")
        print("“外面！你必须到外面去！自由的飞翔吧！”")
        rooms = room_search(names=["庭院", "墓园", "塔楼", "露台"])
        for room in rooms:
            for role in room.get_creatures():
                if role.camp >= 0:
                    res = role.ability_challenge(ability="意志", type="事件")
                    if sum(res) >= 4:
                        print(role.name, "站在窗台上的瞬间打消了这个愚蠢的念头。")
                    else:
                        print(role.name, "纵身跳了出去，发出如怪鸟一般的叫声，")
                        print(role.name, "一段时间后，在[天井]醒来，骰1肉体伤害")
                        if yard in room_card_set:
                            role.floor = 0
                            while True:
                                x = random.randint(0, 4)
                                y = random.randint(0, 4)
                                if game_map[0].map[x][y] is None:
                                    set_room(yard, role.floor, x, y)
                                    room_card_set.remove(yard)
                                    yard.into(role)
                                    break
                        else:
                            x = 0
                            y = 0
                            for i in range(len(game_map[0].map)):
                                x = i
                                for room in game_map[0].map[x]:
                                    if room == yard:
                                        break
                                    y += 1
                            role.x = x
                            role.y = y
                            role.floor = 0
                        role.hurt(type="肉体")
                        yard.into(role)


# ------------------------------------烟雾------------------------------------
class Smoke(Event):
    def __init__(self):
        self.name = "烟雾"

    def do(self, *args, **kwargs):
        print("浓烟滚滚的从四处冒出，你流着泪，喉头刺痛。")
        role = kwargs.get("role")
        role.room.sign.append("烟雾")


# ------------------------------------墓土------------------------------------
class GraveDust(Event):
    def __init__(self):
        self.name = "墓土"

    def do(self, *args, **kwargs):
        print("这个房间完全被灰尘所覆盖着，当你进入时，气流扬起了这些或许沉寂几个世纪的尘土。")
        role = kwargs.get("role")
        res = role.ability_challenge(ability="力量", type="事件")
        if sum(res) >= 4:
            print(role.name, "猛地挥手将灰尘扫除，力量上升1个级别。")
            role.promote(ability="力量")
        else:
            print(role.name, "没能驱散这可疑的尘土，不小心吸入肺中")
            role.buff.append("墓土")


# ------------------------------------究竟怎么回事？------------------------------------
class Strange(Event):
    def __init__(self):
        self.name = "究竟怎么回事？"

    def do(self, *args, **kwargs):
        print("你觉得你走进了一个充满迷雾的走廊，迷迷糊糊的前进着，当你回头望去，发现一切迷雾都消失了")
        role = kwargs.get("role")
        set_room(None, role.floor, role.room.x, role.room.y)
        while True:
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if game_map[role.floor].map[x][y] is None:
                set_room(role.room, role.floor, x, y)
                break


# ------------------------------------迷失神志------------------------------------
class LostSpirit(Event):
    def __init__(self):
        self.name = "迷失神志"

    def do(self, *args, **kwargs):
        print("一名身穿旧式礼服的新娘子向你招手，你顿时恍惚出神")
        role = kwargs.get("role")
        res = role.ability_challenge(ability="知识", type="事件")
        if sum(res) >= 5:
            print("某些异样让你迅速的回复了神志，知识上升1个级别")
        else:
            print("迷迷糊糊之中，你发现你向着不知何处前进着")
            res = role.dice(n=3)
            if sum(res) == 6:
                print("回过神来，你发现你在入口处")
                role.floor = 1
                role.x = 4
                role.y = 6
                lobby_0.into(role)
                return
            elif 4 <= sum(res) <= 5:
                print("回过神来，你发现你在上台阶处")
                role.floor = 2
                role.x = 4
                role.y = 4
                up_steps.into(role)
                return
            elif 2 <= sum(res) <= 3:
                role.floor = 2
            elif 0 <= sum(res) <= 1:
                role.floor = 0
            while True:
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                if game_map[role.floor].map[x][y] is None:
                    set_room(role.explore(direction=random.randint(0, 3)), role.floor, x, y)
                    break


# ------------------------------------水滴------------------------------------
class Drip(Event):
    def __init__(self):
        self.name = "水滴"

    def do(self, *args, **kwargs):
        print("“滴。。。滴。。。滴。。。”")
        print("这个房间某处像是有根不断滴水的管子，然而你却什么都没有发现，那个滴水的声音一直回荡在你的脑海中。")
        role = kwargs.get("role")
        role.room.sign.append("水滴")


# ------------------------------------悄无声息------------------------------------
class Silent(Event):
    def __init__(self):
        self.name = "悄无声息"

    def do(self, *args, **kwargs):
        print("身处地下的人们突然发觉自己听觉失灵，四周寂静得令人发狂，甚至连自己的声音都听不见。")
        for role in role_list:
            if role.floor == 0:
                n = 0
                if "玩具猴" in role.buff:
                    print("无声的环境中，", role.name, "手中的玩具猴异常诡异。（骰子-2）")
                    n = -2
                res = role.ability_challenge(ability="意志", type="事件")
                if sum(res) >= 4:
                    print(role.name, "正定心神，不多时，听觉便自己恢复了")
                elif 1 <= sum(res) <= 3:
                    print(role.name, "发狂的大叫，却依然听不见任何声响。骰1精神伤害")
                    role.hurt(type="精神")
                else:
                    print(role.name, "陷入无意识状态。骰2精神伤害")
                    role.hurt(type="精神", n=2)


# ------------------------------------墙上雾霭------------------------------------
class Fog(Event):
    def __init__(self):
        self.name = "墙上雾霭"

    def do(self, *args, **kwargs):
        print("身处地下的人们自己所在的房间墙壁上弥漫起一层雾霭，雾中隐约藏着许多面孔，有人类的。。也有异类的。")
        for role in role_list:
            if role.floor == 0:
                n = 0
                res = role.ability_challenge(ability="意志", type="事件")
                if sum(res) >= 4:
                    print(role.name, "很快稳定了心神，发现那些只是光影中的错觉，一切都很正常")
                elif 1 <= sum(res) <= 3:
                    print(role.name, "骰1精神伤害")
                    role.hurt(type="精神")
                    if role.room.item_type == "事件":
                        print(role.name, "身处灵异房间，额外骰1精神伤害")
                        role.hurt(type="精神")
                else:
                    print(role.name, "陷入无意识状态。骰2精神伤害")
                    role.hurt(type="精神")
                    if role.room.item_type == "事件":
                        print(role.name, "身处灵异房间，额外骰2精神伤害")
                        role.hurt(type="精神", n=2)


# ------------------------------------灯灭------------------------------------
class Lightout(Event):
    def __init__(self):
        self.name = "灯灭"

    def do(self, *args, **kwargs):
        print("你的手电筒突然熄灭，黑暗中你难以前行，不过，其他人那里应该有多的电池。")
        role = kwargs.get("role")
        if "蜡烛" in role.buff:
            print(role.name, "想起了之前捡到的蜡烛，这个也可以作为光源使用。")
        elif stove_room == role.room:
            print(role.name, "虽然没有了手电，不过这里是暖炉房，通过房间内的杂物制作了一个简易火把。")
        else:
            role.buff.append("灯灭")


# ------------------------------------亡骸------------------------------------
class Skeletons(Event):
    def __init__(self):
        self.name = "亡骸"

    def do(self, *args, **kwargs):
        print("一对可怜的母子在地上仍相互拥抱着")
        role = kwargs.get("role")
        role.hurt(type="精神")
        role.room.sign.append("亡骸")


# ------------------------------------凛冽强风------------------------------------
class Wild(Event):
    def __init__(self):
        self.name = "凛冽强风"

    def do(self, *args, **kwargs):
        rooms = room_search(names=["庭院", "墓园", "天井", "塔楼", "露台"])
        for room in rooms:
            for role in room.get_creatures():
                res = role.ability_challenge(ability="力量", type="事件")
                if sum(res) >= 5:
                    print(role.name, "坚定的站立着")
                elif 3 <= sum(res) <= 4:
                    print(role.name, "被风吹倒了，骰1肉体伤害")
                    role.hurt(type="肉体")
                elif 1 <= sum(res) <= 2:
                    print(role.name, "寒风似乎冻结了你的灵魂，骰1精神伤害")
                    role.hurt(type="精神")
                elif sum(res) == 0:
                    print(role.name, "被风吹倒了，翻滚过程中，似乎有什么东西遗落到某处")
                    role.hurt(type="肉体")
                    item = role.discard_list()
                    lobby_0.items.append(item)


# ------------------------------------保险箱------------------------------------
class Box(Event):
    def __init__(self):
        self.name = "保险箱"

    def do(self, *args, **kwargs):
        print("在这个屋子的某个墙后，你发现了一个隐秘的保险箱")
        role = kwargs.get("role")
        role.room.sign.append("保险箱")


# ------------------------------------约拿的戏耍------------------------------------
class Trick(Event):
    def __init__(self):
        self.name = "约拿的戏耍"

    def do(self, *args, **kwargs):
        print("进入房间的你发现两个小孩正拿着木制陀螺玩耍。")
        print("一个小孩说：“约拿，你要自己抛一趟么？”")
        print("约拿：“不！我只想自己玩！”")
        print("约拿拿起手中的陀螺大力的击打在另一个孩童头上，一下又一下的猛击着。")
        role = kwargs.get("role")
        if "玩具猴" in role.buff or "魔术方块" in role.buff:
            print("约拿似乎对你身上的某些物品感兴趣")
            print("约拿穿过了你的身体，你感觉某些东西失去了")
            print("约拿和小孩的身影消失了，你的意志清醒了不少")
            if monkey in role.items:
                role.items.remove(monkey)
                role.promote(abiliy="意志")
            if magic_box in role.items:
                role.items.remove(magic_box)
                role.promote(abiliy="意志")
        else:
            print("两名孩童的身影渐渐消失了，骰1精神伤害")
            role.hurt(type="精神")


# ------------------------------------镜中映像_1------------------------------------
class Mirror_1(Event):
    def __init__(self):
        self.name = "镜中映像"

    def do(self, *args, **kwargs):
        role = kwargs.get("role")
        print("房间中古老的大镜映照着惊慌失措的你")
        print("你忽然意识到，这是某一时空的自己")
        print("而你发现你可以透过此镜可以传递一件物品")
        if len(role.get_items_list()) > 0:
            print("你决定帮助镜子那边的自己")
            item = role.get_items_list()
            item_card_set.append(item)
            random.shuffle(item_card_set)
        else:
            print("然而这个时空的你似乎束手无策")


# ------------------------------------镜中映像_2------------------------------------
class Mirror_2(Event):
    def __init__(self):
        self.name = "镜中映像"

    def do(self, *args, **kwargs):
        role = kwargs.get("role")
        print("房间中古老的大镜映照着惊慌失措的你")
        print("你忽然意识到，这是某一时空的自己")
        print("这时，你发现镜子中的自己向你递过来一件物品")
        role.items.append(draw_card("物品"))


# ------------------------------------瓦砾------------------------------------
class Rubble(Event):
    def __init__(self):
        self.name = "瓦砾"

    def do(self, *args, **kwargs):
        print("泥灰瓦砾从墙壁和天花板上塌落下来，你尝试躲开。")
        role = kwargs.get("role")
        res = role.ability_challenge(ability="速度", type="事件")
        if sum(res) >= 3:
            print(role.name, "躲开了塌下的瓦砾，速度上升1个级别")
            role.promote(ability='速度')
        elif 1 <= sum(res) <= 2:
            print(role.name, "被瓦砾掩埋，骰1肉体伤害")
            role.hurt(type="肉体")
            role.buff.append("瓦砾")
        else:
            print(role.name, "被瓦砾掩埋，骰1肉体伤害")
            role.hurt(type="肉体", n=2)
            role.buff.append("瓦砾")


# ------------------------------------焦虑的声响------------------------------------
class Noise(Event):
    def __init__(self):
        self.name = "焦虑的声响"

    def do(self, *args, **kwargs):
        print("一些声音在你脑海中响起，是被遗弃的婴儿的哭喊声，高声的尖叫，玻璃破碎声。然后，一片寂静。")
        role = kwargs.get("role")
        res = role.dice(n=6)
        if sum(res) == len(role.omens):
            print("一股神秘的力量稳定了你的心神，让你的负面情绪一扫而空。")
            role.promote(ability="意志")
        else:
            print("负面情绪充斥的你的心里，你感到很难受。")
            role.hurt(type="肉体")


# ------------------------------------壁柜门------------------------------------
class Closet(Event):
    def __init__(self):
        self.name = "壁柜门"

    def do(self, *args, **kwargs):
        print("在这个房间，你找到一个壁柜门")
        role = kwargs.get("role")
        role.room.sign.append("壁柜")


# ------------------------------------哎哟！------------------------------------
class Ache(Event):
    def __init__(self):
        self.name = "哎哟！"

    def do(self, *args, **kwargs):
        print("你突然感到一个生物在你脚下，当你尝试躲开的时候，你被绊倒了。")
        print("当你到下时，你只听到咯咯的笑声，回望地上并无异样。你起身时发现某件物品从你身上遗失了。")
        role = kwargs.get("role")
        if len(role.items) > 0:
            random.shuffle(role.items)
            role.items.pop()


def event_init():
    scream = AHorribleScream()
    event_card_set.append(scream)
    silk_screen = SilkScreen()
    event_card_set.append(silk_screen)
    nature = NatureOfFrenzy()
    event_card_set.append(nature)
    hope = Hope()
    event_card_set.append(hope)
    freedom = Freedom()
    event_card_set.append(freedom)
    smoke = Smoke()
    event_card_set.append(smoke)
    grave_dust = GraveDust()
    event_card_set.append(grave_dust)
    strange = Strange()
    event_card_set.append(strange)
    lost_spirit = LostSpirit()
    event_card_set.append(lost_spirit)
    drip = Drip()
    event_card_set.append(drip)
    silent = Silent()
    event_card_set.append(silent)
    fog = Fog()
    event_card_set.append(fog)
    lightout = Lightout()
    event_card_set.append(lightout)
    skeletons = Skeletons()
    event_card_set.append(skeletons)
    wild = Wild()
    event_card_set.append(wild)
    box = Box()
    event_card_set.append(box)
    trick = Trick()
    event_card_set.append(trick)
    mirror_1 = Mirror_1()
    event_card_set.append(mirror_1)
    mirror_2 = Mirror_2()
    event_card_set.append(mirror_2)
    rubble = Rubble()
    event_card_set.append(rubble)
    noise = Noise()
    event_card_set.append(noise)
    closet = Closet()
    event_card_set.append(closet)
    ache = Ache()
    event_card_set.append(ache)
    # 打乱
    random.shuffle(event_card_set)
