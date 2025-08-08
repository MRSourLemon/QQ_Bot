import random
from nonebot.rule import to_me
from nonebot import on_command, on_startswith, on_keyword, on_fullmatch, on_message
from nonebot.adapters.qq import Bot, MessageSegment, Message, Event, escape, ActionFailed, MessageEvent
from nonebot.params import ArgPlainText, CommandArg, ArgStr
import time
import datetime
import os
from pathlib import Path
update = on_command("更新日志", aliases={"update"}, rule=to_me(), priority=10, block=True)

@update.handle()
async def handle_update():
    update_log = r"src\update.md"
    # 检查更新日志文件是否存在
    if not Path(update_log).exists():
        await update.finish("更新日志文件不存在。请联系管理员。")
    # 模拟获取更新日志
    with open(update_log, 'r',encoding='utf-8') as file:
        update_log = file.read()
    # 如果日志为空，发送默认消息
    if not update_log.strip():
        update_log = "暂无更新日志。请稍后再试。"
    # 发送更新日志
    await update.finish(MessageSegment.text(update_log))