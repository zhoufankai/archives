# coding: utf8

import csv
import json

"""
考题1：按规则转换如图结果相同的json
"""

def assign_state(state_dict, row_item, specific_level):
    """
    赋值到指定节点
    """
    if not state_dict:
        return False

    temp_dict = state_dict
    status = 1
    level = 0
    while status:
        for k, item in temp_dict.items():
            level += 1
            if level == specific_level:
                # 如果是同一个层，则append都最后一个位置
                item.append({row_item: []})
                status = 0
                break
            else:
                if not item:
                    status = 0
                    break
                # 不是同一层的时候, 取最后一个数据进行迭代赋值
                temp_dict = item[-1]
                break
    return state_dict


def csv2json(file_path):
    """
    解析csv，按照指定规则存放到dict
    """
    state_dict = dict()
    with open(file_path, "rb") as csvFile:
        spamreader = csv.reader(csvFile, delimiter=",", quotechar='"')
        for row in spamreader:
            for level, row_item in enumerate(row):
                if row_item:
                    row_item = row_item.decode("utf8")

                if level == 0 and row_item:
                    # 第一个节点
                    state_dict[row_item] = []
                    continue
                
                if row_item:
                    # 如果位置有值，把该值当为key，赋值指定的层次
                    assign_state(state_dict, row_item, level)

    return json.dumps(state_dict)


file_path = "./history.csv"
state_json = csv2json(file_path)
print state_json

