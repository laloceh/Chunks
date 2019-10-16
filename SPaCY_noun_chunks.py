#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:21:34 2019

@author: eduardo
"""

from __future__ import unicode_literals

texts = ["We need to go to New York city for vacation", "This machine learning course is really hard",
         "The battery does not last as much as the other version", "I really liked the pool and the food"]

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


import spacy

nlp = spacy.load("en_core_web_sm")

for t in h_review:
    t = nlp(t)
    pos = [(token.text, token.tag_) for token in t]
    #print pos
    chunks = [c.text for c in t.noun_chunks]
    print chunks
    print

##################

nouns = []
for text in texts:
    try:
        t = nlp(text)
        for token in t:
            if (token.tag_ == "NN" or token.tag_ == 'NNP'):
                nouns.append(token.text)
    except:
        pass
        
print nouns

                