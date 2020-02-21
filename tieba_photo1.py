import urllib.request
import re
import os
import random
import time
import requests
from bs4 import BeautifulSoup
import bs4
import socket

class empressive_bag():
    def __init__(self):      #初始化
        self.iplist=[]#初始化一个列表用于储存查找的代理ip
        self.num=0     #计算下载图片的数量
        self.znum=0   #预计下载的图片数量
        self.enum=0   #未下载的图片数量
        self.ip_num=0  #记录找到的ip个数
    def opens(self,url):     #用requests库来打开一个网址
        try:                 #报错时输出open error
            r=requests.get(url,headers={'user-Agent':'Mozilla/5.0'})
            r.encoding=r.apparent_encoding
            r.raise_for_status()
            return r
        except:               
            print('open error\n')
    def find_ip(self):        #抓取免费的代理ip
        url='http://www.xicidaili.com/nn'
        r=self.opens(url)     #打开该网址
        soup=BeautifulSoup(r.text,'html.parser')  #对获取的数据进行处理
        find=soup.find('div',class_="clearfix proxies") #查找标签为‘div’有一个‘class’属性且值为‘clearfix proxies’的标签
    
        for i in find('tr',class_="odd"):
            if isinstance(i,bs4.element.Tag):   #确认查找的是一个标签而非字符串
                ipmum=i('td')
                if ipmum[5].string=='HTTP':
                    self.iplist.append(ipmum[1].string+':'+ipmum[2].string)
                    self.ip_num=self.ip_num+1
                    print(ipmum[1].string+':'+ipmum[2].string,ipmum[5].string)
    def open_url(self,url):#使用代理ip
        choose=random.randint(0,self.ip_num-1)
        try:
            timeout = 2

            socket.setdefaulttimeout(timeout)

            proxy_support=urllib.request.ProxyHandler({'http':self.iplist[choose]})




            opener=urllib.request.build_opener(proxy_support)



            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36')]



            urllib.request.install_opener(opener)



            response =urllib.request.urlopen(url)
            return response.read()
        except:
            self.open_url(url)
    def find_adrs(self,idd): #查找表情包吧的一页的网址
        url='https://tieba.baidu.com/f?kw=%B1%ED%C7%E9%B0%FC&fr=ala0&tpl='
        url=url+idd
        res=self.open_url(url).decode('utf-8')
        a=res.find('j_th_tit ')
        t=0
        pho_adrs=[]
        while a !=-1:
            c=res.find('/',a,a+255)
            b=res.find('"',c,c+20)
            if b!=-1:
                if t==0:
                    t=t+1
                    a=res.find('j_th_tit ',b)
                    continue
                pho_adrs.append(res[c:b])
                t=t+1
               
            else:
                b=c
                
            a=res.find('j_th_tit ',b)
        print(pho_adrs)
        return pho_adrs
    def photo_load (self,photo_name,addrs):    # 下载照片
        ads='C:\\Users\\crawl\\Desktop\\'
        ads=ads+photo_name
        #print(addrs)
        try:
            os.mkdir(ads)
            os.chdir(ads)
        except:
            os.chdir(ads)
        for lists in addrs:
            try:
                print(lists)
                for address in lists:
                    self.znum=self.znum+1
                    response=self.open_url(address)
                    add=address.split("/")[-1]
                    with open(add,'wb') as f:
                        f.write(response)
                    self.num=self.num+1
            except:
                print("跳过一张\n")
                self.enum=self.enum+1
                continue

    def find_photo(self,pnum):      #  查找表情包吧的一个网址的所有表情包的地址
        url='https://tieba.baidu.com'
        addrs=[]
        for i in pnum:
            try:
                url=url+i
                response=self.open_url(url).decode('utf-8')
                p=re.compile(r'https://imgsa.baidu.com/forum/w%3D580/sign=.{73}[.]jpg')   #使用正则表达式查找图片地址
                addrs.append(p.findall(response))
            except:
                continue
    
            url='https://tieba.baidu.com'
        return addrs
    def main(self):#  主函数
        num=int(input("please input crawl number:\n"))
        name=input('please input your filename:\n')
        self.find_ip()
        for i in range(num):
            if i==0:
                flag=5
                lists=self.find_adrs(str(flag))
                addrs_list=self.find_photo(lists)
                self.photo_load(name,addrs_list)
            elif i==1:
                flag+=45
                lists=self.find_adrs(str(flag))
                addrs_list=self.find_photo(lists)
                self.photo_load(name,addrs_list)
            else:
                flag+=50
                lists=self.find_adrs(str(flag))
                addrs_list=self.find_photo(lists)
                self.photo_load(name,addrs_list)
        print(self.znum,self.num,self.enum)
    

if __name__=='__main__':
    a=empressive_bag()
    a.main()
        
    
