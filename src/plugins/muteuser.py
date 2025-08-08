from pathlib import Path
from re import U
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.qq import  MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
import random
from nonebot.adapters.qq import Bot
from nonebot import get_bot
import os

import requests

def ban_member(group_id: str, user_id: str, duration: int):
    url = "https://api.q.qq.com/api/group/ban_member"
    headers = {
        "Authorization": "NjtjU8u76wx1BIrbsracbfLnJizS72Lz",  # 替换为你的Token
        "Content-Type": "application/json"
    }
    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "duration": duration
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("禁言成功")
    else:
        print(f"禁言失败: {response.json()['message']}")



mute= on_command("mute", rule=to_me(), priority=10, block=True)
@mute.handle()
async def handle_function(bot:Bot):
    #await mute.finish("mute user")
    bot = get_bot("102801649")
    guildID = "2108"
    userID = "Shelockun"
    options = { "seconds": "100" }  # 设置禁言时长为100秒
    # 调用禁言API
    #await bot.api.muteMember(guildID, userID, options      
    #await bot.set_group_ban(guildID,userID)
    ban_member(guildID, userID, 100)
    await mute.finish("mute user success")
