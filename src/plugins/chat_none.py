import json
import requests
from nonebot import on_command
from nonebot.adapters.qq import MessageEvent, MessageSegment
from nonebot.params import CommandArg
from typing import Dict, List

import json
from pathlib import Path
from typing import Dict, List

# 历史记录存储路径
HISTORY_PATH = Path("src/plugins/spark_history.json")

def load_histories() -> Dict[str, List[dict]]:
    """加载历史记录"""
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_histories(histories: Dict[str, List[dict]]):
    """保存历史记录"""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(histories, f, ensure_ascii=False, indent=2)

# 在插件中使用
#user_histories = load_histories()  # 启动时加载




# 星火API配置
API_KEY = "Bearer CRsrvqjeyYYvKzOAPJGt:utqNicILaofZIzHQZNfb"
API_URL = "https://spark-api-open.xf-yun.com/v1/chat/completions"

# 存储用户对话历史 {user_id: history}
user_histories: Dict[str, List[dict]] = {}

# 注册命令处理器
spark = on_command("星火", priority=10)

@spark.handle()
async def handle_spark(event: MessageEvent):
    user_id = event.get_user_id()


    raw_msg = event.get_message().extract_plain_text().strip()
    user_input = raw_msg.replace("/星火", "").strip()  # 手动移除命令前缀

    if not user_input:
        await spark.finish("请输入问题，例如：/星火 你好")

    # 初始化或获取该用户的历史记录
    if user_id not in user_histories:
        user_histories[user_id] = []

    # 保存时自动写入文件
    all_histories = load_histories()  # 启动时加载
    user_histories[user_id] = all_histories.get(user_id,[])

    # 添加用户提问到历史
    user_histories[user_id] = _add_message(user_histories[user_id], "user", user_input)
    
    # 调用星火API（流式）
    await spark.send("思考中...")
    full_response = ""
    async for chunk in _get_spark_stream(user_histories[user_id]):
        full_response += chunk
        # 分段发送避免消息过长被截断
        if len(full_response) % 100 == 0:
            await spark.send(chunk)

    # 添加AI回复到历史
    user_histories[user_id] = _add_message(user_histories[user_id], "assistant", full_response)
    
    save_histories(user_histories)
    
    await spark.finish(full_response)

# 工具函数：添加消息到历史（自动清理超长历史）
def _add_message(history: List[dict], role: str, content: str) -> List[dict]:
    new_history = history + [{"role": role, "content": content}]
    # 限制历史记录长度（按Token或简单按条数）
    while len(json.dumps(new_history)) > 8000:  # 简易长度控制
        new_history.pop(0)
    return new_history

# 工具函数：流式获取星火响应
async def _get_spark_stream(messages: List[dict]):
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
    body = {
        "model": "4.0Ultra",
        "messages": messages,
        "stream": True,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, json=body, headers=headers, stream=True)
        for line in response.iter_lines():
            if line and b'[DONE]' not in line:
                data = json.loads(line[6:])  # 跳过SSE前缀
                if "content" in data["choices"][0]["delta"]:
                    yield data["choices"][0]["delta"]["content"]
    except Exception as e:
        yield f"请求失败: {str(e)}"