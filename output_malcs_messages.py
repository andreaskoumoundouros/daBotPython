from operator import truediv
import chat_log_import
import pickle
import os
from json import load
from transformers import AutoTokenizer
from tokenizers.models import BPE
from tokenizers import Tokenizer
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.normalizers import NFKC, Sequence
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer
from pathlib import Path
import re

M_PLAINTEXT_FILE = './text/malcs_messages.txt'
M_TOKEN_SAVE_PATH = 'malcs_data'
M_CHAT_LOG_PATH = './discord_chat_logs/MINIFIED_main_chat.json'

class BPE_token(object):
    def __init__(self):
        self.tokenizer = Tokenizer(BPE())
        self.tokenizer.normalizer = Sequence([
            NFKC()
        ])
        self.tokenizer.pre_tokenizer = ByteLevel()
        self.tokenizer.decoder = ByteLevelDecoder()

    def bpe_train(self, paths):
        trainer = BpeTrainer(vocab_size=50000, show_progress=True, inital_alphabet=ByteLevel.alphabet(), special_tokens=[
            "<s>",
            "<pad>",
            "</s>",
            "<unk>",
            "<mask>"
        ])
        self.tokenizer.train(paths, trainer)

    def save_tokenizer(self, location, prefix=None):
        if not os.path.exists(location):
            os.makedirs(location)
        self.tokenizer.model.save(location, prefix)

class Msg_data:
    def __init__(self, msg, response) -> None:
        self.message = msg
        self.response = response

    message = ''
    response = ''

def isMalcs(message):
    if message['author']['id'] == '150490683269054464':
        return True
    
    return False

# Chat data contents: guild, channel, dateRange, messages, messageCount
chat_data = chat_log_import.importer(M_CHAT_LOG_PATH)
top_level_keys = chat_data.keys()

msg_cnt = chat_data['messageCount']
json_messages = chat_data['messages']
messages = []

i = 0
while i < msg_cnt:
    message = json_messages[i]
    if isMalcs(message):
        if len(message['content']) > 2:
            # If message from malcs append his message and any messages directly after from him and the previous message
            previous_msg = json_messages[i-1]['content']
            malcs_msg = message['content']

            while isMalcs(json_messages[i+1]):
                malcs_msg += ' ' + json_messages[i+1]['content'].strip()
                i += 1

            messages.append(re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',malcs_msg) + '\n')
    i += 1

with open(M_PLAINTEXT_FILE, 'w+', encoding='utf-8') as f:
    f.writelines(messages)

tokenizer = BPE_token()# train the tokenizer model
tokenizer.bpe_train([M_PLAINTEXT_FILE])# saving the tokenized data in our specified folder 
tokenizer.save_tokenizer(M_TOKEN_SAVE_PATH)
