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
        "Host":"www.pbc.gov.cn",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Referer": "http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html",
        "Cookie": "wzwsconfirm=b2e5dd6bffed07fb74e193d7738a7138; wzwstemplate=Nw==; wzwschallenge=-1; ccpassport=4320f9419a7bd71905c48f076a9b0d86; wzwsvtime=1529751461",
    }

    try:
        ss = requests.Session();
        html = ss.get(url, headers=headers).content;
        #html = requests.get(url, headers=headers).content;
    except:
        sys.exit("\033[31M [ERROR]crawl " + url + "\033[0m");

    print html;
    print "\033[34m [DUMP] create file " + filename +"\033[0m";

    wp = open(filename,"w");
    wp.write(html);
    wp.close();
    time.sleep(1);


def parseCatalogLink(url, filename):
    
    lastName = filename.split("/")[-1];
    currentPath = "/".join(filename.split("/")[:-1]);

    print "\033[32m [Parse] "+filename+"\033[0m";
    html = open(filename,"r").read();
    tree = etree.HTML(html);

    catalog =  tree.xpath("//td[@align='left'][@height='22']");

    print catalog

    for li in catalog:
        link = "http://www.pbc.gov.cn/" + li.xpath("font//a/@href")[0];
        title = li.xpath("font//a/text()")[0].encode("utf-8");
    

        if link[0] == "/":
            link = "http://www.stats.gov.cn" + link;
        elif "http://" in link:
            pass;
        else:
            link = url + link;

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

