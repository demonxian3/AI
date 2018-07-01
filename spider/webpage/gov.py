#coding: utf-8
import time
import requests
import xml.dom.minidom
from bs4 import BeautifulSoup
from xml.dom.minidom import parse

def crawlLink(url, title):
    print title;

    rep = requests.get(url);
    html = rep.content;
    soup = BeautifulSoup(html, "html.parser");

    date = soup.select(" div.content_subtitle ");
    aritcle = soup.select(" div#content ")

    dateContent = date[0].text.encode("utf-8");
    aritcleContent = aritcle[0].text.encode("utf-8");

    wp = open(title.decode("utf-8").encode("gb2312")+".txt","w");
    wp.write(dateContent);
    wp.write(aritcleContent);
    wp.close()

url = "http://www.fzb.gd.gov.cn/business/htmlfiles/gdsfzb/s134/list.html";
rep = requests.get(url);

#crawl xml info from javascript code
wp = open("gov.xml", "w");
xmldata = rep.content.split("sXml")[1].split("'")[1].split("'")[0];
wp.write(xmldata);
wp.close();

#use xml modules to parse the xml data
DOM = xml.dom.minidom.parse("gov.xml");
ROOT = DOM.documentElement;
INFOS = ROOT.getElementsByTagName("INFO");



#traverse every per <info> tag 
for INFO in INFOS:
    headLink = "http://www.fzb.gd.gov.cn/publicfiles/business/htmlfiles/"
    Title = INFO.getElementsByTagName("Title")[0].childNodes[0].data.encode("utf-8");
    Link  = INFO.getElementsByTagName("InfoURL")[0].childNodes[0].data;
    print Title;
    print headLink + Link;
    crawlLink(headLink+Link, Title);


