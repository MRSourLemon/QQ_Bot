from pathlib import Path
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.qq import  MessageSegment
import random

import os


image = on_command("gif", rule=to_me(), priority=10, block=True)
 
@image.handle()
async def handle_function():
    local_image_path = f"src/plugins/梗图/1.gif"
    while True:
        i= random.randint(0, 100)
        local_image_path = f"src/plugins/梗图/{i}.gif"  # 本地图片路径
        # 检查文件是否存在
        if Path(local_image_path).exists():
            break
    # 发送本地图片
    await image.finish(MessageSegment.file_image(Path(local_image_path)))