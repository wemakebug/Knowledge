# -*- coding:utf-8-*-

'''
    #构建一个人物关系json文件
    #读取明星txt文件，判断页面是否能提取关系
    #如果能提取出关系，则提出来，保存至json文件中
    #如果不能，则直接跳过
    #每个关系独立存放
    #将关系导入图数据库
'''
import httplib
import urllib2
import json
from bs4 import BeautifulSoup


#搜索链接
url = "http://baike.baidu.com/search/word?word=" 

#解决一定的中文编码问题
import __init__
__init__.setEncoding()

#读取本地明星文件夹
def readMan():
    fileman = open(r"G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\man.txt","r")
    lines = fileman.readlines()
    return lines

#抽取明星关系操作
class ScrapmanRelation():
    def __init__(self):
        self.basicname =[]
        self.basicvalue = []
    
    #获得页面信息
    def get_request_direct(self,searchUrl):
        httplib.HTTPConnection.debuglevel = 1
        request = urllib2.Request(searchUrl)
        request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")  
        request.add_header("Connection", "Keep-Alive")
        opener = urllib2.build_opener()
        f = opener.open(request,timeout=60)
        html = f.read()
        return html
    
    #获取明星关系信息
    def matchResult_relation(self,html):
        soup_relation = BeautifulSoup(html,"html.parser")
        match_relation1 = soup_relation.find_all("div", class_="star-info-block relations")
        if len(match_relation1) == 0:
            print "此明星无明显明星关系"
            return
        else:         
            soup_relation2 = BeautifulSoup(str(match_relation1),"html.parser")
            match_relation2 = soup_relation2.find_all("div",class_="name")
            for i in match_relation2:
                string_relation = i.stripped_strings
            #将关系存入数组中
                index = 0
                for s in string_relation:
                    #解决Unicode字符串问题
                    s = s.decode("unicode_escape")
                    if index == 0:
                        self.basicname.append(s)
                    else:
                        self.basicvalue.append(s)  
                    index += 1  
        
    #形成json文档
    def getJson(self,man):
        #基本关系录入
        jsonDict = {}
        number = 0
        if len(self.basicname)>len(self.basicvalue):
            number = len(self.basicvalue)
        else:
            number = len(self.basicname)
        print ("此明星有%d个关系"%number)
        for itemjson in range(number):
            jsonname = self.basicname[itemjson]
            jsonvalue = self.basicvalue[itemjson]
            if jsonDict.has_key(jsonname):
                jsonDict[jsonname] = jsonDict[jsonname] +","+jsonvalue
            else:
                jsonDict[jsonname] = jsonvalue
            
        jsonData = json.dumps(jsonDict)
        jsontest = json.loads(jsonData)
        
        
        #构建整体明星关系
        jsonDict2 ={}
        jsonDict2[str(man).strip('\n')] = jsonDict
        jsonData2 = json.dumps(jsonDict2)
        jsontest2 = json.loads(jsonData2)

        #写入json文件中
        filewrite = open('manrelation.json','a')
        filewrite.write("\n")
        json.dump(jsontest2,filewrite,ensure_ascii=False)
        filewrite.close()
        self.basicname = []
        self.basicvalue = []        
        return jsontest2
            
        
if __name__ == '__main__':
    man = ScrapmanRelation()
    lines = readMan()
    i = 0
    for line in lines:
        i = i+1
        if  i <=5301:
            continue
        searchUrl = url + line
        print searchUrl
        request = man.get_request_direct(searchUrl)
        man.matchResult_relation(request)
        man.getJson(line)
        print ("提取第%d个明星"%i)
    










