import openai
import json
import time
import spacy
from spacy import displacy
import en_core_web_sm
import re
from sentence_splitter import SentenceSplitter


nlp = spacy.load("en_core_web_sm")


"""
This function embeds the root verb of a sentence in a modal.
For example: 'I'm generating presuppositions' gets changed to 'I might be generating presuppositions'.
"""


def make_modal(sentence):
    doc = nlp(sentence)
    newsentence = ""
    for token in doc:
        if token.dep_ == 'ROOT':
            for child in token.children:
                if child.dep_ == 'aux':
                    if child.text in ['has','have']:
                        newsentence = sentence.replace(" " + child.text + " ",' might have ')
                    else:
                        newsentence = sentence.replace(" " + child.text + " ",' might ')
                if child.dep_ == 'auxpass':
                    newsentence = sentence.replace(" " + child.text + " ",' might be ')
            if newsentence == "":
                if token.text == 'do':
                    newsentence = sentence.replace(" " + token.text + " ",' might ')
                elif token.text in ['is','am','are']:
                    newsentence = sentence.replace(" " + token.text + " ", ' might be ')
                elif token.text == '\'s':
                    newsentence = sentence.replace(token.text + " ", ' might be ')
                else: 
                    try:
                        tense = token.morph.get("Tense")[0]
                        if tense == 'Past':
                            if token.text in ['was','were']:
                                newsentence = sentence.replace(" " + token.text + " ",' might have been ')
                            else:
                                newsentence = sentence.replace(" " + token.text + " ",' might have ' + token.text + " ")
                        elif tense == 'Pres':
                            if token.text.endswith('s'):
                                no_s = ''.join(token.text.rsplit('s',1))
                                newsentence = sentence.replace(" " + token.text + " ",' might ' + no_s + " ")
                            else:
                                newsentence = sentence.replace(" " + token.text + " ",' might ' + token.text + " ")
                    except IndexError:
                        try:
                            number = token.morph.get("Number")[0]
                            if number == 'Plur':
                                no_s = ''.join(token.text.rsplit('s',1))
                                newsentence = sentence.replace(token.text, 'might ' + no_s)
                        except IndexError:
                            newsentence = sentence.replace(" " + token.text + " ",' might ' + token.text + " ")
    return newsentence


