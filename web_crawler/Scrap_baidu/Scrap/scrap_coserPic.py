#coding:utf-8

import httplib
import urllib2
import requests
from bs4 import BeautifulSoup

#搜索链接
url ="http://bcy.net/coser/detail/8284/620843"

#解决一定的中文编码问题
import __init__
__init__.setEncoding()

class scrap_coser():
    
    #初始化图片名称
    def __init__(self):
        self.works =[]
        
    #获得页面信息
    def get_request_direct(self,searchUrl):
        httplib.HTTPConnection.debuglevel = 1
        request = urllib2.Request(searchUrl)
        request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")  
        request.add_header("Connection", "Keep-Alive")
        request.add_header("Cookie"," lang_set=zh; CNZZDATA1257708097=2136948692-1464822086-http%253A%252F%252Fmoe.hao123.com%252F%7C1466657114; Hm_lvt_330d168f9714e3aa16c5661e62c00232=1464827386,1464827696,1465089544,1466658880; LOGGED_USER=q71sFjn5DUCVIT2WbsQABtc%3D%3ArkWge5EGWcmX%2BB9mOWHdbA%3D%3D; PHPSESSID=qg3v7fo9mj229ebcqk55i1niq5; mobile_set=no; Hm_lpvt_330d168f9714e3aa16c5661e62c00232=1466658929")
        request.add_header("User-Agent"," Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
        opener = urllib2.build_opener()
        f = opener.open(request,timeout=60)
        html = f.read()
        return html    
    
    
    #获取coser图片Url与名称
    def matchResult_Info(self,html):
        soup_baseInfo = BeautifulSoup(html,"html.parser")
        macth_basicInfo1 = soup_baseInfo.find_all("img", class_="detail_std detail_clickable")
        macth_basicInfo2 = soup_baseInfo.find_all("h1", class_="js-post-title")
        
        i = macth_basicInfo2[0]
        #去掉HTML标签
        string_brief = i.stripped_strings
        string_all = ""
        for s in string_brief:
            substring = unicode(str(s))
            string_all = string_all + substring
        num = 0
        for i in macth_basicInfo1:
            imgUrl =  i['src']
            imgName = string_all+str(num)+".jpg"
            self.downImg(imgUrl,r"D:\图片\动漫\cos盗图", imgName)
            num+=1
            
            
    # 下载图片
    def downImg(self,imgUrl, dirpath, imgName):
        filename = dirpath +"\\"+imgName
        try:
            res = requests.get(imgUrl, timeout=15)
            if str(res.status_code)[0] == "4":
                print(str(res.status_code), ":" , imgUrl)
                return False
        except Exception as e:
            print(u"抛出异常：", imgUrl)
            print(e)
            return False
        with open(filename, "wb") as f:
            f.write(res.content)
        return True
    
    #测试网页信息用
    def writeHtml(self,html):
        fileWriteObj = open("html1.txt",'w')
        fileWriteObj.write(html)
        fileWriteObj.close()    

if __name__ == '__main__':
    coser = scrap_coser()
    request = coser.get_request_direct(url)
    coser.matchResult_Info(request)

