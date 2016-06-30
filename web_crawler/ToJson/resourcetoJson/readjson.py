#coding:utf-8
import json



#解决一定的中文编码问题
import __init__
__init__.setEncoding()

fin = file("place.json")

for eachLine in fin:
    line = eachLine.strip().decode("utf-8")
    js = None
    try:
        js = json.loads(line)
        print json.dumps(js,ensure_ascii=False)[1]
    except Exception,e:
        print 'bad Line'
        continue
