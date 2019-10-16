#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:23:21 2019

@author: eduardo
"""

import nltk
from nltk.corpus import stopwords

text = raw_input("Enter the text please ...")
print text

text = """
We stayed here for two days in the beginning of August.
The pros: We had a 2 bedroom suite which was beautiful.
It was absolutely huge.
Also, the shuttle service was great.
You didn't have to wait more than a couple of minutes.
It took us to Main Street as well as Olympic National Park.
The cons: The layout of this hotel is ridiculous, as other reviewers have mentioned.
Whether you want to go to a restaurant, the bar, or the lobby, it requires multiple elevator changes and walking down multiple very long hallways.
More than once we passed people wandering around trying to find various destinations.
I can't imagine who thought this layout was a good idea.
It is for this reason I would not stay here again even though the rooms were beautiful.
"""

sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)
toks = nltk.regexp_tokenize(text, sentence_re)
postoks = nltk.tag.pos_tag(toks)
print postoks
tree = chunker.parse(postoks)
stopwords = stopwords.words('english')

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    # word = stemmer.stem_word(word) #if we consider stemmer then results comes with stemmed word, but in this case word will not match with comment
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword. We can increase the length if we want to consider large phrase"""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term

terms = get_terms(tree)

for term in terms:
    for word in term:
        print word,
    print