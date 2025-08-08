import random
from nonebot.rule import to_me
from nonebot import on_command, on_startswith, on_keyword, on_fullmatch, on_message
from nonebot.adapters.qq import Bot, MessageSegment, Message, Event, escape, ActionFailed, MessageEvent
from nonebot.params import ArgPlainText, CommandArg, ArgStr
import time
import datetime
from src.plugins.jianyan import jianyan

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

ren_pin_table_table=[]
jian_yan_table=[]
id=[]
lastcall_date = None
jian_yan=0
renpin = on_command("人品", aliases={"今日人品"})
@renpin.handle()
async def _(event: MessageEvent, message : MessageEvent):
    global id, ren_pin_table, lastcall_date,jian_yan_table,jian_yan
    if IS_NEWDAY(lastcall_date):
        id=[]
        ren_pin_table=[]
        jian_yan_table=[]
    #await renpin.finish("1")
    lastcall_date = datetime.date.today()
    member_openid = str(message.get_user_id())
    content = ""
    ren_pin=0
    if member_openid in id:
       # 安全检查，确保索引在范围内
       index = id.index(member_openid)
       if index < len(ren_pin_table):
           ren_pin = ren_pin_table[index]
           jian_yan = jian_yan_table[index]
       else:
           await renpin.send("数据错误，请稍后重试。")
    else:
       id.append(member_openid)
       temp = random.randint(0, 100)
       ren_pin_table.append(temp)
       ren_pin = temp
       jian_yan=random.randint(ren_pin,100)
       jian_yan_table.append(jian_yan)
    
    content = ("今日人品:"+str(ren_pin)+"\n"
               + jianyan(jian_yan) + "\n"
               + "仅供娱乐|相信科学|请勿迷信" + "\n")
    await renpin.finish(content)


timezero = on_command("time")
@timezero.handle()
async def time_zero(event: MessageEvent, message : MessageEvent,):
    if IS_ZERO():
        await timezero.send("是零点")
    else:
        await timezero.send("不是零点")
import psutil
 
status_send = on_command("status", aliases={"状态"}, rule=to_me(), priority=10, block=True)
@status_send.handle()
async def handle_status():
    await status_send.finish("cpu使用率: "+str(psutil.cpu_percent(interval=1))+"%\n"
                                +"内存使用率: "+str(psutil.virtual_memory().percent)+"%\n"
                                +"磁盘使用率: "+str(psutil.disk_usage('/').percent)+"%\n"
                               # +"网络状态: "+str(psutil.net_if_stats())+"\n"
                               # +"传输数据: "+str(psutil.net_io_counters())+"\n"
                                )
