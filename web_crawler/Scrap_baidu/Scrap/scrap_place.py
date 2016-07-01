#coding:utf-8

import urllib2 
import re 
import json
from bs4 import BeautifulSoup

#解决一定的中文编码问题
import __init__
__init__.setEncoding()


#搜索链接
url = "http://baike.baidu.com/search/word?word=" 

#搜索参数


#################################读取本地地名文件#######################
def readplace():
    fileplace = open("placename.txt","r")
    lines = fileplace.readlines()
    return lines

class ScrapPlace():
    def __init__(self):
        self.basicname = []
        self.basicvalue = []
        
    def get_request_direct(self,searchUrl): 
        import httplib  
        httplib.HTTPConnection.debuglevel = 1  
        request = urllib2.Request(searchUrl)
        request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")  
        request.add_header("Connection", "Keep-Alive")  
        opener = urllib2.build_opener()  
        f = opener.open(request)  
        html = f.read()
        return html    
    
    
############################获取地区简介###############################
    def matchResult_Introdution(self,html):
        soup_breIntrodution = BeautifulSoup(html,"html.parser")
        macthes_brief = soup_breIntrodution.findAll("div",class_ = "lemma-summary")
        
        #去掉HTML标签
        if len(macthes_brief)==0:
            return " "
        i = macthes_brief[0]
            
        string_brief = i.stripped_strings
        string_all=" "
        for s in string_brief:
            substring = unicode(str(s))
            if substring[0] == '[':
                continue
            string_all  =string_all + substring    
        #写入文件内
        #self.writehtml(string_all)
        
        return string_all
        
#####################获取地区详细信息###################################
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
        jsonDict["城市简介"] = string_brief
        number = 0;
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
        filewrite = open('place.json','a')
        filewrite.write("\n")
        json.dump(jsontest2,filewrite,ensure_ascii=False)
        filewrite.close()
        self.basicname = []
        self.basicvalue = []
        return jsontest2
        
    #分析网页用
    def writehtml(self,html):
        fileWriteObj = open("html.txt", 'w') 
        fileWriteObj.write(html)
        fileWriteObj.close()
        
        
if __name__ == '__main__':
    s = ScrapPlace()
    lines = readplace()
    i = 0
    for line in lines:
        i = i+1
        if i ==1 or i <=2222:
            continue
        searchUrl = url + line
        #print str(line)
        print searchUrl
        request = s.get_request_direct(searchUrl)
        string_brief = s.matchResult_Introdution(request)
        s.matchResult_Info(request)
        s.getJson(string_brief,line)
        
        print i
    
    
    
    