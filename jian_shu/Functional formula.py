import re
import requests
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}

def Download(url):
    response = requests.get(url, headers = headers)
    response.encoding = response.apparent_encoding
    return response.text

def Spider(url):
    html = Download()
    sh_url_txt = re.findall(r'<a class="title" target="_blank" href="(.*?)">(.*?)</a>', html, re.S)
    for url_txt in sh_url_txt:
        wen_url = url_txt[0]  # 文章url
        wen_txt = url_txt[1]  # 文章标题
        wen_txt = wen_txt.replace('/', '')
        wen_txt = wen_txt.replace('|', '')
        # 合成文章完整url
        wen_url = url + wen_url
        wen_url_t_u = requests.get(wen_url, headers=headers)
        wen_url_t_u.encoding = 'utf-8'
        wen_url_html = wen_url_t_u.text
        wen_url_all = re.findall(r'<div class="image-caption">(.*?)<div data-vcomp="free-reward-panel">', wen_url_html, re.S)
        wen_url_t_str = ''.join(wen_url_all)
        # 保存图片
        wen_url_pic_all = re.findall(r'<img data-original-src="(.*?)" dat', wen_url_t_str, re.S)
        files = 'D:\jian_shu\picture'
        if os.path.isdir(files):
            os.mkdir(os.path.join(files, wen_txt))
            print(os.getcwd())
        for wen_url_pic in wen_url_pic_all:
            url_pic = 'https:' + wen_url_pic
            url_pic_t = requests.get(url_pic, headers=headers)
            url_pic_name = wen_url_pic.split('/')[-1]
            url_pic_format = wen_url_pic.split('.')[-1]
            with open('picture\%s\%s' % (wen_txt, url_pic_name), 'wb+') as f:
                f.write(url_pic_t.content)
            # 将段落文字保存
        wen_url_t = re.findall(r'<p>(.*?)</p>', wen_url_t_str, re.S)
        wen_url_t = ''.join(wen_url_t)
        wen_url_t = re.sub(r'<div class="image-package">.*?</p>', '', wen_url_t, re.S)
        wen_url_t = wen_url_t.replace('<br>', '')
        wen_url_t = wen_url_t.replace('<b>', '')
        wen_url_t = wen_url_t.replace('</b>', '')
        wen_url_t = wen_url_t.replace('。', '\n')
        with open('text1\\%s.txt' % wen_txt, 'w', encoding='utf-8')as f:
            f.write(wen_url_t)

if __name__ == '__main__':
    url = 'https://www.jianshu.com/'
    Spider(url)