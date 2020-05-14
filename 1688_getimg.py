import os
import re
import time
import requests

num_zhutu = 0
num_sku = 0
num_xq = 0

# 1688主图下载+sku图片下载+详情图片下载
#需手动获取两个txt文本 具体内容请看截图（python初学 请大家见谅 笨方法仅供参考）

# 参数注释
# url 下载图片地址
# num 图片张数计数  第一张 命名为 1_01 第二张 1_02 方便淘宝后台上传时按文件名排序不会错乱
# filename 文件夹名字
# sku_name sku单个图片名称
def download_img(url,num,filename,sku_name): #下载图片 方法
    d = 'D:\program\python_project\\1688\\'+filename+'\\'
    print(d)
    if (num<10):
        num = '0'+str(num)
    else:
        num = str(num)
    if sku_name == '':
        path = d + '1_'+num+'.jpg'
    else:
        path = d + sku_name+'.jpg'
    try:
        if not os.path.exists(d):
            os.mkdir(d)
        if not os.path.exists(path):
            r = requests.get(url)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("第"+num+"张图片保存成功")
        else:
            print("图片已存在")
    except:
        print("图片获取失败")

# 读取txt文本内容 开始
if __name__ == '__main__':

    # 主图 sku读取文件
    fileHandler = open('3.txt', mode='r', encoding='UTF-8')
    report_lines = fileHandler.readlines()
    txt = ''
    for line in report_lines:#循环每行赋值
        txt = txt + line.rstrip()

    # 详情图读取文件
    fileHandler = open('xqimg.txt', mode='r', encoding='UTF-8')
    report_lines = fileHandler.readlines()
    xqimg_txt = ''
    for line in report_lines:  # 循环每行赋值
        xqimg_txt = xqimg_txt + line.rstrip()


# print(txt)
# 读取txt文本内容 结束
#         主图正则匹配
    results = re.findall('"original":"(http.*?jpg)',txt)
    # print(results[0])
    for res in  results:
        num_zhutu = num_zhutu + 1
        download_img(res,num_zhutu,'zhutu','')
        # time.sleep(1)
        print(res)

    # sku图片正则匹配
    results2 = re.findall('"imageUrl":"(http.*?jpg)', txt)
    results_alt = re.findall('name":"(.*?)"', txt)
    print(len(results2))
    for i in  range(len(results2)):
        num_sku = num_sku + 1

        download_img(results2[i],num_sku,'sku',results_alt[i])
        # time.sleep(1)
        # print(results2[i])

    # 详情图匹配
    results3 = re.findall('<img.*?src=\\\\\"(http.*?\.jpg)', xqimg_txt)
    # print(results3[0])
    for res3 in results3:
        num_xq = num_xq + 1
        download_img(res3, num_xq,'xq','')
        # time.sleep(1)
        # print(res3)
