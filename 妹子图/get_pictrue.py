import re
import os
import time
import random
import requests
import multiprocessing
from bs4 import BeautifulSoup


def Save_url(url, headers):
    time.sleep(random.randint(0,2))

    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'html.parser')
    urls_title = soup.find_all('h3', attrs={'class':'tit'})
    for url_title in urls_title:

        url = url_title.find('a')['href']
        title = url_title.find('a').string
        data = { 'url':url,
                 'title':title
                 }
    Get_u_t(data,headers)

def Get_u_t(data,headers):
    t = time.time()
    if not os.path.isdir(data['title']):
        os.mkdir(data['title'])
    html = requests.get(data['url'], headers=headers)
    html.encoding = html.apparent_encoding

    urls = re.findall(r'<img alt=".*?" src="(.*?)" /><br />', html.text, re.S)
    for url in urls:
        pictrue = requests.get(url, headers=headers)
        name = url.split('/')[-1]
        with open('{}\{}'.format(data['title'], name), 'wb') as f:
            f.write(pictrue.content)
    print("单个图集时间: " + str(time.time()-t))

if __name__ == '__main__':
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
              }
    pool = multiprocessing.Pool(processes=4)
    for i in ['http://www.meizitu.com/a/more_'+str(x)+'.html' for x in range(1, 73)]:
        pool.apply(Save_url, (i,headers))
    pool.close()
    pool.join()


