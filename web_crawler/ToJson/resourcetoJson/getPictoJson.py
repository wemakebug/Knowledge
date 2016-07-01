# -*- coding:utf-8-*-

'''
    #找到资源文件中所有的图片路径
    #读取已抓取的json文件
    #将json文件的每一行都与相应的图片匹配
    #将十个图片的绝对路径放入json文件中
    #暂时以地名为读取目标
'''

import json

def IsSubString(SubStrList,Str):
    '''
    #判断字符串Str是否包含序列SubStrList中的每一个子字符串
    #>>>SubStrList=['F','EMS','txt']
    #>>>Str='F06925EMS91.txt'
    #>>>IsSubString(SubStrList,Str)#return True (or False)
    '''
    flag=True
    for substr in SubStrList:
        if not(substr in Str):
            flag=False

    return flag
#~ #----------------------------------------------------------------------
def GetFileList(FindPath,FlagStr=[]):
    '''
    #获取目录中指定的文件名
    #>>>FlagStr=['F','EMS','txt'] #要求文件名称中包含这些字符
    #>>>FileList=GetFileList(FindPath,FlagStr) #
    '''
    import os
    FileList=[]
    FileNames=os.listdir(FindPath)
    if (len(FileNames)>0):
        for fn in FileNames:
            if (len(FlagStr)>0):
                #返回指定类型的文件名
                if (IsSubString(FlagStr,fn)):
                    #fullfilename=os.path.join(FindPath,fn)
                    fullfilename = FindPath+"\\"+fn.replace("?","")
                    FileList.append(fullfilename)
                else:
                    #默认直接返回所有文件名
                    #fullfilename=os.path.join(FindPath,fn)
                    fullfilename = FindPath+"\\"+fn.replace("?","")
                    FileList.append(fullfilename)

    #对文件名排序
    if (len(FileList)>0):
        FileList.sort()
    return FileList

#获取相应地名的图片的绝对路径
def get_absolute_path(fileList,cityname):
    pathList =[]
    for i in fileList:
        city_path = unicode(i,"gbk")
        result_find =city_path.find(cityname)
        if (result_find)!=-1:
            pathList.append(city_path)
    return pathList


#读取地名信息json文件,并将图片的绝对路径加入进去
def read_placeJson(fileList):
    fin = file(r'G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\place.json')
    fout = open(r'G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\place2.json','a')
    #cityList = []
    placeIndex =0
    for eachLine in fin:
        line = eachLine.strip().decode('utf-8')
        js_read = None
        try:
            js_read =json.loads(line)
            for index in js_read:
                #cityList.append(index)
                jDict = js_read[index]  
                pathList = get_absolute_path(fileList, index)
                for num in range(len(pathList)):
                    jsonname = "Img"+str(num)
                    jsonvalue = pathList[num]
                    jDict[jsonname] = jsonvalue
            outStr = json.dumps(js_read,fout, ensure_ascii=False)
            fout.write(outStr.strip().encode('utf-8')+'\n')
            placeIndex +=1
            print (u"已插入第%d个地名的图片" %placeIndex)
        except Exception,e:
            print "bad Line"
            continue
    fin.close()
    fout.close()


#尝试写入文件中查看中文导入情况
def check_result(fileList,cityname):
    fin = open('test.txt','wb')
    for i in fileList:
        city_path = unicode(i,"gbk")
        result_find =city_path.find(cityname)
        if (result_find)!=-1:
            fin.write(i)
            fin.write("\n")
    fin.write("\n")
    fin.close()

if __name__ == '__main__':
    fileList = GetFileList("G:\knowledge graph\search_Knowledge v0.2\sources\placePic",'jpg')
    #cityList = read_placeJson()
    read_placeJson(fileList)
    #check_result(fileList,cityName)
    

    
    