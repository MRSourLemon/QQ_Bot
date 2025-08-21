import requests
token = "LwExDtUWhF3rH5ib"
msg = input()
url = f"https://v2.alapi.cn/api/mingyan?typeid={int(msg)}&token={token}"
response =  requests.get(url, verify=False)


data = response.json()

content = data['data']['content']+"\n--"+data['data']['author'] + "\n" + str(data['data']['typeid'])
print(content)

print(url)