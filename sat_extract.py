from pyteaser import SummarizeUrl
import wikipedia  # for gathering wikipedia content
import collections  # for counting the most counted word
from collections import Counter
import re  # for regular expressions
from textblob import TextBlob as tb
import math


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def get_facts(user_input):
    document1 = wikipedia.summary(user_input)

    document1 = tb(document1)
    bloblist = [document1]
    for i, blob in enumerate(bloblist):
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    sent = document1.split('.')
    p = 0.0
    dict1 = {}
    for sent in document1.split('.'):
        if sent != '':
            for word in sent.split(' '):
                word != ' '
                for word, score in sorted_words:
                    p = p + score
                dict1[sent] = p
    sorted_dict = sorted(
        dict1.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict


def remove_num(sent):
    return [x.strip() for x in re.split(r'\[].[0-9*][\]', sent) if x.split()]

# non reg ex way of dealing with expressions


def removeNestedParentheses(s):
    ret = ''
    skip = 0
    for i in s:
        if i == '[':
            skip += 1
        elif i == ']'and skip > 0:
            skip -= 1
        elif skip == 0:
            ret += i
    return ret


def fact_extract(user_input):
    url = wikipedia.page(user_input).url
    error = ''
    # s = Summarize(user_input, wikipedia.page(user_input).content) is to summarize if the url is not available
    # this one is for extracting the content directly from the keyword entered by the user
    s = SummarizeUrl(url)
    try:
        summ = ' '.join(word for word in s)
    except TypeError:
        return error
    summ = removeNestedParentheses(summ)
    summ = summ.replace(". ", ".\n\n")
    return summ
