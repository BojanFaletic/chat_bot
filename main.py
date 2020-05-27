
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

# global variables


class Chatbot:
    def __init__(self):
        self.PLAY_AUDIO = True 
        self.personality = Personality()
        self.bot_mood = 'natural'

        self.create_gui()
        self.run()

    # get basic lemma from sentence
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(
            word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


    def bow(self,sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
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
    def predict_class(self, sentence, model):
        # filter out predictions below a threshold
        p = self.bow(sentence, words, show_details=False)
        res = model.predict(np.array([p]))[0]
        
        # Increased threshold to avoid misunderstanding
        ERROR_THRESHOLD = 0.97
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []

        # check if user intent is clear
        if len(results) > 0:
            for r in results:
                return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        else:
            return_list.append({"intent": 'noanswer', "probability": '1'})
            
        return return_list


    def getResponse(self, ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag'] == tag):
                result = random.choice(i['responses'])
                break
        return result


    def chatbot_response(self, msg):
        ints = self.predict_class(msg, model)
        print('ints:', ints)

        # special states indicates command
        res = self.getResponse(ints, intents)
        return res

    # Creating GUI with tkinter


    def send(self, _=None):
        msg = self.EntryBox.get("1.0", 'end-1c').strip()
        self.EntryBox.delete("0.0", END)

        if msg != '':
            self.ChatLog.config(state=NORMAL)
            self.ChatLog.insert(END, "You: " + msg + '\n\n')
            self.ChatLog.config(foreground="#442265", font=("Verdana", 12))

            res = self.chatbot_response(msg)
            self.ChatLog.insert(END, "Bot: " + res + '\n\n')

            self.ChatLog.config(state=DISABLED)
            self.ChatLog.yview(END)

        # update emotional state of chatbot
        self.update_emotion_state(msg)
        if self.PLAY_AUDIO:
            self.bot_speak(msg)

    # render emotion of agent
    def update_emotion_state(self,text):
        # get lemmas from sentence
        words = self.clean_up_sentence(text)
        feeling = self.personality.word_to_mood(words)
        print(feeling)
        if feeling is not None:
            key_name = list(feeling)[0]
            bot_mood = self.personality.get_mood(
                insert_emotion=key_name, prob=feeling[key_name]*5)
        else:
            bot_mood = self.personality.get_mood()

        self.ChatLog2.config(state=NORMAL)
        self.ChatLog2.config(foreground="#442265", font=("Verdana", 12))
        self.ChatLog2.delete("0.0", END)
        self.ChatLog2.insert(END, 'Chat bot is:' + bot_mood)
        self.ChatLog2.config(state=DISABLED)
        self.ChatLog2.yview(END)


    # speak text
    def bot_speak(self, msg):
        self.personality.speak_with_mood(msg)

    def toggle_speech(self):
        self.PLAY_AUDIO ^= 1


    def create_gui(self):
        self.base = Tk()
        self.base.title("Chat bot")
        self.base.geometry("400x500")
        self.base.resizable(width=FALSE, height=FALSE)

        # Create Chat window
        self.ChatLog = Text(self.base, bd=0, bg="white", height="8", width="50", font="Arial",)

        self.ChatLog2 = Text(self.base, bd=0, bg="white", height="8", width="50", font="Arial",)

        self.ChatLog.config(state=DISABLED)
        self.ChatLog2.config(state=DISABLED)

        # Bind scrollbar to Chat window
        self.scrollbar = Scrollbar(self.base, command=self.ChatLog.yview, cursor="heart")

        # Current emotion
        self.scrollbar2 = Scrollbar(self.base, command=self.ChatLog.yview, cursor="heart")


        self.ChatLog['yscrollcommand'] = self.scrollbar.set
        self.ChatLog2['yscrollcommand'] = self.scrollbar2.set


        # Create Button to send message
        self.SendButton = Button(self.base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                            bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                            command=self.send)

        # create audio button

        self.AudioButton = Button(self.base, font=("Verdana", 12, 'bold'), text="Talk", width="12", height=5,
                            bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                            command=self.toggle_speech)

        # Create the box to enter message
        self.EntryBox = Text(self.base, bd=0, bg="white", width="29",
                        height="5", font="Arial", fg='black')
        self.EntryBox.bind("<Return>", self.send)


        # Place all components on the screen
        self.scrollbar.place(x=376, y=6, height=386)
        self.ChatLog.place(x=6, y=6+20, height=386-20, width=370)
        self.ChatLog2.place(x=6, y=6, height=20, width=300)
        # insert button at 300 width


        self.EntryBox.place(x=128, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=90)
        self.AudioButton.place(x=300,y=6, height=20, width=70)

       
    
    def run(self):
        # TKinter main loop
        self.base.mainloop()

bot = Chatbot()