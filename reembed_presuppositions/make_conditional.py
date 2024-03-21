import openai
import json
import time

"""
This function turns declarative sentences into conditional ones.
Specifically, it takes the declarative sentence and embeds it into the andecedent of a conditional.
Example: "You are generating presuppositions." -> "If you're generating presuppositions, you're probably a linguist."

We generate these sentences with OpenAI's 'da-vinci-003' generative language model. We have different prompts based on what triggers the 
presupposition in the sentence, as it is important that the conditional sentence is such that it still triggers the presupposition.
"""

def make_conditional(sentence,trigger_type):
    conditional_sentence = 'na'
    if trigger_type == 'clefts':
        try:
            conditional_sentence = askGPT_cleft(sentence)
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
            conditional_sentence = askGPT_numeric_determiners(sentence)
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
            conditional_sentence = askGPT(sentence)
        except openai.error.RateLimitError as e:
            print(e)
        except openai.error.ServiceUnavailableError as e:
            print(e)
        except openai.error.APIError as e:
            print(e)
        except OSError as e:
            print(e)
    return conditional_sentence


def askGPT_cleft(text):
    openai.api_key = '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'
    prompt = "Turn this sentence into an if-clause while keeping the cleft, and write your own consequent." + "\n" + text
    response = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    temperature = 0.8,
    max_tokens = 100,
    )
  # Print the generated response
    return response.choices[0].text.strip()

def askGPT_numeric_determiners(text):
    openai.api_key = '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'
    prompt = "Turn this sentence into an if-clause while keeping the relative clause, and and write your own consequent." + "\n" + text
    response = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    temperature = 0.5,
    max_tokens = 100,
    )
  # Print the generated response
    return response.choices[0].text.strip()

def askGPT(text):
    openai.api_key = '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'
    prompt = "Turn this sentence into an if-clause, making as little changes to the original sentence as possible, and write your own consequent." + "\n" + text
    response = openai.Completion.create(
    engine = "text-davinci-003",
    prompt = prompt,
    temperature = 0.6,
    max_tokens = 100,
    )
  # Print the generated response
    return response.choices[0].text.strip()