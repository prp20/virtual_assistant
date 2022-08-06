import json 
import numpy as np
from tensorflow import keras

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

with open("intents.json") as file:
    data = json.load(file)

#load trained model
model = keras.models.load_model('chat_model')

# load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

def smart_chat(text_input):
    global model, tokenizer, lbl_encoder, data
    max_len = 20
    response = None

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text_input]),truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])
    print(tag)
    for i in data['intents']:
        if i['tag'] == tag:
            response = np.random.choice(i['responses'])
    return (tag, response)