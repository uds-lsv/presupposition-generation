from negate import Negator

# Use default model (en_core_web_md):
negator = Negator(use_transformers=True)


def make_negated(sentence):
    negated_sentence = negator.negate_sentence(sentence)

    return negated_sentence  # "An apple a day, doesn't keep the doctor away."

