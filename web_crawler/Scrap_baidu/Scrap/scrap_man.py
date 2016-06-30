#coding:utf-8

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

#抽取明星信息操作
class ScrapMan():
    def __init__(self):
        self.basicname = []
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
    
    #获取明星基本信息
    def matchResult_Introdution(self,html):
        soup_breIntrodution = BeautifulSoup(html,"html.parser")
        macthes_brief = soup_breIntrodution.find_all("div", class_ = "lemma-summary")
        if len(macthes_brief) == 0:
            return " "
        
        i = macthes_brief[0]
        #去掉HTML标签
        string_brief = i.stripped_strings
        
        string_all = ""
        for s in string_brief:
            substring = unicode(str(s))
            if substring[0] =="[":
                continue
            string_all = string_all + substring
            
        return string_all
    
    #获取明星详细信息
    def matchResult_Info(self,html):
        soup_baseInfo = BeautifulSoup(html,"html.parser")
        macth_basicInfo1 = soup_baseInfo.find_all("dt", class_="basicInfo-item name")
        macth_basicInfo2 = soup_baseInfo.find_all("dd", class_="basicInfo-item value")
        
        for i in macth_basicInfo1:
            for s in i.stripped_strings:
                s = unicode(str(s))
                self.basicname.append(s)
        
        for a in macth_basicInfo2:
            oneinfo =""
            for h in a.stripped_strings:
                h = unicode(str(h))
                oneinfo = oneinfo + h
            self.basicvalue.append(oneinfo)
            
            
    ############形成json格式文档##########################
    def getJson(self,string_brief,place):
        jsonDict = {}
        jsonDict["个人基本信息"] = string_brief
        number = 0
        if len(self.basicname)>len(self.basicvalue):
            number = len(self.basicvalue)
        else:
            number = len(self.basicname)
        for itemjson in range(number):
            jsonname = self.basicname[itemjson]
            jsonvalue = self.basicvalue[itemjson]
            jsonDict[jsonname] = jsonvalue
        jsonData = json.dumps(jsonDict)
        jsontest = json.loads(jsonData)
        #for item in jsontest.items():
            #print '"'+item[0]+'"'+':"'+item[1]+'"'    
        
        jsonDict2 ={}
        jsonDict2[str(place).strip("\n")] = jsonDict
        jsonData2 = json.dumps(jsonDict2)
        jsontest2 = json.loads(jsonData2)
        filewrite = open('man.json','a')
        filewrite.write("\n")
        json.dump(jsontest2,filewrite,ensure_ascii=False)
        filewrite.close()
        self.basicname = []
        self.basicvalue = []
        return jsontest2
    
    #分析测试网页用
    def writeHtml(self,html):
        fileWriteObj = open("html.txt",'w')
        fileWriteObj.write(html)
        fileWriteObj.close()
        
if __name__ == '__main__':
    man = ScrapMan()
    lines = readMan()
    
    i = 0
    for line in lines:
        i = i+1
        if  i <=5948:
            continue
        searchUrl = url +line
        print searchUrl
        
        request = man.get_request_direct(searchUrl)
        string_brief = man.matchResult_Introdution(request)
        man.matchResult_Info(request)
        man.getJson(string_brief, line)
        
        print i
    
    
    
    
    
    
    
    
        












