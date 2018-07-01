#!coding: utf-8
#date: 2018-06-13
#author: demonxian3
#desc: 猪八戒API-v1.0
#env:
#       pip install jieba
#       pip install scipy
#       pip install wordcloud
#       pip install matplotlib


from Bajie import Bajie

bajie = Bajie("data/test.txt");

#加载分词字典
#bajie.addkey();
bajie.suggest(("平均","工资"));
bajie.loaddict("./dict/testdict.txt");


#切词
bajie.cut();                            #切词
bajie.wfilter("./dict/stopword.txt");   #过滤
print bajie.show("cut", split="|");     #查看切词结果
print bajie.show("wf",  split="|");     #查看过滤结果


print
print


#标注
bajie.tag();                                                #标注
bajie.wpfilter("dict/stopword.txt");                        #过滤
print bajie.show(select="tag", split="|");                  #查看标注结果
txt = bajie.show(select="wp", split=" ", onlyword=True);    #获取过滤结果


print
print


#排序
bajie.sort("textrank", 500, txt=txt);                       #对过滤结果排序
sortList = bajie.sort_list;                                 #获取排序列表
sortList.append(("新增测试",0.78873212));                     #添加自定义项目
print bajie.show(select="sort", split="\n");                #查看排序结果（不包含自定义）


#云图
cloudDict = bajie.makeSortDict(sortList);                   #生成排序字典
ttf = "./data/ttf";
pic = './data/apple.jpg';
bajie.makeCloudPic(cloudDict, ttf, pic);                    #生成云图
bajie.showCloudPic();                                       #显示云图
