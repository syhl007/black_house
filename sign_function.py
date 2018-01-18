from util import draw_card


def skeletons(*args, **kwargs):
    role = kwargs.get('role')
    print(role.name, "开始搜寻亡骸，以期找到有价值的东西。")
    res = role.ability_challenge(ability="意志", type="房间")
    print(role.name, "意志鉴定结果为：", res)
    if sum(res) >= 5:
        print(role.name, "找到了一件物品")
        item = draw_card(type="物品")
        role.gain_obj(item)
        role.room.sign.remove("骸骨")
        return True
    else:
        print(role.name, "一无所获，受到1点精神伤害")
        role.hurt(ability="精神", value=1)
        return False


sign_func_dict = {
    "骸骨": skeletons,
}
