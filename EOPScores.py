#EOP网站曲谱下载
import os
import requests
import json
import re
from bs4 import BeautifulSoup
import EOPsites

Basepath=r'E:\EOPScores'
finished=0
total=0
totalimg=0
def main():
    print("请选择下载类型")
    print('0=流行 1=影视 2=经典 3=动漫 4=儿歌 5=练习曲 6=轻音乐 7=原创 8=民乐 9=其他')
    key=int(input())
    global Basepath
    Basepath=os.path.join(Basepath,EOPsites.GetClass(key))
    if not os.path.exists(Basepath):
        os.mkdir(Basepath)
    Basesite=EOPsites.SelectClass(key)
    ParseBasepage(Basesite)
def AutoGet(url,**param):
    times=0
    while times<5:
        if param==None:
            try:
                r=requests.get(url,timeout=10)
                return r
            except:
                times+=1
        else:
            try:
                r=requests.get(url,params=param,timeout=10)
                return r
            except:
                times+=1
    raise('error')
def ParseBasepage(Basesite):
    request=AutoGet(Basesite)
    HtmlText=re.sub('[\n\t]*','',request.text)
    HtmlContent=BeautifulSoup(HtmlText,features="html.parser")
    #f=open(r'f:\EOPScores\base.html',encoding='utf-8')
    #HtmlText=re.sub('[\n\t]*','',f.read())
    #HtmlContent=BeautifulSoup(HtmlText)
    #f.close()
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
def ParseAnypage(site,page):
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
            #s.img=i.contents[1].contents[1].contents[1].contents[1].contents[0]['src']
            s.descriptioin=i.contents[3].contents[1].contents[2]
            mode=str(i.contents[3].contents[1].contents[3])
            if 'stave' in mode:
                s.wuxian=True
            if 'num' in mode:
                s.jian=True
        except:pass
        #print(s.img)
        s.no=re.sub('^0*','',s.no_origin)
        s.href='https://www.everyonepiano.cn'+s.href
        s.descriptioin=s.descriptioin.replace(' ','')
        #print('编号：{}'.format(s.no))
        #print('标题：{}'.format(s.title))
        #print('作者：{}'.format(s.artist))
        #print('描述：{}'.format(s.descriptioin))
        #print('网页链接：{}'.format(s.href))
        #print('是否有五线谱：{}'.format(s.wuxian))
        #print('是否有简谱：{}'.format(s.jian))
        #print()
        #SaveJSON(s)
        s=ParseScorepage(s)
        if s.available==True:
            SaveJSON(s)
            DownloadScore(s)
        else:
            print(s.no+'下载失败！')
def SaveJSON(s):
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
    #print('{}.json saved!'.format(s.no))
def DownloadScore(s):
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
def ParseScorepage(s):
    r=AutoGet(s.href)
    HtmlText=re.sub('[\n\t]*','',r.text)
    #HtmlContent=BeautifulSoup(HtmlText,features="html.parser")
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
class score:
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

if __name__=='__main__':
    main()
    print('=====下载完成=====')
    input()

