#慎动 copilot重构后动一下整个项目都炸

from pathlib import Path
from nonebot import on
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.qq import MessageSegment
import random

# 已发送图片记录
sent_images = []

image = on_command("梗图", rule=to_me(), priority=10, block=True)

@image.handle()
async def handle_function():
    global sent_images  # 使用全局变量记录已发送图片

    # 获取所有图片文件路径
    image_dir = Path("src/plugins/梗图")
    all_images = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png")) + list(image_dir.glob("*.gif"))

    # 检查是否有图片
    if not all_images:
        await image.finish("没有找到任何图片！")

    # 读取已发送的图片记录（只存文件名）
    with open("src/plugins/sent_images.txt", "r", encoding="utf-8") as sent_images_file:
        sent_images = [line.strip() for line in sent_images_file if line.strip()]

    # 获取未发送的图片（只比较文件名）
    unsent_images = [img for img in all_images if img.name not in sent_images]

    # 如果所有图片都已发送过一次，清空记录并重新开始
    if not unsent_images:
        sent_images = []
        unsent_images = all_images

    # 随机选择一个未发送的图片
    selected_image = random.choice(unsent_images)
    sent_images.append(selected_image.name)  # 只记录文件名

    # 追加写入文件名
    with open("src/plugins/sent_images.txt", "a", encoding="utf-8") as sent_images_file:
        sent_images_file.write(f"{selected_image.name}\n")

    # 发送图片，增加重试机制
    max_retries = 3  # 最大重试次数
    for attempt in range(max_retries):
        try:
            await image.send(MessageSegment.file_image(selected_image))
            return
        except Exception as e:
            if attempt < max_retries - 1:
                await image.send(f"发送图片失败，正在重试...({attempt + 1}/{max_retries})")
            else:
                await image.finish(f"发送图片失败，已尝试 {max_retries} 次。错误信息：{e}")

sent_images_flie_read = []

sent_image_file = on_command("已发送梗图", rule=to_me(), priority=10, block=True)

@sent_image_file.handle()
async def handle_sent_images():
    global sent_images, sent_images_flie_read

    # 读取已发送的图片记录（只存文件名）
    with open("src/plugins/sent_images.txt", "r", encoding="utf-8") as sent_images_file:
        sent_images = [line.strip() for line in sent_images_file if line.strip()]

    def sort_key(filename):
        # 按扩展名分组，jpg优先，其次png，最后gif
        ext_order = {'.jpg': 0, '.png': 1, '.gif': 2}
        name, ext = Path(filename).stem, Path(filename).suffix.lower()
        # 尝试将文件名前缀转为数字，非数字则为0
        try:
            num = int(name)
        except ValueError:
            num = name
        return (ext_order.get(ext, 99), num, filename)

    sent_images.sort(key=sort_key)

    if not sent_images:
        await sent_image_file.finish("没有已发送的梗图记录。")
    # 返回已发送的图片列表
    response = "已发送的梗图:\n" + " ".join(str(item) for item in sent_images)
    await sent_image_file.finish(response)