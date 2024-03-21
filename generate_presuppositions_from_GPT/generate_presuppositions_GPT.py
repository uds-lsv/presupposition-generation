import openai
import json
import time

"""
This code takes as input a file a .tsv file with one question per line, such as 'cross_examinations.tsv'.
It prompts GPT (da-vinci-003) to generate all possible presuppositions carried by each question in the file.
It creates a .json file with one json item per presupposition, where the question is the premise and the presupposition is the hypothesis.
It gives it the label 'E' for entailment, since GPT tends to generate mostly entailment items.
After the file is generated, the labels for items that are true presuppositions must be changed, and 'trigger_type' and 'type' filled in.
"""

def enter_text(input,output):
  with open(input,'r',encoding='utf-8') as f:
    finished_json_items = []
    lines = f.readlines()
    for line in lines:
      try:
        GPT_generated_text = askGPT(line)
        psps = GPT_generated_text.split("\n")
        for psp in psps:
          try:
            if psp[0].isdigit():
              result = psp[3:]
            else:
              result = psp
          except IndexError:
              print(psp)

          new_json = {
            'premise': line,
            'hypothesis': result,
            'label': 'E',
            'trigger_type': 'na',
            'type': 'na'
          }
          finished_json_items.append(new_json)
          print("append")
      except openai.error.RateLimitError as e:
        print(e)
        continue

      except openai.error.ServiceUnavailableError as e:
        print(e)
        continue

      except openai.error.APIError as e:
        print(e)
        continue

      except OSError as e:
        print(e)
        continue

    with open(output,'w',encoding='utf-8') as w:
      item = json.dumps(finished_json_items,indent=4)
      w.write(item)
  
      
def askGPT(text):
    openai.api_key = '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'
    prompt = "Please generate all possible presuppositions carried by this sentence: " + text
    response = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    temperature = 0.6,
    max_tokens = 100,
    )
  # Print the generated response
    return response.choices[0].text.strip()