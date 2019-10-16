#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 14:54:48 2019

@author: eduardo
"""
from __future__ import unicode_literals
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence
from gensim.summarization import keywords
import itertools
import nltk
import sys

stopwords = nltk.corpus.stopwords.words('english')

texts = ["We need to go to New York city for vacation", "This machine learning course is really hard",
         "The battery does not last as much as the other version", "I really liked the pool and the food"]

def get_chunks(sentences, grammar=r'NP: {<NN.*>+}', stopword_list=stopwords):
    all_chunks = []
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    
    for sentence in sentences:

        tagged_sents = nltk.pos_tag(nltk.word_tokenize(sentence))
                       
        chunks = [chunker.parse(tagged_sents) for tagged_sent in tagged_sents]
        
        wtc_sents = [nltk.chunk.tree2conlltags(chunk) for chunk in chunks]
                     
        flattened_chunks = list(itertools.chain.from_iterable(wtc_sent 
                                                              for wtc_sent in wtc_sents))
        
        valid_chunks_tagged = [(status, [wtc for wtc in chunk])
                                for status, chunk
                                        in itertools.groupby(flattened_chunks,
                                                lambda word_pos_chunk: word_pos_chunk[2] != 'O')]
                                                    
        valid_chunks = [' '.join(word.lower() for word, tag, chunk in wtc_group
                                 if word.lower() not in stopword_list) 
                                for status, wtc_group in valid_chunks_tagged if status]
                                
        all_chunks.append(valid_chunks)
        
    return all_chunks
    
chunks = get_chunks(texts)
print chunks