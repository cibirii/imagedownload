import requests
import urllib.request as ur
from urllib.error import URLError,ContentTooShortError,HTTPError
import re
from urllib.parse import urljoin
from urllib import robotparser
import time
from urllib.parse import urlparse
import json #引入json模块，用到json.dumps()方法

# 定义要抓取的年份
# years=["2016","2015","2014","2013"]
# years=["2016","2015"]
# years=["2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]
years=["2021"]
savefile="" #构造存储文件名，即为年份，用“-”连接
for r in range(0,len(years)):
    savefile=savefile+years[r]+"-"

headers = {
    # post请求头，用Mac下的Charles抓取了网易Mumu模拟器下的Funko App
    # 很简单的post headers，没有做任何限制
    "cache-control":"no-cache",
    "content-type":"application/json",
    "content-length":"72",
    "accept-encoding":"gzip",
    "user-agent":"okhttp/3.12.1",
}

# 定义getitems()函数，提交Post请求，用于获取json返回
def getitems(url, headers, data):
    print("正在提交，请等待。。。")
    # 以下用于重复3次
    i = 0
    while i < 3:
        try:
            # 利用了requests库的post方法，文件头部已经import引入
            res = requests.post(url=url, headers=headers, data=data)
            #获取服务器返回代码，很重要，用于判断服务器状态
            print("服务器返回代码："+str(res.status_code))
            print("获取成功！！")
            return res.text
        except requests.exceptions.RequestException:
            i += 1
            print("超时（超过10秒）！重试第"+str(i)+"次")
'''
data = {
    "page":1,
    "pageCount":60,
    "type":"catalog",
    "sort":{
    "releaseDate":"desc"
    }
}
'''

# 变量data-params为post提交的参数，为json，其中的page会改为变量
# data_params={"page":1,"pageCount":60,"type":"catalog","sort":{"releaseDate":"desc"}} #针对所有的sku
#以下为2019和2020年出的产品数据
# data_params={"page":0,"pageCount":180,"type":"catalog","releaseDate":["2018","2017"],"sort":{"releaseDate":"desc"}}
#以下为2015-2018年出的产品数据 ["2016","2015","2014","2013"]
# data_params={"page":0,"pageCount":180,"type":"catalog","releaseDate":["2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"],"sort":{"releaseDate":"desc"}}
# data_params={"page":0,"pageCount":180,"type":"catalog","releaseDate":["2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"],"sort":{"releaseDate":"desc"}}
data_params={"page":0,"pageCount":180,"type":"catalog","releaseDate":["2021"],"sort":{"releaseDate":"desc"}}

# data_params["releaseDate"]=years
# 服务器网址
url = 'https://www.funko.com/api/search/terms'
# 此处itemsget为测试，data-params必须经过json.dumps()处理，服务器才会认，否则返回400.
# itemsget=getitems(url=url,headers=headers,data=json.dumps(data-params))
# print(itemsget)

# 此处的循环构造所有post提交的参数data_params，定义了一个名为data_paramstotal的list（数组），把构造出来的参数存入data_paramstotal
data_paramstotal=[]
# 变量m根据总页数设置，即range(0,x/60)，x为总SKU数
#totalsku=21354
#以下为2015-2018年出的产品数据
# totalsku=19
# pagecount=int(totalsku/data_params['pageCount'])
'''
for m in range(0,pagecount):
    data_paramstotal.append(data_params)
    data_paramstotal[m]['page']=str(m)
    print(data_paramstotal[m])
    #itemsget=getitems(url,paramstotal[m],headers)
    #itemswhole.append(itemsget)
# 修改List中的page参数
# print(data_paramstotal)
'''
# 获取总SKU数量
itemsget=getitems(url=url,headers=headers,data=json.dumps(data_params))
totalsku=json.loads(itemsget)["total"]

# pagecount为页数
pagecount=int(totalsku/data_params['pageCount'])
#pagecount=10 # 3为测试循环数
filelist=[]
for j in range(0,pagecount+10):
    data_paramstotal.append(data_params)

