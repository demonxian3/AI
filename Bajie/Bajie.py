#!coding: utf-8
#date: 2018/06/13
#nickname: demonxain3
#blog: http://cnblogs.com/demonxian3

import sys
import jieba
import jieba.analyse as anal
import jieba.posseg as pseg

from scipy.misc import imread
from matplotlib import pyplot
from wordcloud import WordCloud


class Bajie:
    def __init__(self, foodpath):
        self.food = self.read(foodpath);
        self.wp_list = [];
        self.wf_list = [];
        self.cut_list = [];
        self.tag_list = [];
        self.sort_list = [];

    def addkey(self, word):
        jieba.add_word(word);


    def suggest(self, word):
        jieba.suggest_freq(word, True);


    def loaddict(self, dictfile):
        jieba.load_userdict(dictfile);


    def read(self, filename):
        fp = open(filename);
        txt = fp.read().decode("utf-8").encode("utf-8");
        fp.close();
        return txt;


    def cut(self, mode="N"):
        if mode == "F":
            words = jieba.lcut(self.food, cut_all=True);

        elif mode == "N":
            words = jieba.lcut(self.food);

        elif mode == "S":
            gen = jieba.cut_for_search(self.food);
            words = [i for i in gen];

        for idx in range(len(words)):
            words[idx] = words[idx].encode("utf-8");

        self.cut_list = words;



    def tag(self):
        words = pseg.lcut(self.food);

        for idx in range(len(words)):
            words[idx].word = words[idx].word.encode("utf-8");
            words[idx].flag = words[idx].flag.encode("utf-8");

        self.tag_list = words;



    def wfilter(self, stopfile):
        if self.cut_list:
            self.wf_list = [];

            stoplist = self.read(stopfile);
            for word in self.cut_list:
                if word and word not in stoplist:
                    self.wf_list.append(word);
        else:
            print "Nothing that has been cut";



    def wpfilter(self, stopfile):
        if self.tag_list:
            self.wp_list = [];
            savelist = []
            stoplist = self.read(stopfile);
            savelist += ["an", "n", "nr", "ns", "nt"];
            savelist += ["nz", "v", "vd", "eng", "ni"];

            for o in self.tag_list:
                if o.word not in stoplist and o.flag in savelist:
                    self.wp_list.append({"flag":o.flag, "word":o.word});

        else:
            print "Nothing that has been cut and tag"



    def show(self, select="cut", split="", onlyword=False):
        content = "";

        if select == "cut" :
            for i in self.cut_list:
                content += i + split;

        elif select == "wf":
            for i in self.wf_list:
                content += i + split;

        elif select == "tag":
            for i in self.tag_list:
                if not onlyword:
                    content += i.word + "("+i.flag+")" + split;
                else:
                    content += i.word + split;

        elif select == "wp":
            for i in self.wp_list:
                if not onlyword:
                    content += i['word'] + "(" + i['flag'] + ")" + split;
                else:
                    content += i['word'] + split;

        elif select == "sort":
            for w,v in self.sort_list:
                if not  onlyword:
                    content += w +"\t" + str(v) + split;
                else:
                    content += w + split;

        return content



    def sort(self, mode, topK, txt=""):
        self.sort_list = [];

        if txt:
            food = txt;
        else:
            food = self.food;

        if mode == "tfidf":
            words = anal.extract_tags(food, topK, withWeight=True);

        elif mode == "textrank":
            words = anal.textrank(food, topK, withWeight=True);

        for w,v in words:
            w = w.encode("utf-8");
            self.sort_list.append((w,v));



    def makeSortDict(self, sortList=""):
        if not sortList and not self.sort_list:
            print "no sort list";

        if not sortList:
            sortList = self.sort_list;

        sortDict = {}
        for i in sortList:
            sortDict[i[0].decode("utf-8")] = i[1];

        return sortDict;



    def makeCloudPic(self, cloudDict, ttf, maskimg=""):
        if not ttf:
            print "plesae special ttf file";

        if maskimg:
            pic = imread(maskimg);
            #max_words=2000, #max_font_size=40, #width=1000, #height=800,
            wc = WordCloud(
                font_path = ttf,
                background_color = "white",
                mask=pic,
            );

        else:
            wc = WordCloud(
                font_path = ttf,
                background_color = "white",
            );


        self.wc = wc.generate_from_frequencies(cloudDict);


    def showCloudPic(self):
        pyplot.imshow(self.wc);
        pyplot.axis("off");
        pyplot.show();
