
import json
import matplotlib.pyplot as plt
from pathlib import Path

import pandas as pd


def plot_line_graph(x, y):
    plt.plot(x, y)
    plt.xlabel('epoch')
    plt.ylabel('test_loss_bbox')
    plt.title('queryObj = 50')
    plt.grid(True)
    plt.show()
def read_dicts_from_file(inputFile):
    dicts = []
    with open(inputFile, 'r') as file:
        for line in file:
            # 从文件中读取每一行，并将其解析为字典
            try:
                dictionary = json.loads(line.strip())
                dicts.append(dictionary)
            except json.JSONDecodeError:
                print("Invalid JSON format in line:", line)
    return dicts

def findMin(dictArr):
    min_test_class_error = 100
    min_test_bbox_loss = 1
    for dic in dictArr:
        if dic['test_class_error'] < min_test_class_error:
            min_test_class_error = dic['test_class_error']
        if dic['test_loss_bbox'] < min_test_bbox_loss:
            min_test_bbox_loss = dic['test_loss_bbox']
    return min_test_class_error,min_test_bbox_loss

def processData(inputDir):
    folderPath = Path(inputDir)
    experiences = folderPath.iterdir()
    row_names = []
    col_names = ['分类错误率','边界框差异度量']
    col_1 = [] # 分类错误率
    col_2 = [] # 边界框差异度量
    # 遍历文件夹中的每个子文件和文件夹
    for item in experiences:
        inputFile = inputDir + "/" + item.name + "/log.txt"
        row_names.append(item.name)
        min_test_class_error,min_test_bbox_loss = findMin(inputFile)
        col_1.append(min_test_class_error)
        col_2.append(min_test_bbox_loss)
    data = []
    data.append(col_1)
    data.append(col_2)
    df = pd.DataFrame(data,index=row_names,col_names = col_names)
    # 显示表格
    print(df)
# # 使用示例
# dicts_array = read_dicts_from_file(inputFile)
# x = []
# y = []
# for dic in dicts_array:
#     x.append(dic['epoch'])
#     y.append(dic["test_loss_bbox"])
# plot_line_graph(x,y)
# # print(dicts_array)
# inputFile = '../models/tunedModels/exp1_8heads_50query/log.txt'
inputDir = '../models/tunedModels'
processData(inputDir)