for m in range(1,pagecount+2): # 这里从1开始，因为0和1的值是一样的
    #paramstotal.append(params)
    time1=time.strftime('%Y-%m-%d %H:%M:%S')
    time11=time.strftime('%S')
    time111=time.strftime('%M')
    print(time1)
    data_paramstotal[m]['page']=str(m)
    print(data_paramstotal[m])
    itemsget=getitems(url=url,headers=headers,data=json.dumps(data_params))

    # 构造存储文件名
    # jsonfile='/Users/admin/Desktop/0001/funkoTest'+'-'+str(m)+'.txt'
    # filelist.append(jsonfile)
    # with open(jsonfile,'w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    #     print("正在写入文件。。。。。。")
    #     f.write(itemsget)
    # print("写入文件成功！")

    print(type(itemsget)) # 为str类型
    print(type(json.loads(itemsget))) # 为dict类型
    dictlen=len(json.loads(itemsget)["hits"]) #利用dict类型的方法，访问内容
    mm=[]# 定义python list变量
    fid=[]
    # 构造包含所有参数的dict字典，不能用list
    ss={"uid":"","type":"","title":"","referenceUrl":"","visibleDate":"","releaseDate":"","keywords":"","score":"","imageUrl":"","additionalImages":"","productCategories":"","productBrands":"","productLines":"","licenses":"","formFactors":"","productSections":"","licensors":"","exclusivity":"","features":"","events":"","characters":"","status":"","b2bStatus":"","upc":"","boxNumber":"","itemNumber":"","componentNumber":"","hobbyDbId":"","craftProductId":"","craftComponentId":"","isMultipack":"","caseQuantity":"","masterCaseQty":"","isPurchasable":"","nextIncomingDate":"","availability":"","relatedProducts":"","collectionData":"","marketValue":"","isChase":"","hasChase":"","isAssortment":"","components":"","historicPricing":"","siblings":"","isB2B":""}
    for i in range(0,dictlen): # 构造循环函数，
        # mm.append(i) # list变量添加新对象的append()方法
        # print(mm[i]) # 访问list变量内的对象
        b2b=json.loads(itemsget)["hits"][i]
        if len(b2b)>20:
            fid.append(i)
            print(len(b2b))
            print(b2b)
            
            for key,value in b2b.items():  # python 字典dict的循环方法，b2b.items()
                # print(str(key)+" | "+str(value))
                # ss[key]=str(value)  #s失败，因为s构造为list，不是dict,改为ss
                # print(type(value))
                # if key=="relatedProducts":
                #     print(type(value))
                #     print(value)
                if type(value)==list: #判断值是什么类型，如果是list，则判断长度是否为0，如果不是，则取出所有的值，组合为长字符串，返回到ss[key]中
                    if len(value)==0:
                        ss[key]=""
                    elif len(value)==1:
                        ss[key]=value[0]
                        print(value)
                    # elif key=="additionalImages":
                    #     xx=""
                    #     print(value)
                    #     for x in range(1,len(value)):
                    #         xx=xx+str(value[x])+"@"
                    #     ss[key]=xx
                    else:
                        xx=""
                        print(value)
                        for x in range(0,len(value)):
                            xx=xx+str(value[x])+"@"
                        ss[key]=xx
                elif type(value)==dict:
                    print("Dict!!!")
                    print(value)
                    ss[key]=""
                else:
                    ss[key]=value
            print(ss)
            # 取出所有值之后的ss dict字典，循环组成一个长字符串，再写入文件
            sss=""
            for key,value in ss.items():
                sss=sss+str(value).replace(":","-")+"\t"
            sss=sss+"\n" # 行尾加换行符\n

            print(sss)
            jsonfile='/Users/admin/Desktop/0002/funko'+savefile+'total-final.txt'
            with open(jsonfile,'a') as f: # 如果filename不存在会自动创建， 'a'表示写数据，不会清空文件中的原有数据，会在文件尾部增加内容！
                print("正在写入文件。。。。。。")
                f.write(sss)
            print("写入文件成功！")


    time2=time.strftime('%Y-%m-%d %H:%M:%S')
    time22=time.strftime('%S')
    time222=time.strftime('%M')
    print(time2)
    if int(time222)-int(time111)==0:
        print("耗时："+str(int(time22)-int(time11))+"秒")
    else:
        print("耗时："+str(int(time22)+60-int(time11))+"秒")
    time.sleep(3) 
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
