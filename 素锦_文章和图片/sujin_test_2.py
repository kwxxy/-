#函数式编程

import requests
import re


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}

def Download(url):
    response = requests.get(url, headers = header)
    response.encoding = response.apparent_encoding
    return response.text

def Spider(one_url):
    html = Download(one_url)
    url_title_list = re.findall(r'<h3><a .*?</a></h3>', html, re.S)
    for url_title in url_title_list:
        url_list = re.findall(r'href="(.*?)">', url_title)
        title_list = re.findall(r'">(.*?)</a>', url_title)
        #  print(url_list, title_list)
        # 5. 进入每一个网页，并获取图片和信息
        tu_wen = requests.get(url_list[0], headers=header)
        # tu_wen.encoding = tu_wen.apparent_encoding                   # 看原网页编码
        # 6. 接收网页文本
        tu_wen_txt = tu_wen.text
        url_tu = re.findall(r'<div id="jg">.*?</div>', tu_wen_txt, re.S)[0]  # 获取图片全地址
        url_wen = re.findall(r'<div class="content">(.*?)<a href', tu_wen_txt, re.S)[0]  # 获取文本
        # 保存图片
        url_tu_list = re.findall(r'href="(.*?)"><', url_tu, re.S)
        for url_tu_url in url_tu_list:
            url_dizhi = url_tu_url.split('/')[-1]
            print(url_dizhi)
            root = 'D:\素锦_文章和图片\picture\\'
            path = root + url_dizhi
            tupian = requests.get(url_tu_url, headers=header)
            with open(path, 'wb') as f:
                f.write(tupian.content)
        url_wen = url_wen.replace('<br />', '')
        url_wen = url_wen.replace('<p>', '')
        file = open('text\%s.txt' % title_list[0], 'w', encoding='utf-8')
        file.write(url_wen)
        file.close()

if __name__ == '__main__':
    one_url = 'http://isujin.com/'
    Spider(one_url)