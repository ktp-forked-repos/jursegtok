__author__ = 'kuhn'

import nltk
import codecs
import os

JUR = '/home/kuhn/Data/GitHub/jursegtok/data/legal_abbrv.txt'
COMMON = '/home/kuhn/Data/GitHub/jursegtok/data/common_abbrv.txt'


class JurSentTokenizer(object):

    def __init__(self):

        self.jur_abbreviations = codecs.open(os.path.abspath(JUR), encoding='utf-8').readlines()

        self.common_abbreviations = codecs.open(os.path.abspath(COMMON), encoding='utf-8').readlines()

        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')

        # must remove ending abbreviation stops to feed as parameters.
        # inline abbreviation stops are kept
        for abbrev in self.jur_abbreviations:
            abbrev.rstrip('.')

        for abbrev in self.common_abbreviations:
            abbrev.rstrip('.')

        # self.sent_tokenizer._params.abbrev_types.update(set(self.common_abbreviations), set(self.jur_abbreviations))

    def sentence_tokenize(self, data):

        return self.sent_tokenizer.tokenize(data)

