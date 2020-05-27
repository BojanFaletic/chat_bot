
from personality import Personality
from tkinter import *
import tkinter
import random
import json
from keras.models import load_model
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


# get basic lemma from sentence

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))


# run deep neural network trough learned model
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    print('ints:', ints)

    # special states indicates command
    res = getResponse(ints, intents)
    return res

# Creating GUI with tkinter


def send(_=None):
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

    # update emotional state of chatbot
    update_emotion_state(msg)

# render emotion of agent
def update_emotion_state(text):
    # get lemmas from sentence
    words = clean_up_sentence(text)
    feeling = personality.word_to_mood(words)
    print(feeling)
    if feeling is not None:
        key_name = list(feeling)[0]
        mood = personality.get_mood(
            insert_emotion=key_name, prob=feeling[key_name]*3)
    else:
        mood = personality.get_mood()

    ChatLog2.config(state=NORMAL)
    ChatLog2.config(foreground="#442265", font=("Verdana", 12))
    ChatLog2.delete("0.0", END)
    ChatLog2.insert(END, 'Chat bot is:' + mood)
    ChatLog2.config(state=DISABLED)
    ChatLog2.yview(END)


base = Tk()
base.title("Chat bot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog2 = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)
ChatLog2.config(state=DISABLED)

# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")

# Current emotion
scrollbar2 = Scrollbar(base, command=ChatLog.yview, cursor="heart")


ChatLog['yscrollcommand'] = scrollbar.set
ChatLog2['yscrollcommand'] = scrollbar2.set


# Create Button to send message
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                    command=send)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="29",
                height="5", font="Arial", fg='black')
EntryBox.bind("<Return>", send)


# Place all components on the screen
scrollbar.place(x=376, y=6, height=386)
ChatLog.place(x=6, y=6+20, height=386-20, width=370)
ChatLog2.place(x=6, y=6, height=20, width=370)

EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

# GUI generated, create personality agent
personality = Personality()

# TKinter main loop
base.mainloop()
