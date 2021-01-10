import re
import requests
import os
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}
proxies = {
    "http": "http://123.207.96.189:80"
}
if not os.path.exists(os.getcwd()+'/comments'):
    os.mkdir(os.getcwd()+'/comments')

for i in range(0,200,20):
    url = 'https://movie.douban.com/subject/26100958/comments?start=' + str(i) + '&limit=20&sort=new_score&status=P&percent_type=h'
    #type=h,m,l,因反扒所限一次只能给出200条，共600条
    response = requests.get(url, proxies=proxies, headers=headers)
    # 必须加入代理否则会触发反扒机制
    temp_text = response.text
    pattern = '(?<=<span class="short">).*?(?=</span>)'
    results = re.findall(pattern, temp_text, re.S)
    print(results.__len__())
    file = open('result.txt', 'a', encoding='UTF-8')
    #输出
    for item in results:
        file.write(item)

