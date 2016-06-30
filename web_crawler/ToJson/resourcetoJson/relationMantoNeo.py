# -*- coding:utf-8-*-

'''
    #读取已构建的关系json文件
    #将含有关系的json行提取出来，没有的舍去
    #将关系元素提取出来，将用逗号的切割开来
    #构建对应关系
'''

import json
from py2neo import Graph

#读取明星txt文件，将其存入数组中
def getManList():
    manList = []
    fin = file(r"G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\man.txt")
    for eachLine in fin:
        manList.append(eachLine)
    return manList 

#读取txt文件，查看关系中是否存在这样的明星，并将需要构建关系的元素打包成数组
def match_Man(relation_name,relation_man,relation_index,manList):
    buildList = []
    for eachline in manList:
        eachLine = eachline.strip('\n').decode('utf-8')
        if relation_man == eachLine:
            buildList.append(relation_index)
            buildList.append(relation_name)
            buildList.append(relation_man)
            print relation_index + ","+ relation_name+","+ relation_man
            buildRelation(buildList)
            
#构造明星关系
def buildRelation(buildList):
    graph = Graph()
    tx = graph.cypher.begin()
    statement = "MATCH (a {name:{A}}), (b {name:{B}}) CREATE (a)-[:«rel»]->(b)"
    tx.append(statement, {"A":buildList[0],"B":buildList[2],"rel":buildList[1]})
    print "插入ok"
    tx.commit()
    return        
    

#读取关系json文件，将所有含有关系的行提取出来，与明星数组相正则匹配
def getJsonRelation():
        fin = file(r'G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\manrelation.json')
        for eachJsonLine in fin:
            jsonLine = eachJsonLine.strip().decode('utf-8')
            js_read = None
            try:
                js_read = json.loads(jsonLine)
                for index in js_read:
                    #获得了每行关系
                    jDict = js_read[index]
                    for j_index in jDict:
                        relation_Info = jDict[j_index]
                        string =  relation_Info.split(",")
                        for relation_Info_index in string: 
                            manList = getManList()
                            match_Man(j_index, relation_Info_index , index, manList)
            except Exception:
                print "bad Line"
                continue
        

if __name__ == '__main__': 
    getJsonRelation()


        
        