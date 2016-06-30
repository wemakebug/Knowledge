# -*- coding:utf-8-*-

'''
    #读取地名txt文件，将地名存入数组中
    #读取json文件，判断每一个元素是否有所属地区这个属性
    #若没有所属地区这个属性，则跳过
    #若有所属地区这个属性，则将其字符串提取出来
    #将所属地区字符串与地名列表进行正则表达式匹配，将所有的匹配结果提取出来
'''
import json
from py2neo import Graph


#读取地名文件，将地名存入数组中
def getplaceList():
    placeList = []
    fin = file(r"G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\placename.txt")
    for eachLine in fin:
        placeList.append(eachLine)
    return placeList   


#将提取出的所属地区与地名数组相关的地名正则匹配
def match_place(dict_condition):
    placeList = getplaceList()
    upperList =[]
    #将地名一一匹配检查
    for eachLine in placeList:
        eachLine = eachLine.strip('\n').decode('utf-8')
        #print dict_condition.find(eachLine)
        if dict_condition.find(eachLine)!= -1:
            upperList.append(eachLine)
    return upperList

#构造所属地区关系
def buildupperRelation(index,upperList):
    graph = Graph()
    tx = graph.cypher.begin()
    statement = "MATCH (a {name:{A}}), (b {name:{B}}) CREATE (a)-[:所属地区]->(b)"
    for upperPlace in upperList:
        tx.append(statement, {"A":index,"B":upperPlace})
        print "ok"
    tx.commit()
    return

#构建下级管辖区域关系
def buildlowerRelation(index,upperList):
    graph = Graph()
    tx = graph.cypher.begin()
    statement = "MATCH (a {name:{A}}), (b {name:{B}}) CREATE (a)-[:管辖区域]->(b)"
    for upperPlace in upperList:
        tx.append(statement, {"A":upperPlace,"B":index})
        print "ok"
    tx.commit()
    return

#读取json文件，将所有的所属地区的字符串提取出来，与地名数组正则匹配
def getJsonPlace():
    fin = file(r'G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\place.json') 
    condition = u"所属地区"
    for eachJsonLine in fin:
        jsonLine = eachJsonLine.strip().decode('utf-8')
        js_read = None
        try:
            js_read = json.loads(jsonLine)
            #js_one = json.dumps(js_read, ensure_ascii = False)
            for index in js_read:
                jDict = js_read[index]
                if jDict.has_key(condition):
                    #获得所属地区属性
                    dict_condition = jDict[condition]
                    #获得上级地区城市列表
                    upperList = match_place(dict_condition)
                    #构建上级所属地区关系
                    buildupperRelation(index, upperList)
                    #构建下级管辖区域关系
                    #buildlowerRelation(index, upperList)
                else:
                    continue
        except Exception:
            print "bad Line"
            continue
    fin.close()            
    
if __name__ == '__main__': 
    placeNameList =  getplaceList()
    getJsonPlace()






