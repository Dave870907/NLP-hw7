import streamlit as st

import re
from collections import Counter
from pprint import pprint

#from functools import filter

def words(text): return re.findall(r'\w+', text.lower())
word_count = Counter(words(open('big.txt').read()))
N = sum(word_count.values())
def P(word): return word_count[word] / N # float

#Run the function:

# print( list(map(lambda x: (x, P(x)), words('speling spelling speeling'))) )

letters    = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    dup_two   = duplicate_char_two(word)
    

    return set(deletes + transposes + replaces + inserts + dup_two)
    
#Run the function:
# pprint( list(edits1('adresable'))[:3])
# pprint( list(map(lambda x: (x, P(x)), edits1('adresable'))) )
# print( list(filter(lambda x: P(x) != 0.0, edits1('adresable'))) )
# print( max(edits1('adresable'), key=P) )

def duplicate_char_two(word):
    dup_two = []
    for i in range(len(word)):
        first = word[:i]+word[i]+word[i:]
        for j in range(i+2,len(first)):
            second = first[:j]+first[j]+first[j:]
            dup_two.append(second)
    return dup_two

def filter_non_sense(words):
    non_sense = {'aa':'a','uu':'u','aly':'ally','lble':'lable'}
    return [word.replace(key,value) for key,value in non_sense.items() 
                                    for word in words if key in word ] or words

# def typo_correct(words):


def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]).union(known(edits1(word))) or known(edits2(word)) or filter_non_sense([word]))

def known(words): 
    test = []
    for w in words: 
        if w in word_count:
            test.append(w)
    return set(test)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

st.title = "Speller Checker"
choice = st.selectbox('Select a word',['forgive','dare','edit','propase','propose','paint','pace','wol','noticesd','addresss'])
word = st.text_input('Type your word',choice)

with st.sidebar:
    original = st.checkbox('Show original word')

if original:
    st.text(f'Original word: {word}')

if word == correction(word):
    st.success(f'{word} is correct')
else:
    st.error(f'Correction: {correction(word)}')

