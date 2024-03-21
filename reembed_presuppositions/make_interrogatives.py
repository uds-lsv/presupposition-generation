import openai
import json
import time
import spacy
from spacy import displacy
import en_core_web_sm
import re
from sentence_splitter import SentenceSplitter

nlp = spacy.load("en_core_web_sm")
splitter = SentenceSplitter(language='en')

"""
######  FUNCTIONS: INTERROGATIVE -> ORIGINAL ############
"""

def fix_capitalization(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.pos_ == 'VERB' or token.pos_ == "AUX":
            sentence = sentence.replace(token.text, token.text.lower())
    return sentence      

def generate_poss(token):
    poss = ""
    for child in token.children:
        if str(child.dep_) == 'compound':
            poss += child.text + " "
    poss += token.text
    for child in token.children:
        if str(child.dep_) == 'case':
            poss += child.text
    return poss

def generate_pp(token):
    pp = token.text + " "
    for child in token.children:
    
        if str(child.dep_) == "pobj":
            pp += generate_np(child)
    return pp

def generate_relcl(token):
    relcl = ""
    for child in token.children:
        if child.dep_ == 'nsubj':
            relcl += child.text + " "
        if child.dep_ == 'aux':
            relcl += child.text
            for kid in child.head.children:
                if kid.dep_ == 'neg':
                    relcl += kid.text + " "
            relcl += " "
    relcl += token.text
    for child in token.children:
        if child.dep_ == 'advmod':
            relcl += child.text + " "
        if child.dep_ == 'prep':
            relcl += generate_pp(child) + " "
    return relcl

def generate_np(token):
    np = ""
    for child in token.children:
        if str(child.dep_) == "det":
            np += child.text + " "
        if str(child.dep_) == 'poss':
            np += generate_poss(child) + " "
        if str(child.dep_) == "compound":
            np += child.text + " "
    np += token.text + " "
    for child in token.children:
        if child.dep_ == 'relcl':
            np += generate_relcl(child)
        if str(child.dep_) == 'cc':
            np += child.text + " "
        if str(child.dep_) == 'conj':
            np += child.text + ' '
        if str(child.dep_) == 'prep':
            np += generate_pp(child)
    return np

def swap_substrings(string, subject, verb):
    #indexes of subject and verb in string
    split_string = string.split()
    # For an original sentence, the subject should precede the verb (SVO). 
    # Check if this is already the case.
    if string.find(subject) < string.find(verb):
        return string
    # If the verb comes before the subject:
    # split by subject, replace verb with subject, connect by verb
    else:
        filler = 'zzzzzzzz'
        tempStr1 = string.replace(subject, filler,1)
        #print(tempStr1)
        tempStr2 = tempStr1.replace(verb, subject,1)
        #print(tempStr2)
        str = tempStr2.replace(filler, verb,1)
        return str 

def from_interrogative(sentence):
    # Get rid of short discourse fillers
    sentence_no_fillers = ""
    split_sentence = splitter.split(sentence)
    for satz in split_sentence:
        if len(satz.split()) <= 3:
            pass
        else:
            sentence_no_fillers += satz
    # Replace the ? with a .
    modified_sentence = sentence_no_fillers.replace("?", ".")
    modified_sentence = modified_sentence.replace(', is that correct','')
    modified_sentence = modified_sentence.replace(', don\u2019t you','')
    modified_sentence = modified_sentence.replace(', wouldn\u2019t you','')
    modified_sentence = modified_sentence.replace(', aren\u2019t you','')
    # Switch verb and subject.
    doc = nlp(modified_sentence)
    subject = ""
    verb = ""
    for token in doc:
        if token.dep_ == 'ROOT':
            for child in token.children:
                if child.dep_ == 'nsubj' or child.dep_ == 'nsubjpass':
                    subject = generate_np(child)
                if child.dep_ == 'auxpass' or child.dep_ == 'aux':
                    verb = child.text + " "
            if verb == "":
                verb = token.text + " "
    subject = re.sub(r"\s+", " ", subject)
    try:
        modified_sentence = swap_substrings(modified_sentence,subject,verb)
        modified_sentence = re.sub(r"\s+", " ", modified_sentence)
        modified_sentence = fix_capitalization(modified_sentence)
    except ValueError:
        print('ValueError')
        modified_sentence = 'na'
    except TypeError:
        print('TypeError')
        #print(modified_sentence)
    return modified_sentence

########## METHODS FOR ORIGINAL -> INTERROGATIVE

def askGPT_interrogative(text):
    openai.api_key = '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'
    prompt = "Turn this statement into a question, making as little changes to the original sentence as possible." + "\n" + text
    response = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    temperature = 0.6,
    max_tokens = 30,
    )
# Print the generated response
    return response.choices[0].text.strip()

def askGPT_cleft(text):
    openai.api_key = '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'
    prompt = "Turn this statement into a question, making as little changes to the original sentence as possible and keeping the cleft as it is." + "\n" + text
    response = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    temperature = 0.8,
    max_tokens = 30,
    )
    return response.choices[0].text.strip()

def askGPT_numeric_det(text):
    openai.api_key = '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'
    prompt = "Turn this statement into a question, keeping all noun phrases as they are." + "\n" + text
    response = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    temperature = 0.8,
    max_tokens = 30,
    )
    return response.choices[0].text.strip()

def make_interrogative(sentence,trigger_type):
    interrogative_sentence = 'na'
    if trigger_type == 'clefts':
        try:
            interrogative_sentence = askGPT_cleft(sentence)
        except openai.error.RateLimitError as e:
            print(e)
        except openai.error.ServiceUnavailableError as e:
            print(e)
        except openai.error.APIError as e:
            print(e)
        except OSError as e:
            print(e)
    elif trigger_type == 'numeric_determiners':
        try:
            interrogative_sentence = askGPT_numeric_det(sentence)
        except openai.error.RateLimitError as e:
            print(e)
        except openai.error.ServiceUnavailableError as e:
            print(e)
        except openai.error.APIError as e:
            print(e)
        except OSError as e:
            print(e)
    else:
        try:
            interrogative_sentence = askGPT_interrogative(sentence)
        except openai.error.RateLimitError as e:
            print(e)
        except openai.error.ServiceUnavailableError as e:
            print(e)
        except openai.error.APIError as e:
            print(e)
        except OSError as e:
            print(e)
    return interrogative_sentence


