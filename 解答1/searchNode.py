# coding: utf8

from changeStructure import csv2json
import json, csv

"""
考题2：以考题转换的结果为基础，实现一个key search方法
todo 如果层次比较大，考虑用spark建立倒序索引
"""

file_path = "./history.csv"
state_json = csv2json(file_path)
state_dict = json.loads(state_json)

def search(words, _res, pattern):
    connect = "."
    if isinstance(_res, list):
        if _res == []:
            return None
        for item in _res:
            for key, sub_res in item.items():
                result = search(words, item, pattern)
                if result:
                    return result
    else:
        for key, val_list in _res.items():
            if words == key:
                result = pattern + connect + words if pattern else words
                return result
            else:
                if pattern == "":
                    pattern = key
                else:
                    pattern = pattern + connect + key 

                result = search(words, val_list, pattern)
                if result:
                    return result
    
    
def find(key):
    output = search(key, state_dict, "")
    if not output:
        return (u"不存在关键字: " + key)
    else:
        return output


print(find(u"汉谟拉比法典"))
print(find(u'美洲'))

