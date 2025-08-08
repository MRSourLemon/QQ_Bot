from nonebot import on
import requests
from nonebot.adapters.qq import MessageEvent
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
#question = "1"  # 默认问题
url = "https://v2.xxapi.cn/api/answers?question=1"

payload = {}
headers = {
'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'
}

#response = requests.request("GET", url, headers = headers, data = payload)

#print(response.text)
response = {"code":200,"msg":"数据请求成功","data":{"description_en":"Persist relentlessly until you reach your goal or complete the task.","description_zh":"坚持不懈，直到达到目标或完成任务。","title_en":"Persist until the end.","title_zh":"坚持到底"},"request_id":"0a2b68414532d4db3b9c7633"}
answer = on_command("答案", rule=to_me(), priority=10, block=True)
@answer.handle()
async def handle_answer(message: MessageEvent):
    global question, url , payload, headers , response
    question = message.get_plaintext().split(" ")
    #await answer.send("正在获取答案，请稍候...")

    # 提取参数纯文本作为问题，并判断是否有效
    #question = args.extract_plain_text() or question
    if not question:
        await answer.finish("请输入问题")
    url = f"https://v2.xxapi.cn/api/answers?question={question}"
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        await answer.finish("获取答案失败，请稍后再试。")
    response = response.json()
    
    await answer.finish(response["data"]["description_zh"] + "\n" + response["data"]["description_en"]
                         #+ "\n" + response["data"]["title_zh"] + "\n" + response["data"]["title_en"]
                         )