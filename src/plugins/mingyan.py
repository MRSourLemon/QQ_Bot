from re import A
from nonebot.adapters.qq import MessageEvent
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
import requests
from nonebot.adapters import Message
from nonebot.exception import MatcherException
token = "LwExDtUWhF3rH5ib"
url = f"https://v2.alapi.cn/api/mingyan?token={token}"
mingyan = on_command("名言", rule=to_me(), priority=10, block=True)
@mingyan.handle()
async def handle_mingyan(message: MessageEvent,args: Message = CommandArg()):
    global url, token
    msg = args.extract_plain_text()
    try:
        #await mingyan.send(msg)
        if msg:
            #await mingyan.send("1")
            try:
                num = int(msg)
                if num in range(1,45+1):
                    url = f"https://v2.alapi.cn/api/mingyan?typeid={int(msg)}&token={token}"
                    #await mingyan.send("2")
                else:
                    await mingyan.finish("Please provide a valid typeid between 1 and 45."+"名言类型：1——爱情 2——道德 3——青春 4——愿望 5——集体 6——理想 7——志向 8——人才 9——谦虚 10——人格 11——天才 12——青年 13——社会 14——国家 15——财富 16——智慧 17——修养 18——工作 19——妇女 20——儿童 21——思想 22——理智 23——学习 24——科学 25——信仰 26——诚信 27——读书 28——成败 29——奉献 30——劳动 31——节约 32——教育 33——企业 34——事业 35——时间 36——勤奋 37——民族 38——真理 39——友谊 40——自由 41——心理 42——心灵 43——人生 44——幸福 45——团结", at_sender=True)
            except ValueError:
                await mingyan.finish("Please provide a valid typeid between 1 and 45."+"名言类型：1——爱情 2——道德 3——青春 4——愿望 5——集体 6——理想 7——志向 8——人才 9——谦虚 10——人格 11——天才 12——青年 13——社会 14——国家 15——财富 16——智慧 17——修养 18——工作 19——妇女 20——儿童 21——思想 22——理智 23——学习 24——科学 25——信仰 26——诚信 27——读书 28——成败 29——奉献 30——劳动 31——节约 32——教育 33——企业 34——事业 35——时间 36——勤奋 37——民族 38——真理 39——友谊 40——自由 41——心理 42——心灵 43——人生 44——幸福 45——团结", at_sender=True)

        response =  requests.get(url, verify=False)
        if response.status_code != 200:
            await mingyan.finish("Failed to fetch data from the API.", at_sender=True)
        data = response.json()
        if data['code'] == 200:
            content = data['data']['content']+"\n--"+data['data']['author'] + "\n" + str(data['data']['typeid'])
            #await mingyan.send(url)#maybe make a url confirm func?
            await mingyan.finish(content, at_sender=True)
        else:
            await mingyan.finish("Failed to fetch data from the API.")
    except MatcherException:
        raise
    except Exception as e:
        await mingyan.finish(f"An error occurred: {str(e)}", at_sender=True)