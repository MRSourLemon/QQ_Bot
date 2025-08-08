from pathlib import Path
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.qq import MessageSegment
import random

trail = on_command("图", rule=to_me(), priority=10, block=True)

@trail.handle()
async def handle_function():
    await trail.finish(MessageSegment.file_image("src/plugins/梗图/1.jpg"))