import re
import csv
import requests
import time
import multiprocessing

def Getchapter(url, header):
    try:
        txt = requests.get(url, headers=header)
        txt.raise_for_status()
        txt.encoding = txt.apparent_encoding

        return txt.text
    except:
        return ''

def Getcontent(url, header):
    time.sleep(1)
    html = Getchapter(url, header)
    title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html)[0]
    dl = re.findall(r'<dl>.*?</dl>', html, re.S)[0]
    zhangjie_info_list = re.findall(r'href="(.*?)">(.*?)<', dl)
    Savetext(zhangjie_info_list, title, header)

def Savetext(info_lists, titl, header):
    t = time.time()

    fd = open('%s.txt' % titl, 'w', encoding='utf-8')
    for zhangjie_info in info_lists:

        zhangjie_title = zhangjie_info[1]
        zhangjie_url = zhangjie_info[0]

        zhangjie_response = requests.get(zhangjie_url, headers=header)
        zhangjie_response.encoding = zhangjie_response.apparent_encoding
        zhangjie_html = zhangjie_response.text

        zhangjie_content = re.findall(r'<div id="content">(.*?)</div>', zhangjie_html, re.S)[0]

        zhangjie_content = zhangjie_content.replace('<br/>', '\n')
        zhangjie_content = zhangjie_content.replace('<br/>\u3000\u3000', '')

        fd.write(zhangjie_title)
        fd.write('\n')
        fd.write(zhangjie_content)
    print("单本小说时间: " + str(time.time()-t))

    fd.close()

if __name__ == '__main__':

    header = {
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
             }

    with open("alltext.csv", 'r', encoding='utf-8') as file:
        readers = csv.reader(file)
        pool = multiprocessing.Pool(processes=4)
        for reader in readers:
            pool.apply(Getcontent, (reader[0], header))
            Getcontent(reader[0], header)
        pool.close()
        pool.join()





