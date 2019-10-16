#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:40:01 2019

@author: eduardo
"""

toy_text = [
"Elephants are large mammals of the family Elephantidae and the order Proboscidea", 
"Two species are traditionally recognised, the African elephant and the Asian elephant", 
"Elephants are scattered throughout sub-Saharan Africa, South Asia, and Southeast Asia", 
"Male African elephants are the largest extant terrestrial animals",
"All elephants have a long trunk used for many purposes, particularly breathing, lifting water and grasping objects",
"Their incisors grow into tusks, which can serve as weapons and as tools for moving objects and digging",
"Elephants' large ear flaps help to control their body temperature",
"Their pillar-like legs can carry their great weight",
"African elephants have larger ears and concave backs while Asian elephants have smaller ears and convex or level backs"]

texts = [
"We need to go to New York city for vacation", 
"This machine learning course is really hard",
"The battery does not last as much as the other version", 
"I really liked the pool and the food",
"The screen is great, it has major resolution",
"The restaurant looks great, the decoration is neat, however the food could be better"
]
     
h_review =[
"We stayed here for two days in the beginning of August",
"The pros: We had a 2 bedroom suite which was beautiful",
"It was absolutely huge",
"Also, the shuttle service was great",
"You didn't have to wait more than a couple of minutes",
"It took us to Main Street as well as Olympic National Park",
"The cons: The layout of this hotel is ridiculous, as other reviewers have mentioned",
"Whether you want to go to a restaurant, the bar, or the lobby, it requires multiple elevator changes and walking down multiple very long hallways"
"More than once we passed people wandering around trying to find various destinations",
"I can't imagine who thought this layout was a good idea",
"It is for this reason I would not stay here again even though the rooms were beautiful"
]

    
#from normalization import parse_document
import itertools
import nltk
#from normalization import stopword_list
from gensim import corpora, models

stopword_list = nltk.corpus.stopwords.words('english')

grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""

def get_chunks(sentences, grammar = r'NP: {<DT>? <JJ>* <NN.*>+}'):
#def get_chunks(sentences, grammar = r'NP: {<VB.*>? <IN>? <DT>? <JJ>? <NN.*>+}'):
#def get_chunks(sentences, grammar = r'NP: {<DT>? <NN.*>+}'):
#def get_chunks(sentences, grammar = r'NP: {<NN.*>+ <VB.*>? <NN.*>?}'):
    all_chunks = []
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    
    for sentence in sentences:
        
        tagged_sents = nltk.pos_tag_sents(
                            [nltk.word_tokenize(sentence)])
        
        chunks = [chunker.parse(tagged_sent) 
                  for tagged_sent in tagged_sents]
        
        wtc_sents = [nltk.chunk.tree2conlltags(chunk)
                     for chunk in chunks]    
         
        flattened_chunks = list(
                            itertools.chain.from_iterable(
                                wtc_sent for wtc_sent in wtc_sents)
                           )
        
        valid_chunks_tagged = [(status, [wtc for wtc in chunk]) 
                        for status, chunk 
                        in itertools.groupby(flattened_chunks, 
                                             lambda (word,pos,chunk): chunk != 'O')]
        
        valid_chunks = [' '.join(word.lower() 
                                for word, tag, chunk 
                                in wtc_group 
                                    if word.lower() 
                                        not in stopword_list) 
                                    for status, wtc_group 
                                    in valid_chunks_tagged
                                        if status]
                                            
        all_chunks.append(valid_chunks)
    
    return all_chunks

    

def avg_aspects(text):
    print "Num. of aspects:", sum([len(x) for x in text])
    
    
#sentences = parse_document(toy_text)          
valid_chunks = get_chunks(h_review)
print valid_chunks
avg_aspects(valid_chunks)

