
"""
These functions handle the generation of individual constituents.
"""

def generate_pp(token):
    pp = token.text + " "
    for child in token.children:
        if str(child.dep_) == "pobj":
            pp += generate_np(child)
    return pp

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
        if str(child.dep_) == 'cc':
            np += child.text + " "
        if str(child.dep_) == 'conj':
            np += child.text + ' '
        if str(child.dep_) == 'prep':
            np += generate_pp(child)
    return np

def generate_subject(token):
    subject = ""
    for child in token.children:
        if str(child.dep_) == "compound":
            subject += child.text + " "
    subject += token.text
    return subject


def generate_attr(token):
    attr = token.text + " "
    for child in token.children:
        if str(child.dep_) == "prep":
            attr += generate_pp(child)
    return attr

    
def generate_advmod(token):
    advmod = ""
    for child in token.children:
        if str(child.dep_) == "advmod":
            advmod += generate_advmod(child)
    advmod += token.text + " "
    return advmod

def generate_prt(token):
    prt = token.text + " "
    for child in token.children:
        if str(child.dep_) == 'prep':
            prt += generate_pp(child)
    return prt

def generate_ccomp(token):
    ccomp = ""
    for child in token.children:
        if str(child.dep_) == 'nsubj':
            ccomp = generate_np(child) + " "
    ccomp += token.text
    return ccomp

def generate_xcomp(token):
    xcomp = ""
    for child in token.children:
        if str(child.dep_) == 'aux':
            xcomp += child.text + " "
    xcomp += token.text + " "
    for child in token.children:
        if str(child.dep_) == 'ccomp':
            xcomp += generate_ccomp(child) + " "
        if str(child.dep_) == 'prep':
            xcomp += generate_pp(child)
    return xcomp

def generate_vp(token):
    index = 0
    vp = ""
    aux = ""
    neg = ""
    auxpass = ""
    xcomp = ""
    acomp = ""
    for child in token.children:
        if str(child.dep_) == 'aux':
            aux += child.text
        if str(child.dep_) == 'neg':
            neg += child.text
        if str(child.dep_) == 'auxpass':
            if str(next(token.children).dep_) == "neg":
                auxpass += child.text + token.children[index+1].dep_ + " "
            else:
                auxpass += child.text + ' '
        if str(child.dep_) == 'xcomp':
            xcomp += generate_xcomp(child)
        if str(child.dep_) == 'acomp':
            acomp += child.text
        index += 1
    vp += aux + neg + " " + auxpass + " " + token.text + " " + xcomp + " " + acomp
    return vp
    
"""
Functions that detect vowels and plurals.
"""

def starts_with_vowel(word):
    return str(word)[0] in ["a","e","i","o","u","A","E","I","O","U"]

def regular_plural(word):
    number = word.morph.get("Number")
    if number == []:
        return False
    else:
        if number[0] == 'Sing':
            return False
        else:
            return True