#简书首页    面向过程
import requests
import re
import os

#url给定
url = 'https://www.jianshu.com/'
#爬取指定标识
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
#首页内容获取
sh_ye = requests.get(url, headers = headers)
#指定文章编码
sh_ye.encoding = 'utf-8'
#测试内容
#print(sh_ye.text)
html = sh_ye.text           #将网页文本内容以文本形式保存在‘html’中
#获取首页 文章 链接
sh_url_txt = re.findall(r'<a class="title" target="_blank" href="(.*?)">(.*?)</a>', html, re.S)
#print(sh_url_txt)
#给出单个url
for url_txt in sh_url_txt:
    wen_url = url_txt[0]    #文章url
    wen_txt = url_txt[1]    #文章标题

    #文章标题修改 去除无效字符
    wen_txt = wen_txt.replace('/', '')
    wen_txt = wen_txt.replace('|', '')

    #合成文章完整url
    wen_url = url + wen_url

    #获取url内容
    wen_url_t_u = requests.get(wen_url, headers = headers)
    wen_url_t_u.encoding = 'utf-8'
    wen_url_html = wen_url_t_u.text

    #找出包含 文本与图片的部分
    wen_url_all = re.findall(r'<div class="image-caption">(.*?)<div data-vcomp="free-reward-panel">', wen_url_html, re.S)
    #将列表转换为字符串
    wen_url_t_str = ''.join(wen_url_all)

    # 保存图片url
    wen_url_pic_all = re.findall(r'<img data-original-src="(.*?)" dat', wen_url_t_str, re.S)
    #在指定目录下创建目录
    files = 'D:\Spider\jian_shu\picture'
    if os.path.isdir(files):        #判断目录是否存在
        os.mkdir(os.path.join(files, wen_txt))

        print(os.getcwd())

    for wen_url_pic in wen_url_pic_all:
        url_pic = 'https:' + wen_url_pic    #合成完整url
        url_pic_t = requests.get(url_pic, headers = headers)
        #取出图片名称
        url_pic_name = wen_url_pic.split('/')[-1]
        print(url_pic_name)
        print(wen_txt)

        #打开并写入二进制图片内容
        with open('picture\%s\%s'%(wen_txt, url_pic_name), 'wb+') as f:
            f.write(url_pic_t.content)

    #将段落文字保存
    wen_url_t = re.findall(r'<p>(.*?)</p>', wen_url_t_str, re.S)
    wen_url_t = ''.join(wen_url_t)
    #将多余部分清除
    wen_url_t = re.sub(r'<div class="image-package">.*?</p>', '', wen_url_t, re.S)
    wen_url_t = wen_url_t.replace('<br>', '')
    wen_url_t = wen_url_t.replace('<b>', '')
    wen_url_t = wen_url_t.replace('</b>', '')
    wen_url_t = wen_url_t.replace('。', '\n')

    #写入文本内容
    with open('text1\\%s.txt'%wen_txt, 'w', encoding='utf-8')as f:
        f.write(wen_url_t)
















