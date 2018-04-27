import os
import json

# 使用次数大于10次的合约地址及使用次数
def find_most_use(filename, filename2):
    with open(filename, 'r+') as f:
        line = f.read().strip().split('\n')
        address_txCount = {}
        for item in line:
            item = json.loads(item)
            if int(item['txCount'])>10:
                address_txCount[item['address']] = int(item['txCount'])
    frequent_contract(address_txCount)

# 使用次数超过10次的合约排序及输出
def frequent_contract(d):
    d=sorted(d.items(), key=lambda x: x[1],reverse=True)
    with open('txt_file/address_txCount.txt', 'w+') as f:
        for i in range(len(d)):
            f.write(d[i][0]+ ':' + str(d[i][1]) + '\n')