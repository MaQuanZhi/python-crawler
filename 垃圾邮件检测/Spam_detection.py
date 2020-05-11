import re
from sklearn.svm import LinearSVC

# 切割文本,统计词频
def splitText(text):
    wordlist = {}
    rtnList = []
    wordFreqList = {}
    # 分词
    listofTokens = re.split(r'\W',text)
    length = len(listofTokens)
    for token in listofTokens:
        if token:
            if  not wordlist.get(token, 0):
                wordlist[token] = 1
                rtnList.append(token)
            else:
                wordlist[token] += 1
            wordFreqList[token] = float(wordlist[token])/length
    return rtnList,wordFreqList
       
# 统计单词反文档频率
def docFre(word,data):
    fre = 0
    for line in data:
        if word in re.split(r'\W',line):
             fre += 1
    return float(fre)/len(data)


# 特征词提取，使用TF-IDF
def extractFeature(data,num=100):
    fullText = []
    wordTFIDF = {}
    for line in data:
        wordlist, wordFreqList = splitText(line)
        fullText.append(wordlist)
        for word in wordFreqList:
            wordIDF = docFre(word,data)
            wordTFIDFValue = wordIDF*wordFreqList[word]
            if not  wordTFIDF.get(word,0):
                wordTFIDF[word] = wordTFIDFValue
            else :
                wordTFIDF[word] += wordTFIDFValue
    sortedWordTFIDF=sorted(wordTFIDF.items(),key=lambda x:x[1],reverse=True)
   # 选取前num个词为分类词
    keywords = [word[0] for word in sortedWordTFIDF[:num]]
    return keywords
 
# 构建特征向量（使用0,1表示存在与否）
def extaxtDocFeatureVec(text,keyword):
    vec = []
    for i,word in enumerate(keyword):
        if word in text:
            vec.append(1)
        else :
            vec.append(0)
    return vec
 
# 抽取所有邮件的特征向量
def extactFeatureVec(hamData,spamData,save=False):
    hamWordsVec = extractFeature(hamData)
    spamWordsVec = extractFeature(spamData)
    allWordsVec = hamWordsVec+spamWordsVec
    if save:
        with open('allWordsVec.txt','w') as f:
            f.write(','.join(allWordsVec))
    wordVecs = []
    classList = []
    for hamLine in hamData:
        wordlistHam, wordFreqList = splitText(hamLine)
        vecHam = extaxtDocFeatureVec(wordlistHam,allWordsVec)
        wordVecs.append(vecHam)
        classList.append(1)
    for spamLine in spamData:
        wordlistSpam, wordFreqList = splitText(spamLine)
        vecSpam = extaxtDocFeatureVec(wordlistSpam,allWordsVec)
        wordVecs.append(vecSpam)
        classList.append(-1)  
    return wordVecs,classList

# 构造测试集
def getTestData(text,allWordsVec):
    dataArr = []
    labelArr = []
    for line in spam_train:
        if line[:4] == 'ham,':
            vec = extaxtDocFeatureVec(line[4:],allWordsVec)
            dataArr.append(vec)
            labelArr.append(1)
        if line[:5] == 'spam,':
            vec = extaxtDocFeatureVec(line[5:],allWordsVec)
            dataArr.append(vec)
            labelArr.append(-1)         
    return dataArr,labelArr

# 构造训练集
def getTrainData(text):
    spamData = []
    hamData = []
    for line in spam_train:
        if line[:4] == 'ham,':
            hamData.append(line[4:])
        if line[:5] == 'spam,':
            spamData.append(line[5:])
    dataArr,labelArr = extactFeatureVec(hamData,spamData)
    return dataArr,labelArr

if __name__ == "__main__":
    with open("spam_train.csv",'rb') as f:
        spam_train = str(f.read()).split('\\r\\n')
    with open("spam_test.csv",'rb') as f:
        spam_test = str(f.read()).split('\\r\\n')
        
    X_train, y_train = getTrainData(spam_train)
    
    with open('allWordsVec.txt','r') as f:
        allWordsVec = f.read().split(',')
    
    X_test, y_test = getTestData(spam_test,allWordsVec)
    model = LinearSVC()
    model.fit(X_train, y_train)
    # 1:ham,-1:spam
    pred = model.predict(X_test)
    print("prediction:",pred)
    # predict_proba = model._predict_proba_lr(X_test)
    accuracy = model.score(X_test,y_test)
    print("accuracy:",accuracy)
    
    '''
    result:
    prediction [ 1  1 -1 ...  1  1  1]
    accuracy 0.9727891156462585
    '''
    
    
