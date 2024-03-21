import json
from make_negated import make_negated
from make_conditional import make_conditional
from make_interrogatives import from_interrogative
from make_interrogatives import make_interrogative
from make_modal import make_modal

types = ['original','negated','interrogative','modal','conditional']


"""
This file contains three main functions: 
    1) create_presupposition_dictionary(input_file)
    This code takes a .json file where each object contains a premise and a hypothesis as input.
    It converts it into a dictionary where the keys are the premises, and the values are dictionaries that will store the hypothesis under 
    the various embeddings: normal, negated, interrogative, modal and conditional.

    2) fill_presupposition_dictionary(input_file)
    This code uses the first code to create a presupposition dictionary. It then fills in the various embedding types.
    In other words, if for a given premise, there is only a hypothesis under a 'normal' embedding, it will generate negated, interrogative,
    modal and conditional versions of this hypothesis.

    3) write_to_output_file(input_file,output_file)
    This code takes a json file as input and creates a full presupposition dictionary using the second code, and writes it to an output .json file.

"""

def create_presupposition_dictionary(input_file):
    # Creates a nested dictionary:
# { premise: {type: hypothesis,
#            type: hypothesis,
#            type: hypothesis},
#  premise: {...}  }
    psp_dict = {}

    with open(input_file,'r') as f:
        data = json.load(f)

    for item in data:
        if item['label'] == 'P':

            item_type = item['type']
            if item_type not in types:
                print("item_type is not a valid type.\n")
                print(json.dumps(item, indent=4))

            if item['hypothesis'] and item['hypothesis'] not in psp_dict:
                psp_dict[item['hypothesis']] = {'original': "",
                                                'negated': "",
                                                'interrogative': "",
                                                'modal': "",
                                                'conditional': "",
                                                'trigger_type': item['trigger_type']}
                
                psp_dict[item['hypothesis']][item_type] = item['premise']
            
            if item['hypothesis'] and item['hypothesis'] in psp_dict:

                if psp_dict[item['hypothesis']][item_type] == "":
                    psp_dict[item['hypothesis']][item_type] = item['premise']
                else:
                    pass

    return psp_dict

def fill_presupposition_dictionary(input_file):
    # fills in missing hypotheses in the presupposition dictionary
    psp_dict = create_presupposition_dictionary(input_file)
    for hypothesis, premises in psp_dict.items():
        # fill in 'original' using whatever we have
        if premises['original'] == "" and premises['negated'] != "":    
            original = make_negated(premises['negated'])
            premises['original'] = original    
        if premises['original'] == "" and premises['interrogative'] != "":
            original = from_interrogative(premises['interrogative'])
            premises['original'] = original 
        # generating missing hypotheses from the original
        if premises['original'] != "" and premises['negated'] == "":
            negated = make_negated(premises['original'])
            premises['negated'] = negated
        if premises['original'] != "" and premises['conditional'] == "":
            conditional = make_conditional(premises['original'],premises['trigger_type'])
            conditional = delete_after_word(conditional,'Consequent:')
            conditional = delete_after_word(conditional,'Consequently,')
            premises['conditional'] = conditional
        if premises['original'] != "" and premises['interrogative'] == "":
            interrogative = make_interrogative(premises['original'],premises['trigger_type'])
            premises['interrogative'] = interrogative
        if premises['original'] != "" and premises['modal'] == "":
            modal = make_modal(premises['original'])
            premises['modal'] = modal
    return psp_dict


def write_to_output_file(input_file,output_file):
    # converts the presupposition dictionary into corpus items in .json file
    # input and output must be .json
    # input must be PECaN format
    psp_dict = fill_presupposition_dictionary(input_file)
    json_items = []
    for hypothesis, premises in psp_dict.items():
        for type, premise in premises.items():
            if type != 'trigger_type' and premise != "" and premise != 'na':
                new_json_item = {
                    'hypothesis': premise,
                    'premise': hypothesis,
                    'label': 'P',
                    'trigger_type': premises['trigger_type'],
                    'type': type
                }
                json_items.append(new_json_item)
    with open(output_file, 'w') as output_file:
        json.dump(json_items, output_file, indent=4)


"""
Auxiliary functions and functions I used for development
"""


def delete_after_word(string, word):
    # Hilfsfunktion that deletes 'Consequent:' part
    index = string.find(word)
    if index != -1:
        return string[:index]
    return string

def pretty_print(psp_dict):
    # Pretty print the presupposition dictionary
    for hypothesis, premises in psp_dict.items():
        print(hypothesis)
        for type, premise in premises.items():
            print(type,": ",premise,"\n")

def count_presupposition_dictionary(input_file):
    psp_dict = create_presupposition_dictionary(input_file)
    counts = {}
    for premises in psp_dict.values():
        vector = [0,0,0,0,0]
        if premises['original'] != "":
            vector[0] = 1
        if premises['negated'] != "":
            vector[1] = 1
        if premises['conditional'] != "":
            vector[2] = 1
        if premises['interrogative'] != "":
            vector[3] = 1
        if premises['modal'] != "":
            vector[4] = 1
        if str(vector) not in counts:
            counts[str(vector)] = 1
        else:
            counts[str(vector)] += 1
    print(counts)
    




