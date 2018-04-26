import spider.spider_contract, spider.spider_content
import os
import txt_file
import drawing

# 创建txt文件存储数据
def mknod(filename):
    if not os.path.exists(filename):
        fp = open(filename, 'w+')
        fp.close()
        return True
    else:
        fp = open(filename, 'w+')
        fp.truncate()
        return False

if __name__=='__main__':
    # 存储合约的主要信息
    content_filename = 'txt_file/contractVf.txt'
    # mknod(content_filename)
    # for i in range(1, 950):
    #     spider_content(i)
    drawing.draw_plot1(content_filename)
    drawing.draw_plot2(content_filename)
    drawing.draw_scatter(content_filename)
    contract_filename = 'txt_file/most_use_contract.txt'
    mknod(contract_filename)
    spider.spider_contract.find_most_use(content_filename, contract_filename)
