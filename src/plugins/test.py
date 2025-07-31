import random
from nonebot.rule import to_me
from nonebot import on_command, on_startswith, on_keyword, on_fullmatch, on_message
from nonebot.adapters.qq import Bot, MessageSegment, Message, Event, escape, ActionFailed, MessageEvent
from nonebot.params import ArgPlainText, CommandArg, ArgStr
import time
import datetime


def IS_ZERO():
    time_now = int(time.time())  # unix时间
    time_local = time.localtime(time_now)  # 转换为win_time
    dt = time.strftime("%H:%M:%S", time_local)  # 转换成新的时间格式(18:59:20)
    a = dt.split(':')
    b = []
    for a in dt.split(':'):
        b.append(a)
    c = ''.join(b)
    return c == '000000'


def IS_NEWDAY(last_date):
    current_time = datetime.date.today()
    if last_date is None:
        return True
    return current_time != last_date

ren_pin=[]
id=[]
lastcall_date = None

renpin = on_command("人品", aliases={"今日人品"})
@renpin.handle()
async def _(event: MessageEvent, message : MessageEvent):
     global id, ren_pin, lastcall_date
     if IS_NEWDAY(lastcall_date):
         id=[]
         ren_pin=[]
     lastcall_date = datetime.date.today()
     member_openid = str(message.get_user_id())
     if member_openid in id:
        #await renpin.send(ren_pin[id.index(member_openid)])
        #await renpin.send("id已存在")
        # 安全检查，确保索引在范围内
        index = id.index(member_openid)
        if index < len(ren_pin):
            await renpin.send(f"你的人品值是：{ren_pin[index]}")
        else:
            await renpin.send("数据错误，请稍后重试。")
     else:
        id.append(member_openid)
        temp = random.randint(0, 100)
        ren_pin.append(temp)
        await renpin.send(f"你的人品值是：{temp}")
    #await renpin.send("1")
    #await renpin.finish("1")

timezero = on_command("time")
@timezero.handle()
async def time_zero(event: MessageEvent, message : MessageEvent,):
    if IS_ZERO():
        await timezero.send("是零点")
    else:
        await timezero.send("不是零点")