#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

import nltk

import hickle

from jursegtok.utils import get_data
from segtok import segmenter, segmenter_test, tokenizer


# COMMON = '/home/kuhn/Dev/github/jursegtok/data/common_abbrv.txt'


class JurSentTokenizer(object):
    def __init__(self):

        self.jur_abbreviations = self.get_abbreviations()

        self.sent_tokenizer= self.get_tokenizer_model()
        self.sent_tokenizer_alt = self.get_tokenizer_model('jursentok1500.hkl')

        # must remove ending abbreviation stops to feed as parameters.
        # inline abbreviation stops are kept

        # self.sent_tokenizer._params.abbrev_types.update(set(self.jur_abbreviations))
        self.sent_tokenizer._params.abbrev_types.update(set(self.jur_abbreviations))

    def get_abbreviations(self, abbreviations='legal_abbrv.txt'):
        """
        Reads and prepares abbreviations from a text file found in data.
        param: abbreviations: file
        return: abbreviations: set
        """
        abbrev_file = codecs.open(get_data('legal_abbrv.txt'), encoding='utf8')
        return set(unicode(abbrev.strip().rstrip('.'))
                   for abbrev in abbrev_file)

    def get_tokenizer_model(self, model='jursentok.hkl'):
        """
        Reads and prepares a pretrained tokenizer model hickle-serialized data.
        param: model: file
        return: tokenizer_object: tokenizer object
        """
        tokenizer_object = hickle.load(get_data(model), safe = False)
        return tokenizer_object


    def sentence_tokenize(self, data):

        sentences = self.check_abbrev(self.sent_tokenizer.tokenize(data))
        sentences_alt = self.check_abbrev(self.sent_tokenizer_alt.tokenize(data))
        if len(sentences) > len(sentences_alt):
            return sentences_alt
        elif len(sentences) > len(sentences_alt):
            return sentences
        else:
            return sentences


    def check_abbrev(self, sentences):
        """
        checks if abbreviations have been mistakingly been seen as sentence terminal
        :param sentences:
        :return:
        """
        for sentence in sentences:

            tokens = tokenizer.space_tokenizer(sentence)
            if tokens[-2] in self.jur_abbreviations and tokens[-1] == u'.':
                tokens[-2] = tokens[-2] + u'.'
                tokens.remove(tokens[-1])
                # get the next sentence
                nextsenttokens = tokenizer.web_tokenizer(sentences[sentences.index(sentence) + 1])
                tokens.extend(nextsenttokens)
                sentence_update = u' '.join(tokens)
                sentences[sentences.index(sentence)] = sentence_update
                sentences = sentences.remove(sentences[sentences.index(sentence) + 1])
                return sentences
            else:
                return sentences

    def add_abbreviations(self, abbreviations):
        """
        From a given list, add abbreviations to the tokenizer.
        Needs a list of abbreviations.

        :param abbreviations: list
        """
        self.jur_abbreviations = self.jur_abbreviations.append(unicode(
                                                        abbreviations))
