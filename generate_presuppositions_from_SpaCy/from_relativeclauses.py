import spacy
from generate_constituents import starts_with_vowel, regular_plural, generate_subject, generate_pp, generate_advmod, generate_attr, generate_ccomp, generate_np, generate_poss, generate_prt, generate_vp, generate_xcomp
import re

"""
This function handles the generation of a presupposition triggered by a reference to an entity including a relative clause.
It works by recursively generating constituents based on detected dependency heads.
"""

def generate_presuppositions_from_relativeclauses(doc):
    presuppositions = []
    for token in doc:
        if str(token.dep_) == 'relcl':
            if regular_plural(token.head):
                psp = "There are "
            else:
                psp = "There is a "
            psp += generate_subject(token.head) + " "
            for child in token.children:
                if is_relpro(child):
                    psp += child.text + " "
                if str(child.dep_) == 'nsubj' and not is_relpro(child):
                    psp += generate_np(child)
                if str(child.dep_) == 'nsubjpass' and not is_relpro(child):
                    psp += generate_np(child)
            psp += generate_vp(token)
            for child in token.children:
                if str(child.dep_) == 'prt':
                    psp += generate_prt(child)
                if str(child.dep_) == 'dobj' and not is_relpro(child):
                    psp += generate_np(child)
                if str(child.dep_) == 'attr':
                    psp += generate_attr(child) + " "
                if str(child.dep_) == 'prep':
                    psp += generate_pp(child) + " "
                if str(child.dep_) == 'advmod' and not is_relpro(child):
                    psp += generate_advmod(child)
            psp = re.sub(' +', ' ',psp)
            psp = psp.strip()
            psp += "."
            presuppositions.append(psp)
    return presuppositions


"""
This function detects the presence of relative pronouns.
"""

def is_relpro(token):
    return token.text in ["who","where","when","that"]
