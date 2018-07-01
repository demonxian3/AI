#!coding: utf-8
import os
import requests
import sys
import time
from lxml import etree
from urlIndex import indexOfUrls



def crawlAndDump(url, filename):

    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        return;

    headers = {
        #"Host":"www.sac.net.cn",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0",
    }

    try:
        ss = requests.Session();
        html = ss.get(url, headers=headers).content;
        #html = requests.get(url, headers=headers).content;
    except:
        sys.exit("\033[31M [ERROR]crawl " + url + "\033[0m");

    print "\033[34m [DUMP] create file " + filename +"\033[0m";

    wp = open(filename,"w");
    wp.write(html);
    wp.close();
    time.sleep(1);


def parseCatalogLink(url, filename):
    
    lastName = filename.split("/")[-1];
    currentPath = "/".join(filename.split("/")[:-1]);
    currentURL  = "/".join(url.split("/")[:-1]) + "/";

    print "\033[32m [Parse] "+filename+"\033[0m";
    html = open(filename,"r").read();
    tree = etree.HTML(html);

    print currentURL;
    catalog =  tree.xpath("//a[contains(@href,'html')]");


    for li in catalog:
        link = li.xpath("@href")[0];
        title = li.xpath("text()")[0].encode("utf-8");

        if not "http" in link:
            link = currentURL + link;

        print title;
        print link;

        title = title.replace("/","|");
        crawlAndDump(link,  currentPath + "/" + title +".html")





if __name__ == "__main__":
    for L1 in indexOfUrls:
    
        L1_name = L1.decode("utf-8").encode("utf-8");
    
        for L2 in indexOfUrls[L1]:
    
            L2_name = L2.decode("utf-8").encode("utf-8");
            L3_link = indexOfUrls[L1][L2];
            L3_name = L3_link.split("/")[-2]
    
            dir_name = L1_name + "/" + L2_name;
            file_name = dir_name + "/" + "catalog_" + L3_name + ".html";
    
    
            if not os.path.exists(dir_name):
                print "mkdir -p '" + dir_name + "'";
                os.system("mkdir -p '" + dir_name + "'");
    
    
            if os.path.exists(file_name) and os.path.getsize(file_name) != 0:
                print file_name + " is exists";
                pass
            else:
                crawlAndDump(L3_link, file_name);

            parseCatalogLink(L3_link, file_name);

