import re
from nonebot.adapters.qq import MessageEvent
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
import requests
from nonebot.adapters import Message
from nonebot.exception import MatcherException

shuangseqiu = on_command("双色球", rule=to_me(), priority=10, block=True)
@shuangseqiu.handle()
async def handle_shuangseqiu(message: MessageEvent, args: Message = CommandArg()):
    url = "http://101.35.2.25/api/caipiao/shuangseqiu.php?id=10007133&key=bb0315bf8a1725a7533ac83cf36c78f9"
    msg = args.extract_plain_text()

    response = requests.get(url, verify=False)
    if response.status_code != 200:
        await shuangseqiu.finish("Failed to fetch data from the API.", at_sender=True)
    data = response.json()
    if data['code'] == 200:
        content = data['number'] +" "+data['number1']+" "+ data['qihao']
        await shuangseqiu.finish(content, at_sender=True)

    else:
        await shuangseqiu.finish("Failed to fetch data from the API.")