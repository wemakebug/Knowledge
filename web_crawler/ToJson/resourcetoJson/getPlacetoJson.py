# -*- coding:utf-8-*-

import json
from py2neo import Graph
from py2neo import Node,Relationship

graph = Graph()
s = 0
f = open(r"G:\knowledge graph\search_Knowledge v0.2\web_crawler\resource\man2.json","r")
for line in f:
    lineone = line
    s = s+1
    #if s <= 3:
        #continue
    print s
    js = None
    try:
        js = json.loads(lineone)
        for i in js:
            place = Node("Man_name",name = i)
            graph.create(place)   
            jDict = js[i]
            for j in jDict:
                property1 = j.split()
                property1 = ''.join(property1)                  
                string = json.dumps(jDict[j],ensure_ascii=False)
                place.properties[property1] =string.replace("\"","")
            place.push()
    except Exception,e:
        print 'bad Line'
f.close()





