import jieba
import re

def f1():
    with open('F:/微博/1_3月微博.txt','r',encoding='utf8') as f:
        lines = f.read().split('\n')
    with open('F:/微博/情感词汇本体.txt','r',encoding='utf8') as f:
        words = f.read().split('\n')
    word_dict = {}
    for word in words:
        list1 = word.split('\t')
        word_dict.update(dict({list1[0]:list1[4]}))
        
    for line in lines:
        list2 = jieba.lcut(line)
        with open('F:/微博/1_3微博分词结果.txt','a',encoding='utf8') as f:
           f.write('\t'.join(list2))
           f.write('\n')
        out = []
        for word in list2:
            if word in word_dict.keys():
                out.append(word_dict[word])
        else:
    #        print(out)
            with open('F:/微博/1_3情感分析.txt','a') as f:
                f.write('\t'.join(out))
                f.write('\n')
#'的','了','么','呢','吧','啊'
#'！','？','。'
def f2():
    with open('F:/微博/1_3月微博.txt','r',encoding='utf8') as f:
        lines = f.read().split('\n')
    outputword = []
    outputtype = []
    for line in lines:
        outword = []
        outtype = []
        if '的。' in line: #句末的“的”
            outword.append('的')
        if '了' in line:
            outword.append('了')
        if '么' in line:
            outword.append('么')
        if '呢' in line:
            outword.append('呢')
        if '吧' in line:
            outword.append('吧')
        if '啊' in line:
            outword.append('啊')
        if '！' in line:
            outtype.append('！')
        if '？' in line:
            outtype.append('？')
        if '。' in line:
            outtype.append('。')
        outputword.append('\t'.join(outword))
        outputtype.append('\t'.join(outtype))
    
    with open('F:/微博/1_3语气词.txt','w',encoding='utf8') as f:
        f.write('\n'.join(outputword))
    with open('F:/微博/1_3句式类别.txt','w',encoding='utf8') as f:
        f.write('\n'.join(outputtype))

def f3():
    with open('F:/微博/1_3月微博.txt','r',encoding='utf8') as f:
        lines = f.read().split('\n')
    count = 0
    for line in lines:
       if '我' in line:
           count += 1
           
    print('“我”出现次数：',count)

def f4():
    with open('F:/微博/1_3微博情感.txt','r') as f:
        lines = f.read().split('\n')
    output = []
    for line in lines:
        line = re.sub('\t{2,}','',line)
        mylist1 = line.split('\t')
        mylist2 = []
        for i in mylist1:
            mylist2.append(mylist1.count(i))
        index = mylist2.index(max(mylist2))
        output.append(mylist1[index])
    with open('F:/微博/1_3微博情感new.txt','w') as f:
        f.write('\n'.join(output))
       
def f5():
    with open('F:/微博/1_3句式类别.txt','r',encoding='utf8') as f:
        lines = f.read().split('\n')
   
    lines1 = []
    for line in lines:
        line = line.split('\t')
        lines1.extend(line)
    print(len(lines1))
    print('？：',lines1.count('？'))
    print('。：',lines1.count('。'))
    print('！：',lines1.count('！'))
    
def f6():
    with open('F:/微博/1_3语气词.txt','r',encoding='utf8') as f:
        lines = f.read().split('\n')
   
    lines1 = []
    for line in lines:
        line = line.split('\t')
        lines1.extend(line)
#    print(len(lines1))
    print('的：',lines1.count('的'))
    print('了：',lines1.count('了'))
    print('么：',lines1.count('么'))
    print('呢：',lines1.count('呢'))
    print('吧：',lines1.count('吧'))
    print('啊：',lines1.count('啊'))

def f7():
    with open('F:/微博/微博活泼分析.txt','r') as f:
        lines = f.read().split('\n')
    mylist = []
    for line in lines:
        line = re.sub('\t{2,}','',line)
        if len(line) == 0:
            mylist.append('正经')
        else:
            mylist.append('活泼')
    with open('F:/微博/1_3微博活泼分析.txt','w',encoding='utf8') as f:
        f.write('\n'.join(mylist))
        
if __name__=='__main__':
    f1()
    f2()
    f3()
    f4()
    f5()
    f6()
    f7()