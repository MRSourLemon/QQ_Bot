from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.qq import Bot, MessageEvent, MessageSegment ,GroupMessageEvent
import random
wife = on_command("wife", rule=to_me(), aliases={"wife"}, priority=10, block=True)
@wife.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    #await wife.finish("1")
    try:
        # 获取群成员列表
        member_list = await bot.get_group_members(group_id=event.group_id)
        
        if not member_list:
            await wife.finish("获取群成员列表失败，请稍后再试~")
        
        # 过滤掉机器人自己
        members = [m for m in member_list if not str(m.get("user_id")) == str(bot.self_id)]
        
        if not members:
            await wife.finish("群里没有其他成员可以@了呢~")
        
        # 随机选择一位成员
        lucky_member = random.choice(members)
        user_id = lucky_member["user_id"]
        nickname = lucky_member.get("nickname", "群友")
        card = lucky_member.get("card", nickname)  # 群名片
        
        # 构建回复消息
        msg = f"  {card} ！"
        await wife.finish(msg)
        
    except Exception as e:
        await wife.finish(f"出错了: {str(e)}")
