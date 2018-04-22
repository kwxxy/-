import requests
import re
import time
import random
# 1.给定一个网页的url
url = 'http://www.biquge5200.com/52_52542/'
response = requests.get(url)
response.encoding = response.apparent_encoding

#print(response.text)
html = response.text
# 2.获取小说的名字
title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html)[0]
#print(title)
#3.获取小说的章节和url
dl = re.findall(r'<dl>.*?</dl>',html,re.S)[0]
print(dl)
zhangjie_info_list = re.findall(r'href="(.*?)">(.*?)<',dl)
fd = open('%s.txt'% title, 'w',encoding='utf-8')

for zhangjie_info in zhangjie_info_list:
     # 循环下载章节
     zhangjie_title = zhangjie_info[1]
     zhangjie_url = zhangjie_info[0]
     #根据章节的url，下载章节

     zhangjie_response = requests.get(zhangjie_url)
     zhangjie_response.encoding = zhangjie_response.apparent_encoding
     zhangjie_html = zhangjie_response.text
     #print(zhangjie_html)
     zhangjie_content = re.findall(r'<div id="content">(.*?)</div>', zhangjie_html, re.S)[0]

     zhangjie_content = zhangjie_content.replace('<br/>', '\n')
     zhangjie_content = zhangjie_content.replace('<br/>\u3000\u3000', '')

     fd.write(zhangjie_title)
     fd.write('\n')
     fd.write(zhangjie_content)

     print(zhangjie_url,zhangjie_title)


fd.close()



