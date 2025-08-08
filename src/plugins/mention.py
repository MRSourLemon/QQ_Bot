from pathlib import Path
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.qq import  MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
import random

import os
#mention_user

mention = on_command("mention", rule=to_me(), priority=10, block=True)
 
@mention.handle()
async def handle_function(args: Message = CommandArg()):
    #await mention.finish(MessageSegment.at("all"))  # 发送@所有人消息
    # 发送@所有人消息
    # 注意：确保你的QQ机器人有权限发送@所有人消息，否则可能会失败
    
    #await mention.finish(MessageSegment.mention_user(1))  
    if at_name := args.extract_plain_text():
        # 发送@指定用户消息
        await mention.finish(MessageSegment.mention_user(at_name))
        
    else:
        await mention.finish("type in at_name")