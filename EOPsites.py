def SelectClass(code):
    if code==0:   #流行
        return 'https://www.everyonepiano.cn/Music-class5-%E6%B5%81%E8%A1%8C.html'
    elif code==1: #影视
        return 'https://www.everyonepiano.cn/Music-class31-%E5%BD%B1%E8%A7%86.html'
    elif code==2: #经典
        return 'https://www.everyonepiano.cn/Music-class11-%E7%BB%8F%E5%85%B8.html'
    elif code==3: #动漫
        return 'https://www.everyonepiano.cn/Music-class12-%E5%8A%A8%E6%BC%AB.html'
    elif code==4: #儿歌
        return 'https://www.everyonepiano.cn/Music-class13-%E5%84%BF%E6%AD%8C.html'
    elif code==5: #练习曲
        return 'https://www.everyonepiano.cn/Music-class14-%E7%BB%83%E4%B9%A0%E6%9B%B2.html'
    elif code==6: #轻音乐
        return 'https://www.everyonepiano.cn/Music-class16-%E8%BD%BB%E9%9F%B3%E4%B9%90.html'
    elif code==7: #原创
        return 'https://www.everyonepiano.cn/Music-class17-%E5%8E%9F%E5%88%9B.html'
    elif code==8: #民乐
        return 'https://www.everyonepiano.cn/Music-class18-%E6%B0%91%E4%B9%90.html'
    elif code==9: #其他
        return 'https://www.everyonepiano.cn/Music-class19-%E5%85%B6%E4%BB%96.html'
    else:
        raise 'NoSuchClassError'

def GetClass(code):
    if code==0:   #流行
        return '流行'
    elif code==1: #影视
        return '影视'
    elif code==2: #经典
        return '经典'
    elif code==3: #动漫
        return '动漫'
    elif code==4: #儿歌
        return '儿歌'
    elif code==5: #练习曲
        return '练习曲'
    elif code==6: #轻音乐
        return '轻音乐'
    elif code==7: #原创
        return '原创'
    elif code==8: #民乐
        return '民乐'
    elif code==9: #其他
        return '其他'
    else:
        raise 'NoSuchClassError'