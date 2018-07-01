#!coding: utf-8
import os
import requests
import sys
import time
from lxml import etree
from color import Color
from urlIndex import indexOfUrls

c = Color();

if os.name == "posix":
    ENCODE = "utf-8";
    MKDIR = "mkdir -p "

elif os.name == "nt":
    ENCODE = "gb2312";
    MKDIR = "mkdir "



def ENC_UTF8(string):
    try:
        string = string.decode(ENCODE).encode("utf-8");
    except:
        pass;

    return string;



def ENC_GB2312(string):
    try:
        string = string.decode("utf-8").encode(ENCODE);
    except:
        pass;

    return string;



def stripBlank(string):
    string = string.replace("\t", "").replace("\n", "").replace("\r","").replace(".","").replace(" ","");
    string = string.replace(u"\xb7", "").replace(":","");
    return string;


def crawlAndDump(url, filename):

    c.show("[Visit] " + url, "green");

    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        c.show("[Warning] "+ENC_UTF8(filename) +"is exist", "yellow");
        return

    headers = {
        "Host": "211.157.104.86:8080",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Referer": "http://211.157.104.86:8080/ogic/view/govinfo.jhtml",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Cookie":"_gscu_889343035=28895705jcy3d943; _gscbrs_889343035=1",
    }

    filename = filename.replace('"', " ");
    filename = filename.replace("'", " ");

    try:
        html = requests.get(url, headers=headers).content;
    except:
        c.show("[Error] "+ url , "red");
        sys.exit();

    c.show("[Dump] " + ENC_UTF8(filename), "blue");

    wp = open(filename,"w");
    wp.write(html);
    wp.close();

    time.sleep(1);





def parseCatalogLink(url, filename):

    lastName = filename.split("/")[-1];
    currentPath = "/".join(filename.split("/")[:-1]);

    c.show("[Parse] " + ENC_UTF8(filename), "green");
    
    html = open(filename, "r").read();
    tree = etree.HTML(html);


    if "catalog_view" in filename:
        catalog = tree.xpath("//table[@id='mytable']/tr[position()>=2]");
        
        for tr in catalog:

            title = tr.xpath("td/a/text()")[0];
            title = stripBlank(title).encode(ENCODE);
            link  = tr.xpath("td/a/@rel")[0];

            if link[0] == '/':
                link = "http://211.157.104.86:8080" + link;
            else:
                pass

            link = link.replace("subview","detail");
            
            crawlAndDump(link,  currentPath + "/" + title +".html")




    elif "catalog_xwfb" in filename \
            or "catalog_wqyzdfxx" in filename \
            or "catalog_wqyz12330rx" in filename :

        catalog = tree.xpath("//li[@style]/a");
        
        for tr in catalog:
            
            title = tr.xpath("text()")[0];
            title = stripBlank(title).encode(ENCODE);
            link = tr.xpath("@href")[0];
        
     
            if "catalog_xwfb" in filename:
                prefix = "http://www.sipo.gov.cn/xwfb/";
            elif "catalog_wqyzdfxx" in filename:
                prefix = "http://www.sipo.gov.cn/zfwq/wqyzdfxx/";
            elif "catalog_wqyz12330rx" in filename:
                prefix = "http://www.sipo.gov.cn/zfwq/wqyz12330rx/"

            if "http://" not in link:
                link = prefix + link;

            crawlAndDump(link, currentPath + "/" + title + ".html");




    elif  "catalog_wqyzdfxx" in filename:
        catalog = tree.xpath("//li[@style]/a");

        for tr in catalog:
            title = tr.xpath("text()")[0];
            title = stripBlank(title).encode(ENCODE);
            link = tr.xpath("@href")[0];
        
            if "http://" not in link:
                link = "http://www.sipo.gov.cn/zfwq/wqyzdfxx/" +link;

            crawlAndDump(link, currentPath + "/" + title + ".html");
            


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
            
            
            if "index.jhtml" in L3_link:
                c.show("[Warning] Redirect the url link", "yellow");
                L3_link = 'http://211.157.104.86:8080/ogic/view/govinfo.jhtml';

    
            """ create mulit layer directory  """
            if not os.path.exists(dir_name):
                c.show("[Command] " + MKDIR + "'" + ENC_UTF8(dir_name) + "'", "cyan");
                os.system( MKDIR + '"' + dir_name + '"');


            """ create catalog file if not exist """
            if os.path.exists(file_name) and os.path.getsize(file_name) != 0:
                c.show("[Warning] " + ENC_UTF8(file_name) + " is exist", "yellow");
                pass
            else:
                crawlAndDump(L3_link, file_name);


            """ parse the catalog file and get link to visit """
            parseCatalogLink(L3_link, file_name);


