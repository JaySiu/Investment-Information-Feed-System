# coding=utf8

import re
import random
import jieba
import pandas as pd
import module_path as mp
from nltk.classify import NaiveBayesClassifier, accuracy
#from hanziconv import HanziConv

TRAINING_SET_SIZE = 1.0
STOPWORDS = []

##### helpers ##################################################################

def tokenize(text):
    return list(set(jieba.lcut(preprocess_text(text))))


def preprocess_text(text):
    return text.replace(u'\xa0', u' ').replace(u' ', u'')


def check_seen(target_list):
    f = open(mp.DIR_ML + 'positive.txt', 'r', encoding="utf8", errors='ignore')
    pos_words = [word.replace('\n', '') for word in f]
    f.close()
    f = open(mp.DIR_ML + 'negative.txt', 'r', encoding="utf8", errors='ignore')
    all_words = pos_words + [word.replace('\n', '') for word in f]
    f.close()
    unseen = 0
    for f in target_list:
        if list(f.keys())[0] not in all_words:
            unseen += 1
    return unseen


def remove_number(word_list):
    num_patt = re.compile(r'[0-9a-zA-Z\.\%]+')
    delete_list = []
    for idx, f in enumerate(word_list):
        found_number = num_patt.search(list(f.keys())[0])
        if found_number != None:
            delete_list.append(idx)
    #print(delete_list, '\n')
    for idx in sorted(delete_list, reverse=True):
        del word_list[idx]
    #print(word_list, '\n')
    return word_list


def clear_up_stopwords():
    f = open(mp.DIR_ML + 'stopwords_zh.txt', 'w', encoding="utf8")
    f.write('\n')
    global STOPWORDS
    STOPWORDS = sorted(list(set(STOPWORDS)))
    for sw in STOPWORDS:
        f.write(sw + '\n')


def read_stopwords_zh():
    f = open(mp.DIR_ML + 'stopwords_zh.txt', 'r', encoding="utf8")
    stopwords = [line for line in f]
    stopwords = [sw.replace('\n', '') for sw in stopwords]
    f.close()
    return set(stopwords)


def create_single_feature(word):
    return {word: True}


def create_features(words):
    return [{word: True} for word in words if word not in STOPWORDS]


def train_NB():
    f = open(mp.DIR_ML + 'positive.txt', 'r', encoding="utf8", errors='ignore')
    pos_words = [word.replace('\n', '') for word in f]
    features_len = len(pos_words)
    pos_feature = [(create_single_feature(word), 'positive') for word in pos_words]
    f.close()

    f = open(mp.DIR_ML + 'negative.txt', 'r', encoding="utf8", errors='ignore')
    neg_words = [word.replace('\n', '') for word in f]
    features_len += len(neg_words)
    neg_feature = [(create_single_feature(word), 'negative') for word in neg_words]

    featuresets = pos_feature + neg_feature
    random.shuffle(featuresets)
    train_set, test_set = featuresets[:int(features_len*TRAINING_SET_SIZE)], featuresets[int(features_len*TRAINING_SET_SIZE):]
    classifier = NaiveBayesClassifier.train(train_set)
    #print(accuracy(classifier, test_set))
    return classifier


################################################################################

def nlp():
    jieba.set_dictionary(mp.DIR_ML + 'dict.txt.big')
    global STOPWORDS
    STOPWORDS = read_stopwords_zh()
    #clear_up_stopwords()           # umcomment this line to clean up the stopwords dict
    #print(len(STOPWORDS))
    classifier_NB = train_NB()

    df = pd.read_csv(mp.DIR_DATA_CUSTOMERS + 'customer_related_news.csv')
    results = []
    for idx, row in df.iterrows():
        if row.Content == '-----':
            results.append('-----')
        else:
            words = tokenize(row.Content)
            target_list = remove_number(create_features(words))
            #print(target_list)
            positive = 0
            for f in target_list:
                if classifier_NB.classify(f) == 'positive':
                    positive += 1
            if positive > (len(target_list) - positive - check_seen(target_list)):
                results.append("positive")
            elif positive == (len(target_list) - positive - check_seen(target_list)):
                results.append("neutral")
            else:
                results.append("negative")
    df['NB_score'] = results
    df.to_csv(mp.DIR_DATA_CUSTOMERS + 'customer_related_news.csv', index=False, encoding='utf_8_sig')

if __name__ == '__main__':
    nlp()
