
# https://towardsdatascience.com/train-gpt-2-in-your-own-language-fc6ad4d60171
# The beginnings of a chat bot
# 1. Get chat data for training.
# 2. Process the data and prepare it for tokenizing.
#   - This should include getting the chat logs desired along with contextual data.
#   For eg. the chat message and the prior message which prompted the response and vice-versa
# 3. Tokenize the data so that it can be used for training. https://huggingface.co/transformers/preprocessing.html
# 4. Fine tune one of the pretrained huggingface models. https://huggingface.co/transformers/training.html

import transformers
from transformers import GPT2Config, TFGPT2LMHeadModel, GPT2Tokenizer
from transformers.file_utils import ModelOutput# loading tokenizer from the saved model path
from transformers import WEIGHTS_NAME, CONFIG_NAME
import os
import random

class Malcs:
    def __init__(self) -> None:
        output_dir = './malcs_model/'

        self.tokenizer = GPT2Tokenizer.from_pretrained(output_dir)
        self.model = TFGPT2LMHeadModel.from_pretrained(output_dir)

    def get_output(self, text):
        # encoding the input text
        input_ids = self.tokenizer.encode(text, return_tensors='tf')

        # getting out output
        beam_output = self.model.generate(
            input_ids,
            max_length = 50 + len(text),
            num_beams = 5,
            temperature = 1.0,
            no_repeat_ngram_size=2,
            num_return_sequences=1
        )

        output = self.tokenizer.decode(beam_output[0]).split('\n')
        output = random.choice([x for x in output[1:] if len(x) > 3])

        return output
    
    def get_full_output(self, text):
        # encoding the input text
        input_ids = self.tokenizer.encode(text, return_tensors='tf')

        # getting out output
        beam_output = self.model.generate(
            input_ids,
            max_length = 50 + len(text),
            num_beams = 5,
            temperature = 1.0,
            no_repeat_ngram_size=2,
            num_return_sequences=1
        )

        output = self.tokenizer.decode(beam_output[0]).split('\n')

        return output