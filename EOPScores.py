#EOP网站曲谱下载
#By Polonium
#GitHub @Polonium84
#---Python标准库---
import os
import json
import re
#---Python第三方库---
import requests
from bs4 import BeautifulSoup
#---EOPsites.py---
import EOPsites

Basepath=r'E:\EOPScores' #保存根目录
finished=0               #下载完成数
total=0                  #总任务数
totalimg=0               #总下载图片数

def main():#主函数
    print("请选择下载类型")
    print('0=流行 1=影视 2=经典 3=动漫 4=儿歌 5=练习曲 6=轻音乐 7=原创 8=民乐 9=其他')
    key=int(input())
    global Basepath
    Basepath=os.path.join(Basepath,EOPsites.GetClass(key))
    if not os.path.exists(Basepath):
        os.mkdir(Basepath)
    Basesite=EOPsites.SelectClass(key)
    ParseBasepage(Basesite)
    print('=====下载完成=====')
    input()

def AutoGet(url,**param):#下载函数，失败后自动重试
    times=0
    while times<5:
        if param==None:
            try:
                r=requests.get(url,timeout=10)
                return r
            except:
                times+=1
        else:#有HTTP请求附加参数的情况下
            try:
                r=requests.get(url,params=param,timeout=10)
                return r
            except:
                times+=1
    raise('error')#尝试5次仍失败后抛出错误

def ParseBasepage(Basesite):#解析主版块HTML源代码
    request=AutoGet(Basesite)
    HtmlText=re.sub('[\n\t]*','',request.text)
    HtmlContent=BeautifulSoup(HtmlText,features="html.parser")
    regex=re.findall(r'\'_self\'>(\d*)</a>',HtmlText)
    pagecount=int(regex[-1])
    tagpage=HtmlContent.find('div','row EOPMusicIndexPage')
    scorecount=int(tagpage.contents[1].contents[1].string)
    print('共{}首，{}页'.format(scorecount,pagecount))
    global total
    total=scorecount
    print()
    #ParseAnypage(Basesite,42)
    for i in range(1,pagecount+1):
        print('-----开始下载第{}页-----'.format(i))
        ParseAnypage(Basesite,i)

def ParseAnypage(site,page):#解析每一页HTML源代码，一页10个曲谱
    #param={'p':page}
    request=AutoGet(site,p=page)
    HtmlText=re.sub('[\n\t]*','',request.text)
    HtmlContent=BeautifulSoup(HtmlText,features="html.parser")
    for i in HtmlContent.find_all('div','MusicIndexBox'):
        if i.has_attr('style'):continue
        s=score()
        try:
            s.no_origin=i.contents[1].contents[1].string
            s.title=i.contents[1].contents[3].string
            s.href=i.contents[1].contents[3]['href']
            s.artist=i.contents[1].contents[5].string
            s.descriptioin=i.contents[3].contents[1].contents[2]
            mode=str(i.contents[3].contents[1].contents[3])
            if 'stave' in mode:
                s.wuxian=True
            if 'num' in mode:
                s.jian=True
        except:pass
        s.no=re.sub('^0*','',s.no_origin)
        s.href='https://www.everyonepiano.cn'+s.href
        s.descriptioin=s.descriptioin.replace(' ','')
        s=ParseScorepage(s)
        if s.available==True:
            SaveJSON(s)
            DownloadScore(s)
        else:
            print(s.no+'下载失败！')

def SaveJSON(s):#保存该曲谱的基本信息
    DirPath=os.path.join(Basepath,s.title)
    if not os.path.exists(DirPath):
        try:
            os.mkdir(DirPath)
        except:
            DirPath=os.path.join(Basepath,s.no)
            if not os.path.exists(DirPath):os.mkdir(DirPath)
    JsonPath=os.path.join(DirPath,'{}.json'.format(s.no))
    with open(JsonPath,'wt+',encoding='utf-8') as f:
        text=json.dumps(s,default=score.ToJSON,sort_keys=True)
        f.write(text)

def DownloadScore(s):#下载该歌曲的所有乐谱图片
    DirPath=os.path.join(Basepath,s.title)
    if not os.path.exists(DirPath):
        try:
            os.mkdir(DirPath)
        except:
            DirPath=os.path.join(Basepath,s.no)
            if not os.path.exists(DirPath):os.mkdir(DirPath)
    url1='https://www.everyonepiano.cn/pianomusic'
    if s.jian_num >= 1:
        for i in range(1,s.jian_num+1):
            url='{0}/{1}/{2}/{3}-j-b-{4}.png'.format(url1,s.scoreserver,s.no_origin,s.no_origin,i)
            r=AutoGet(url)
            img='{0}\\简谱{1}.png'.format(DirPath,i)
            with open(img,'wb+') as f:
                f.write(r.content)
    if s.wuxian_num>=1:
        for i in range(1,s.wuxian_num+1):
            url='{0}/{1}/{2}/{3}-w-b-{4}.png'.format(url1,s.scoreserver,s.no_origin,s.no_origin,i)
            r=AutoGet(url)
            img='{0}\\五线谱{1}.png'.format(DirPath,i)
            with open(img,'wb+') as f:
                f.write(r.content)
    global finished
    global total
    global totalimg
    finished+=1
    per=finished/total
    totalimg+=(s.wuxian_num+s.jian_num)
    s1='{0:>7}下载完成！\t已完成'.format(s.no)
    s2='{}/{}'.format(finished,total).ljust(11)
    s3='{:.2%}'.format(per).ljust(8)
    s4='\t共下载{:^9}张图片'.format(totalimg)
    print(s1+s2+s3+s4)

def ParseScorepage(s):#解析乐谱页面的HTML源代码
    r=AutoGet(s.href)
    HtmlText=re.sub('[\n\t]*','',r.text)
    try:
        s.scoreserver=re.search(r'/pianomusic/(\d{3})/',HtmlText).group(1)
    except:
        s.available=False
        return s
    if s.wuxian:
        try:s.wuxian_num=int(re.search(r'五线谱预览 <small>\( 共(\d*)张 \)',HtmlText).group(1))
        except:pass
    if s.jian:
        try:s.jian_num=int(re.search(r'简谱预览 <small>\( 共(\d*)张 \)',HtmlText).group(1))
        except:pass
    return s

class score:#乐谱类，储存基本信息，并定义一个输出为json文本的函数
    no=''
    no_origin=''
    title=''
    artist=''
    href=''
    img=''
    descriptioin=''
    wuxian=False
    jian=False
    available=True
    wuxian_num=0
    jian_num=0
    scoreserver=''
    def ToJSON(self):
        return{
            'No':self.no,
            'Title':self.title,
            'Artist':self.artist,
            'Description':self.descriptioin,
            'Address':self.href,
            'HasWuxian':self.wuxian,
            'HasJian':self.jian,
            'CountOfWuxian':self.wuxian_num,
            'CountOfJian':self.jian_num,
            'ScoreServer':self.scoreserver
            }

if __name__=='__main__':#主程序入口
    main()
    

