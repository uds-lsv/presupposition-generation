import spacy
from generate_constituents import starts_with_vowel
from generate_constituents import regular_plural
import re
from sentence_splitter import SentenceSplitter
spacy_model = spacy.load("en_core_web_sm")
splitter = SentenceSplitter(language='en')


"""
This function is supposed to generate so-called 'speaker' presuppositions.
These are presuppositions that are triggered by tag-questions.
In other words, tag-questions presuppose that the person uttering the tag-question believes the information they seek to have confirmed is true.

The function works by detecting tag-questions by finding their tags (i.e. 'Right?', 'You see?') and pruning parts of the sentence that do not
belong to the information to be confirmed.

The function doesn't work very well yet so it is not included in the main presupposition generator function.
"""

def generate_presuppositions_from_tagquestions(question):
    presuppositions = []
    sentencelist = splitter.split(text=question)
    speakerpsp_sentencelist = []
    index = 0
    for sentence in sentencelist:
        if is_tag_question(sentence):
            speakerpsp_sentencelist.append(sentencelist[index-1])
        index += 1
    for sentence in speakerpsp_sentencelist:
        wordslist = [word for word in sentence.split(" ")]
        if is_cc(wordslist[0]):
            wordslist = wordslist[1:]
        psp = "The speaker believes that "
        for word in wordslist:
                psp += convert_first_second_person(word) + " "
        presuppositions.append(psp)
    return presuppositions


"""
Auxiliary functions for the generate_presuppositions_from_tagquestions function.
"""

def convert_first_second_person(word):
    if word == "I’m":
        return "they're"
    if word == 'I':
        return "they"
    if word == "I’ve":
        return "they've"
    if word == "you":
        return "their partner"
    if word == 'am':
        return 'are'
    if word == 'my':
        return 'their'
    if word == 'was':
        return 'were'
    else:
        return word

def find_dep(token):
    dep = [(token.text,token.dep_)]
    for child in token.children:
        dep.append((child.text,child.dep_))
    return dep

def is_tag_question(question):
    question = question.strip(" ")
    return question in ["True?","Is that fair?","Do you agree?","Right?","Correct?","Are you with me?","Okay?"]

def is_cc(word):
    return word in ["and","And","but","But","So,","Well,","Then,","Then","Now,","And,"]



