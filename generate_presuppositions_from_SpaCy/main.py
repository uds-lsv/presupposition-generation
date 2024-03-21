import spacy
import re
import json
from from_nounphrases import generate_presuppositions_from_nounphrases
from from_relativeclauses import generate_presuppositions_from_relativeclauses
from from_adverbialclauses import generate_adverbial_psp
from from_tagquestions import generate_speaker_psp

spacy_model = spacy.load("en_core_web_sm")


"""
This code converts a .csv file with questions into a .json file with sentences.
Specifically, it removes whitespaces, newlines, quotation marks, and Q: from the .csv question file.
"""

def clean_csv(csvfile,jsonfile):
    tojson = []
    with open(csvfile,encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip(): # Skips lines that are only whitespace
                line = line.strip("\"")
                line = re.sub("\"$","",line)
                line = line.strip()
                jdict = {"question": line}
                tojson.append(jdict)
    with open(jsonfile, "w", encoding="utf-8") as w:
        json.dump(tojson,w,indent=4)

        
"""
This is the main function of the presupposition extraction script.
It works by reading in a .json file of questions.
Presuppositions triggered somewhere in the question are searched for and extracted using three functions:
np_psp_generator, relcl_psp_generator, and generate_adverbial_psp.
These functions detect and extract presuppositions triggered by nominal phrases, relative clauses, and adverbial clauses, respectively.
"""

def presupposition_generator(injson,outjson):
    with open(injson,encoding="utf-8") as r:
        questions = json.load(r)
        for question in questions:
            doc = spacy_model(question["question"])
            question["presuppositions"] = generate_presuppositions_from_nounphrases(doc)
            question["presuppositions"] += generate_presuppositions_from_relativeclauses(doc)
            question["presuppositions"] += generate_adverbial_psp(doc)
            if generate_pos:
                question["pos"] = pos_generator(doc)
    with open(outjson,"w",encoding="utf-8") as w:
        json.dump(questions,w,indent=4)


