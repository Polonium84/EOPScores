import os
import time
import json
dic={}
dic1={}
dic2={}
strTime=time.strftime('%Y_%m_%d')
dic1['数据版本']=strTime
BasePath=r'E:\EOPScores'
l=[]
for dir in os.listdir(BasePath):
    if os.path.isdir(os.path.join(BasePath,dir)) :
        key=os.path.basename(dir)
        value=len(os.listdir(os.path.join(BasePath,dir)))
        dic2[key]=value
        l.append(value)
total=0
for i in l:
    total+=i
dic1['曲谱总数']=total
dic['基本信息']=dic1
dic['曲谱信息']=dic2
jsontext=json.dumps(dic,sort_keys=True)
with open(os.path.join(BasePath,'info.json'),'wt') as f:
    f.write(jsontext)