import json, os
import collections
from lxml import etree
import requests
from requests.exceptions import RequestException
from multiprocessing import Process, Pool

# 判断页面的请求状态来做异常处理，正常相应则返回网页内容
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        else:
            return None
    except RequestException:
        return None

# 解析交易的具体信息并提取有用信息保存
def parse_one_page(address, filename):
    url = 'https://etherscan.io/tx/' + address
    html = get_one_page(url)
    page = etree.HTML(html)
    tx_dict = collections.OrderedDict()
    tx_dict['txHash'] = address
    tx_dict['txStatus'] = page.xpath('//span[contains(@title, "A Status code indicating if the top-level call succeeded or failed")]/font/text()')[0]
    tx_dict['blockConfirm'] = page.xpath('//span[contains(@title, "No of Blocks")]/text()')[0].split(' ')[0]
    tx_dict['gasLimit'] = page.xpath('//span[contains(@title, "amount of GAS supplied")]/text()')[0].strip()
    tx_dict['gasUsed'] = page.xpath('//span[contains(@title, "amount of gas used")]/text()')[0].strip('\n')
    tx_dict['gasPrice'] = '.'.join(page.xpath('//span[contains(@title, "price offered")]/text()')).strip('\n')
    tx_dict['actualTxFee'] = ','.join(page.xpath('//span[contains(@title, "Gas Price * Gas Used")]/text()')).strip()
    tx_dict['inputData'] = page.xpath('//textarea/text()')
    print(tx_dict)
    write_tx_dict(tx_dict,filename)

# 创建txt文件存储数据, 如果不存在就新建，如果存在就清空文件
def create_txt_file(filename):
    f = open(filename, 'w')
    f.truncate()

# 数据写入txt文件中
def write_tx_dict(tx_dict,filename):
    with open(filename, 'a+',encoding='utf-8',errors='ignore') as f:
        val_list = [val for val in tx_dict.values()]
        temp = val_list[0:-1]
        temp.extend(val_list[-1])
        f.write(' '.join(temp) + '\n')

# (txCount>=25)解析合约账户的交易记录页面，返回每页的交易地址的集合（每页最多50笔交易）
def get_contracts_txAddress(address, id):
    base_url = 'https://etherscan.io/txs'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    params = {'a':address, 'p':id}
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except Exception:
        return None

# (txCount<25)解析合约账户的信息，返回交易地址集合
def get_contract_txAddress(html):
    address_list = []
    page = etree.HTML(html)
    items = page.xpath('//tr/td[1]/a[@class="address-tag"]/text()')
    return items

# 解析合约账户的信息，返回合约的使用次数
def parse_contract_txCount(html):
    page = etree.HTML(html)
    txCount = int(page.xpath('//span[@rel="tooltip"]/text()')[0].split(' ')[0])
    return txCount

# 读取合约账户的交易数量，小于25则直接读取交易记录，大于25则在View All页面按页读取
def get_contract_txCount(address):
    url = 'http://etherscan.io/address/' + address
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    html = get_one_page(url)
    if html is not None:
        txCount = parse_contract_txCount(html)
        if txCount < 1:
            pass
        elif txCount < 25:
            address_list = get_contract_txAddress(html)[0:txCount-1]
            filename = "F:/python/etherscan/transactions/" + address + ".txt"
            create_txt_file(filename)
            for address in address_list:
                parse_one_page(address, filename)
        else:
            pass

if __name__=='__main__':
    # data = get_one_page('http://www.baidu.com')
    # print(data.text.encode(data.encoding).decode('utf-8'))
    address = '0x0d793f640Ad69c3B58c4Bfe771415d4881a0490F'
    address_list = get_contract_txCount(address)


