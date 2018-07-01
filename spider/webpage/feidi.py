#coding: utf-8
import time
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

#get the ten timestamp by hand
timestamp = [];
timestamp.append(1528183237000);
timestamp.append(1528182241000);
timestamp.append(1528181325000);
timestamp.append(1528178728000);
timestamp.append(1528176047000);
timestamp.append(1528170915000);
timestamp.append(1528168311000);
timestamp.append(1528166419000);
timestamp.append(1528164928000);
timestamp.append(1528163207000);


def sendToFeidi(timestamp):
    url = "http://data.news.21fid.com/fidnews/v1/myAjax/getContentByTime";

    #make the http header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Host": "data.news.21fid.com",
        "Referer": "http://www.21fid.cn/",
        "Origin": "http://www.21fid.cn",
    }
    
    #make the http post data
    data = {
            "channelId" : "6",
            #"beginTimeLong" : timestamp,
    }

    #send the post request
    rep = requests.post(url, data=data, headers=headers);
    res = json.loads(rep.content);

    #parser the json and get the key path
    #pprint(res["page"]["dataList"]);
    dataList = res["page"]["dataList"];

    #look every per dataList;
    for i in range(len(dataList)):
        print "第" + str(i+1) + "条"
        #print dataList[i].keys();
        print "================================================="
        try:
            if dataList[i]["title"] != None:
                print "标题:" + dataList[i]["title"].encode("utf-8");
            if dataList[i]["createdBy"] != None:
                print "作者:" + dataList[i]["createdBy"].encode("utf-8");
            print dataList[i]["description"].encode("utf-8");
        except:
            pass

        print
        print


page = 0

for i in timestamp:
    page += 1;

    print "******************************************************"
    print "***                    第"+str(page)+"页                      ***"
    print "******************************************************"
    sendToFeidi(i);
    print
    print
    print
    print
    print
    time.sleep(1);

