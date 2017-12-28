from card import HouseCard, Map, Link

# 游戏进度
game_schedule = 0

# 地图初始化
game_map = [Map(floor=0), Map(floor=1), Map(floor=2)]
game_map[1].map[2][2].set_link(link=Link(start=game_map[1].map[2][2], end=game_map[0].map[2][2]))
game_map[0].map[2][2].set_link(link=Link(start=game_map[0].map[2][2], end=game_map[1].map[2][2]))






