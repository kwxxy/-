import requests
import re

#url给定
url = 'https://www.jianshu.com/p/68a7e6a6de3c'
#爬取指定标识
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
#首页内容获取
sh_ye = requests.get(url, headers = headers)
#指定文章编码
sh_ye.encoding = 'utf-8'
sh_txt = sh_ye.text

wen_url_t = re.findall(r'<div class="image-caption">(.*?)<div data-vcomp="free-reward-panel">', sh_txt, re.S)

#将列表转换为字符串
wen_url_t_str = ''.join(wen_url_t)
wen_url_t_all = re.findall(r'<p>(.*?)</p>', wen_url_t_str, re.S)
wen_url_t_all = ''.join(wen_url_t_all)

wen_url_t_all = re.sub(r'<div class="image-package">.*?</p>', '', wen_url_t_all, re.S)
wen_url_t_all = wen_url_t_all.replace('<br>', '')
print(wen_url_t_all)

