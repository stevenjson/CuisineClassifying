import os
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

def GetFile(fileName, path):
    _file = open(path + fileName, 'r')
    recipeList = _file.read().split('\n')
    recipeList.pop()
    _file.close()

    return recipeList

def SVM(trainMap, testMap, cuisineList):
    """
    count_vec = CountVectorizer()
    train_counts = count_vec.fit_transform(trainMap)
    train_counts.shape
    #print(count_vec.vocabulary_.get(u'tomato'))

    tf_trans = TfidfTransformer(use_idf=False).fit(train_counts)
    train_tf = tf_trans.transform(train_counts)
    train_tf.shape
    """

    #text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=1000, random_state=42)),])

    text_clf = text_clf.fit(trainMap, cuisineList)
    total_all = 0
    correct_all = 0
    for cuisineName in cuisineList:
        
        test = testMap[cuisineName]
        predict = text_clf.predict(test)
        #print(predict)
        correct = 0
        total = 0
        for item in predict:
            total += 1
            total_all += 1
            if item == cuisineName:
                correct += 1
                correct_all += 1
        
        print(cuisineName, correct / float(total))

    print("FINAL:", correct_all / float(total_all)) 
    
    pass

def main():

    trainPath = "Data/train/"
    testPath = "Data/test/"
    
    trainFileList = os.listdir(trainPath)
    testFileList = os.listdir(testPath)
    
    testMap = {}
    trainMap = {}
    cuisineList = []
    format_train = []
    
    for _file in testFileList:
        cuisine = _file.strip("test-").strip(".txt")
        recipeList = GetFile(_file, testPath)
        testMap[cuisine] = recipeList

    for _file in trainFileList:
        cuisine = _file.strip(".txt")
        cuisineList.append(cuisine)
        recipeList = GetFile(_file, trainPath)
        trainMap[cuisine] = " ".join(recipeList)

    for cuisineID in cuisineList:
        format_train.append(trainMap[cuisineID])

    SVM(format_train, testMap, cuisineList)

    pass

main()
