import re
import requests
from urllib import request
import time


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}
proxies = {
    "http": "http://123.207.96.189:80"
}
url = 'https://m.weibo.cn/detail/4459323771679529'
response = requests.get(url, proxies=proxies, headers=headers)
pattern = re.compile(r'wx\d.sinaimg.cn\/large\/.+?\.jpg') #按照我们的要求编的正则
results = pattern.findall(response.text)
print(len(results))  #看看找到了几条
print(results)  #再看看有哪些

for i, pic in enumerate(results):
    pic_url = 'http://' + pic  # 加上协议
    # print(pic_url)
    request.urlretrieve(pic_url, 'C://Users/Robert/Desktop/123/{0}.jpg'.format(i))  # 保存在已有的文件夹目录下
    time.sleep(1)
