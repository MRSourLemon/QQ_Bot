import random
from pathlib import Path
from nonebot.plugin import on_command
from nonebot.adapters.qq import  MessageEvent, MessageSegment
from PIL import Image, ImageDraw,ImageFont


"""
图文合成
"""
async def add_text_to_image(image_path, output_path,content,font_path, font_size, text_color,text_position ,position):
    """
    给图片添加文字
    :param image_path: 输入图片的路径
    :param output_path: 合成后的图片名称
    :param content: 要添加的文字内容
    :param font_path: 字体文件路径
    :param font_size: 文字的字体大小
    :param text_color: 文字颜色 (255, 0, 0) "#FF0000" "red"
    :param text_position: 文字对齐方式，可选值："left", "center", "right"
    :param position: 文字位置，可选值："left", "right", "center", "top", "bottom", "top left corner", "top right corner", "bottom left corner", "bottom right corner"
    :return:
    """
    # 打开图片
    image = Image.open(image_path)
    # 创建一个可用于绘制的对象
    draw = ImageDraw.Draw(image)
    # 设置字体和字体大小
    font = ImageFont.truetype(font_path, font_size)

    wrapped_text,current_width = "",0

    # 遍历文本中的每个字符
    for char in content:
        # 获取字符的宽度
        char_width, _ = draw.textbbox((0, 0), char, font=font)[2:]
        # 如果当前行的宽度加上字符宽度超过图片指定宽度，则换行
        if current_width + char_width > image.width * 9 // 10:  # 这里是图片的十分之九
            wrapped_text += "\n"
            current_width = 0
        # 将字符添加到当前行
        wrapped_text += char
        # 更新当前行的宽度
        current_width += char_width

    # 获取换行后文本的宽度和高度
    text_width, text_height = draw.textbbox((0, 0), wrapped_text, font=font)[2:]

    # 根据位置参数计算文本的位置
    if position == "left":
        position = (0, (image.height - text_height) // 2)
    elif position == "right":
        position = (image.width - text_width, (image.height - text_height) // 2)
    elif position == "center":
        position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
    elif position == "top":
        position = ((image.width - text_width) // 2, 0)
    elif position == "bottom":
        position = ((image.width - text_width) // 2, image.height - text_height)
    elif position == "top left corner":
        position = (0, 0)
    elif position == "top right corner":
        position = (image.width - text_width, 0)
    elif position == "bottom left corner":
        position = (0, image.height - text_height)
    elif position == "bottom right corner":
        position = (image.width - text_width, image.height - text_height)
    elif position == "bottom left corner 9/10":
        position = (0, image.height * 9 // 10 - text_height)

    # 在图片上绘制文本
    draw.multiline_text(position, wrapped_text, font=font, fill=text_color, align=text_position)
    # 保存合成后的图片
    image.save(output_path)
    # 关闭图片
    # image.close()
import os
import asyncio
import shutil


async def delete_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在。")
    except Exception as e:
        print(f"删除文件时发生错误: {e}")

import os
from pathlib import Path

path = os.getcwd()+'/src/resources'


# 塔罗牌图片路径
#image_local_qq_image_path =  path+'/image/qq_image'
#os.makedirs(image_local_qq_image_path, exist_ok=True)
# 个人图片路径
image_local_path= path+"/image/MaoYuNa"
os.makedirs(image_local_path, exist_ok=True)
# cf ratings路径
rating_path = path+'/image/cf_ratings/'
os.makedirs(rating_path, exist_ok=True)
# 塔罗牌图片路径
#tarots_img_path = path+'/image/tarot/TarotImages/'
#os.makedirs(tarots_img_path, exist_ok=True)
# 摸摸头图片路径
#rua_png = path+'/image/rua/'
#os.makedirs(rua_png, exist_ok=True)
# 喜报、悲报图片路径
good_bad = path+'/image/good_bad_news/'
os.makedirs(good_bad, exist_ok=True)
#谁说 生成图片路径
who_say_path = path+'/image/who_say/'
os.makedirs(who_say_path, exist_ok=True)
#yuc_wiki 动漫wiki
yuc_wiki_path = path + '/image/yuc_wiki/'
os.makedirs(yuc_wiki_path, exist_ok=True)
# 字体路径
font_path = path + '/font/'
os.makedirs(font_path, exist_ok=True)
# 临时数据路径
temp_path = path + '/temp/'
os.makedirs(temp_path, exist_ok=True)
# JM下载位置
jm_path = path + '/image/jm/'
os.makedirs(jm_path, exist_ok=True)
# 日志路径
log_path = path+'/log/'
os.makedirs(log_path, exist_ok=True)
# 视频路径
video_path = path+'/video/'
os.makedirs(video_path, exist_ok=True)

#jm配置文件路径
jm_config_path = os.getcwd()+'/src/configs/jm_config.yml'

# # 语音路径
# RECORD_PATH = Path() / "src" / "resources" / "record"
# # 文本路径
# TEXT_PATH = Path() / "src" / "resources" / "text"
# # 数据路径
# DATA_PATH = Path() / "src" / "data"
# # 网页模板路径
# TEMPLATE_PATH = Path() / "src" / "resources" / "template"
# # 视频路径
# VIDEO_PATH = Path() / "src" / "resources" / "videos"

luxun = on_command("luxun", aliases={"鲁迅说"}, rule=None)
@luxun.handle()
async def handle(message: MessageEvent):

    filename = str(message.get_user_id()) + str(random.randint(0, 10000)) + ".jpg"
    value = message.get_plaintext().split(" ")
    keyword, content = value[0], value[1]
    if len(value) < 2 or len(value) > 2 or value[1] == "":
        await luxun.finish("你让鲁迅说点啥?格式不对自己捋一捋吧~")
    if len(content) >= 24:
        await luxun.finish("太长了, 鲁迅说不完! 24字以内~")
    else:
        await add_text_to_image(image_path=who_say_path + "luxun.jpg", output_path=temp_path + filename, content="      "+content+"   —鲁迅",
                                font_path=font_path + "华文行楷.TTF", font_size=28, text_color=(255, 255, 255),text_position="left",
                                position="bottom left corner 9/10")
        await luxun.send(MessageSegment.file_image(Path(temp_path + filename)))
        await delete_file(temp_path + filename)