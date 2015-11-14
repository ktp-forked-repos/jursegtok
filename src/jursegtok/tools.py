#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kuhn'
import codecs
import gzip
import logging
import os
import random
import shutil

from lxml import etree
from sklearn.feature_extraction.text import CountVectorizer
import hickle

from jursegtok.tokenizer import JurSentTokenizer
from jursegtok.utils import get_data, find_files
from segtok import tokenizer as segtoktokenizer
from segtok import segmenter


# define constants
HTML_PARSER = etree.HTMLParser()
COUNT_TOKENIZER = CountVectorizer().build_tokenizer()
JUR_SEGMENTER = hickle.load(get_data('jursentok.hkl'), safe=False)


# HEADERS = [u'Rubrum',u'Tenor', u'Tatbestand', u'Gründe', u'Entscheidungsgründe']
HEADERS = [u'## Tenor', u'## Tatbestand', u'## Grunde',
           u'## Gründe', u'## Entscheidungsgründe', u'Entscheidungs']






def random_sampling(corpuspath, outputpath='/tmp', k=10, debug=False):
    """
    randomly selects k elements from a corpus and
    copies them to an output path
    :param corpuspath:
    :param number:
    :return:
    """
    files = list(find_files(corpuspath, '*.html.gz'))
    samples = random.sample(files, k)
    for filepath in samples:
        shutil.copy(filepath, outputpath)
        if debug:
            print(os.path.basename(filepath))


def convert2sentences(corpuspath, outputpath):
    """
    converts raw ojc data to sentence segmented plaintext files
    :param corpuspath:
    :param outputpath:
    :return:
    """
    corpus = OJCorpusPlain(corpuspath)
    output = os.path.abspath(outputpath)
    jst = JurSentTokenizer()
    for name, document in corpus:
        outfilepath = os.path.join(output, name.rstrip('.html') + '_sentences.txt')
        with codecs.open(outfilepath, encoding='utf-8', mode='w') as sentencetokenized:
            tokenized = sentencelist2string(jst.sentence_tokenize(document))
            sentencetokenized.write(tokenized)


def sentencelist2string(sentencelist):
    """
    takes a list of sentences and returns a
    concatenated string of all elements.
    """
    for element in sentencelist:
        element.strip('\t\n')
        if element in HEADERS:
            element = element.uppercase()
            element = element + '\n'

    sentences = '\n'.join(sentencelist)
    return sentences


def count_tokens(corpuspath):
    tokens_count = int()
    tok_generator = sklearn_tokjursent_generator(corpuspath)
    for tokenized_sentence in tok_generator:
        tokenlen = len(tokenized_sentence)
        tokens_count += tokenlen
    return tokens_count


def count_sentences(corpusiterator):
    """
    counts all sentences a corpusiterator
    :param corpusiterator: an iterator over the corpus resource
    :return: sentnumber: int
    """
    sent_number = int()
    for filename, sentencegenerator in corpusiterator:
        for sentence in sentencegenerator:
            sent_number += 1
    return sent_number


def jursegment_sent_generator(document):
    """
    a sentence generator that uses the retrained nltk sentence tokenizer
    :param document: list of str
    :return:
    """
    for segment in document:
        for sentence in JUR_SEGMENTER.tokenize(segment):
            if sentence.strip():
                yield sentence


def sklearn_toksent_generator(corpus_path):
    ojcorpus = OJCorpus(corpus_path)
    for fname, sentences in ojcorpus:
        for sentence in sentences:
            tokenized_sentence = COUNT_TOKENIZER(sentence)
            if len(tokenized_sentence) > 1:
                yield tokenized_sentence


def sklearn_tokjursent_generator(corpus_path):
    ojcorpus = OJCorpusJurSentTok(corpus_path)
    for fname, sentences in ojcorpus:
        for sentence in sentences:
            tokenized_sentence = COUNT_TOKENIZER(sentence)
            if len(tokenized_sentence) > 1:
                yield tokenized_sentence

