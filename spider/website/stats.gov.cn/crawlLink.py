#!coding: utf-8
import os
import requests
import sys
import time
from lxml import etree
from urlIndex import indexOfUrls

if os.name == "posix":
    ENCODE = "utf-8";
    MKDIR = "mkdir -p "
elif os.name == "nt":
    ENCODE = "gb2312";
    MKDIR = "mkdir "

def crawlAndDump(url, filename):

    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        return

    headers = {
        "Host": "www.stats.gov.cn",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Referer": "http://www.stats.gov.cn/images/style.css",
    }

    filename = filename.replace('"', " ");
    filename = filename.replace("'", " ");

    try:
        html = requests.get(url, headers=headers).content;
    except:
        sys.exit("\033[31M [ERROR]crawl " + url + "\033[0m");

    print "\033[34m [DUMP] create file " + filename.decode(ENCODE).encode("utf-8") +"\033[0m";
    wp = open(filename,"w");
    wp.write(html);
    wp.close();
    time.sleep(1);


def parseCatalogLink(url, filename):
    print url;

    lastName = filename.split("/")[-1];
    currentPath = "/".join(filename.split("/")[:-1]);

    print "\033[32m [Parse] "+filename.decode(ENCODE).encode("utf-8")+"\033[0m";
    html = open(filename,"r").read();
    tree = etree.HTML(html);

    if "sjjd" in filename:
        catalog = tree.xpath("//ul[@class='center_list_cont']/li[not(@class)][position()<last()]");

    elif "rdpcgb"  in filename or "rkpcgb" in filename or "qttjgb" in filename:
        catalog = tree.xpath("//ul[@class='center_ul_list']/li[not(@class)][position()<last()]");

    else:
        catalog = tree.xpath("//ul[@class='center_list_contlist']/li[not(@class)][position()<last()] ")


    for li in catalog:

        if "sjjd" in filename:
            link = li.xpath("span/a/@href")[0].encode("utf-8");
            title = li.xpath("span/a/font/text()")[0].encode(ENCODE);
        elif "fbhwd" in filename:
            link = li.xpath("span//a/@href")[0].encode("utf-8");
            title = li.xpath("span//a/text()")[0].encode(ENCODE);
        else:
            link = li.xpath("a/@href")[0].encode("utf-8");
            title = li.xpath("a/span/font[1]/text()")[0];
            title = title.replace(u"\u2014", "");
            title = title.encode(ENCODE);


        if link[0] == "/":
            link = "http://www.stats.gov.cn" + link;
        elif "http://" in link:
            pass;
        else:
            link = url + link;

        print title;
        print link

        


    #if filename == "统计数据/年度统计公报/ndtjgb":
    #print url
    #   sys.exit(2)

        crawlAndDump(link,  currentPath + "/" + title +".html")





if __name__ == "__main__":
    for L1 in indexOfUrls:
    
        L1_name = L1.decode("utf-8").encode(ENCODE);
        #print L1_name;
    
    
        for L2 in indexOfUrls[L1]:
    
            L2_name = L2.decode("utf-8").encode(ENCODE);
            L3_link = indexOfUrls[L1][L2];
            L3_name = L3_link.split("/")[-2]
    
            dir_name = L1_name + "/" + L2_name;
            file_name = dir_name + "/" + "catalog_" + L3_name + ".html";
    
    
            if not os.path.exists(dir_name):
                print  MKDIR + "'" + dir_name.decode(ENCODE).encode("utf-8") + "'";
                os.system( MKDIR + '"' + dir_name + '"');
    
            if os.path.exists(file_name) and os.path.getsize(file_name) != 0:
                print file_name + " is exists";
                pass
            else:
                crawlAndDump(L3_link, file_name);

            #if file_name == "统计数据/其他统计公报/qttjgb":
            parseCatalogLink(L3_link, file_name);

