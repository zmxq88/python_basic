'''
Created on Oct 19, 2010

@author: Peter
'''
from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	# 进行词条切分后的文档集合
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
	# 类标签的集合
    return postingList,classVec
                 
def createVocabList(dataSet):
# 创建一个包含文档中出现的不重复词的列表，即获得单词表
    vocabSet = set([])  #create empty set
	# 创建空集合
    for document in dataSet:
	# 遍历数据集的每一行
        vocabSet = vocabSet | set(document) #union of the two sets
		# | 是并集的意思，该句将每个文档返回的新词集合添加到该集合中
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
# 输入为词汇表和文档，输出为文档向量（01数组）
    returnVec = [0]*len(vocabList)
	# 创造所有元素都为0的向量
    for word in inputSet:
	# 遍历文档向量的每个单词
        if word in vocabList:
		# 如果单词在词汇表内
            returnVec[vocabList.index(word)] = 1
			# 列表.index()查找第一个匹配值的索引
        else: print "the word: %s is not in my Vocabulary!" % word
		# 否则输出某单词不在字典内
    return returnVec

def trainNB0(trainMatrix,trainCategory):
# 朴素贝叶斯分类的核心函数
    numTrainDocs = len(trainMatrix)
	# 计算文档数
    numWords = len(trainMatrix[0])
	# 计算词汇表中单词数
    pAbusive = sum(trainCategory)/float(numTrainDocs)
	# 计算p(c1)，即p(滥用的)
	
	# 书上代码本来是如下这样
	# p0Num = zeros(numWords); p1Num = zeros(numWords)      
    # p0Denom = 0.0; p1Denom = 0.0
	# 但是当计算多个概率乘积时，如果一个概率值为0，最后的乘积也为0
	# 为了消除这种影响，将所有词的出现数初始化为1，分母初始化为2
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones() 
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
	# 改成书上代码如下
	  
    for i in range(numTrainDocs):
	# 对于每一个训练文档
        if trainCategory[i] == 1:
		# 如果这一个训练文档的类别为1（计算1类别中）
            p1Num += trainMatrix[i]
			# trainMatrix[i]为这条文档向量,p1Num是向下滚动累加
            p1Denom += sum(trainMatrix[i])
			# 统计1类别的所有单词数
        else:
            p0Num += trainMatrix[i]
			# trainMatrix[i]为这条文档向量，p0Num是向下滚动累加
            p0Denom += sum(trainMatrix[i])
			# 统计0类别的所有单词数
    p1Vect = log(p1Num/p1Denom)          #change to log()
	# p1概率对数向量，p1Num是向量，piDenom是值，利用了向量的广播
    p0Vect = log(p0Num/p0Denom)          #change to log()
	# 取对数是为了解决“下溢出”问题，利用对数将算法中的概率相乘，变为取了对数的概率相加
	# 自然对数与原函数具有相同的增减性，而且在同一点上去到极值，所以虽然取值不同，但结果一样
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
# 使用训练好的朴素贝叶斯模型对未知数据向量分类
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
	# 两个向量元素级的相乘相加，对数将原本的相乘变成了相加
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
	# 比较两类的概率大小
        return 1
    else: 
        return 0
    
def bagOfWords2VecMN(vocabList, inputSet):
# 词袋：每个词可以出现多次
    returnVec = [0]*len(vocabList)
	# 同样先定义一个词汇表长度的列表
    for word in inputSet:
	# 对于输入文档的每个词
        if word in vocabList:
		# 如果词在单词表内
            returnVec[vocabList.index(word)] += 1
			# 列表.index()查找第一个匹配值的索引，索引对应的值不是设为1，而是+1
			# 就完成了词袋转换
    return returnVec

def testingNB():
# 便利函数，将测试封装在一个函数里，节省了测试时间
    listOPosts,listClasses = loadDataSet()
	# listOPosts是文档列表（双层列表形式），listClasses是类标签列表
    myVocabList = createVocabList(listOPosts)
	# 产生单词表向量（列表形式）
    trainMat=[]
	# 设置一个空训练集二维列表
    for postinDoc in listOPosts:
	# 遍历文档列表的每一行
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
		# 生成文档向量（01）并添加到空训练集二维列表中
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
	# 测试向量文档（列表形式）
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	# 转换为文档向量，并转化为数组
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)

def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
	# 分隔符是除单词、数字外的任意字符串
    return [tok.lower() for tok in listOfTokens if len(tok) > 2] 
	# 过滤掉长度小于3的字符串，简单的解析
    
def spamTest():
# 对贝叶斯垃圾邮件分类器进行自动化处理
    docList=[]; classList = []; fullText =[]
	# 空文档列表，空类列表，空全文档列表
    for i in range(1,26):
	# 遍历每个文档
        wordList = textParse(open('email/spam/%d.txt' % i).read())
		# 读取每个单词，并且用textParse函数处理，得到单词列表
        docList.append(wordList)
		# 将单词列表添加到文档列表中
        fullText.extend(wordList)
		# 用单词列表拓展全文档列表
        classList.append(1)
		# 列表.append()方法在末尾追加新对象，在此例中追加1类
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)#create vocabulary
	# 利用文档列表，创建单词表
    trainingSet = range(50); testSet=[]           #create test set
	# 初始化，训练集为0-50，测试集为空
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
		# random.uniform(a,b)返回随机实数n,其中a<=n<b,int改为整型
        testSet.append(trainingSet[randIndex])
		# 将被选中的训练集索引添加到测试集索引中
        del(trainingSet[randIndex])  
		# 删除训练集索引
    trainMat=[]; trainClasses = []
	# 初始化空的训练矩阵和训练集类标签列表
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
	# 对每个训练集索引
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
		# 通过输入单词表和文档列表，用词袋函数，转化为文档01向量，并添加到训练矩阵中
        trainClasses.append(classList[docIndex])
		# 将对应的类添加到训练集类标签列表中
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
	# 进行朴素贝叶斯训练，得到两个概率向量和一个概率
    errorCount = 0
	# 初始化错误频数为0
    for docIndex in testSet:        #classify the remaining items
	# 对每个测试集文档索引
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
		# 运用词袋函数转化为文档向量
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
		# 如果所预测的类不是它自身的类
            errorCount += 1
			# 错误频数+1
            print "classification error",docList[docIndex]
			# 显示分类错误
    print 'the error rate is: ',float(errorCount)/len(testSet)
	# 计算错误率并返回
    #return vocabList,fullText

def calcMostFreq(vocabList,fullText):
# 计算出现频率
    import operator
	# 引入操作符模块
    freqDict = {}
	# 初始化一个空的频率集字典
    for token in vocabList:
	# 遍历单词列表
        freqDict[token]=fullText.count(token)
		# 列表.count()统计出现次数，将出现次数赋予字典中的值
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True) 
    # 按键值对中的值大小进行反向排序
	return sortedFreq[:30]    
	# 返回出现频率在前30的单词

def localWords(feed1,feed0):
# 这段代码和spamTest几乎一样，区别在于输入是两个数据源，而不是文本文件
# 添加了去除最高频的30个词的功能，可以提高分类器的准确率
    import feedparser
    docList=[]; classList = []; fullText =[]
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1) #NY is class 1
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)#create vocabulary
    top30Words = calcMostFreq(vocabList,fullText)   #remove top 30 words
	# 移除掉30个常用词，可以有助于提高分类器的准确率
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet=[]           #create test set
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]
