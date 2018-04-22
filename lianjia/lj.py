#爬取链家租房
import requests
import re
import pymysql
#创建函数  获取信息
def Get_info(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    '''
    di_zhi = r'<span class="region">(.*?)&nbsp;&nbsp;'
    jie_gou = r'class="zone"><span>(.*?)&nbsp;&nbsp;'
    da_xiao = r'class="meters">(.*?)&nbsp;&nbsp;'
    chao_xiang = r'</span><span>(.*?)</span></div><div'
    money = r'<div class="price"><span class="num">(.*?)<'
    lai_yuan = r'<div class="con"><a href=".*?">(.*?)</a><'
    '''
    #获取各个标题的值
    di = re.findall(r'<span class="region">(.*?)&nbsp;&nbsp;', response.text)
    jie = re.findall(r'class="zone"><span>(.*?)&nbsp;&nbsp;', response.text)
    da = re.findall(r'class="meters">(.*?)&nbsp;&nbsp;', response.text)
    chao = re.findall(r'</span><span>(.*?)</span></div><div', response.text)
    mon = re.findall(r'<div class="price"><span class="num">(.*?)<', response.text)
    lai = re.findall(r'<div class="con"><a href=".*?">(.*?)</a><', response.text)
    return di, jie, da, chao, mon, lai

def into_db(di, jie, da, chao, mon, lai,cur, conn):
    # zip()  将变量中的各个元素 对应打包成一个一个元组 再返回这些元组组成的列表
    # a = [1,2,3]
    # b = [4,5,6]
    # aa = zip(a,b)
    # [(1,4),(2,5),(3,6)]
    #
    for di_, jie_, da_, chao_, mon_, lai_ in zip(di, jie, da, chao, mon, lai):
        cur.execute('insert into lj(di, jie, da, chao, mon, lai) values("%s", "%s", "%s", "%s", "%s", "%s");'%(di_,jie_,da_,chao_,mon_,lai_))
        conn.commit()
if __name__ == '__main__':
    #链家租房
    url = 'https://cq.lianjia.com/zufang/'
    #接收各个标题的值
    di, jie, da, chao, mon, lai=Get_info(url)
    #连接mysql数据库
    conn = pymysql.connect('localhost', 'root', '123456', charset = 'utf8')
    #创建游标     位置标记
    cur = conn.cursor()
    #exexute() 执行sql命令
    cur.execute('create database if not exists lianjia;')
    #选择数据库
    conn.select_db('lianjia')

    sql = "create table lj (di varchar(40),jie varchar(40),da varchar(40), chao varchar(40),mon varchar(40),lai varchar(40));"
    #执行sql命令
    cur.execute(sql)
    # commit() 写入数据库  不写入会发生错误
    conn.commit()
    into_db(di, jie, da, chao, mon, lai, cur, conn)
    # 最后 要关闭连接
    conn.close()
