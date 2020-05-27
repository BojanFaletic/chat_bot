import numpy as np
from markov_chains import Markov_chain
from emotions import Emotions
from audio_interface import Audio

class Personality:
    # markov chain for mood
    mood_tranzitions = {
        'happy': {'happy': 0.8,
                  'netural': 0.15,
                  'sad': 0.05},
        'netural': {'happy': 0.25,
                    'netural': 0.5,
                    'sad': 0.25},
        'sad': {'happy': 0.05,
                'netural': 0.15,
                'sad': 0.8}
    }

    # markov chain for emotion
    emotion_tranzitions = {
        'smile': {
            'smile': 0.8,
            'netural': 0.15,
            'cry': 0.05
        },
        'netural': {
            'smile': 0.5,
            'netural': 0.4,
            'cry': 0.01
        },
        'cry': {
            'smile': 0.1,
            'netural': 0.6,
            'cry': 0.3
        }
    }

    def __init__(self):
        self.mood = Markov_chain(self.mood_tranzitions)
        self.emotion = Markov_chain(self.emotion_tranzitions)

        # set state of agent
        self.current_mood = np.random.choice(['happy', 'netural', 'sad'])
        self.current_emotion = np.random.choice(['smile', 'netural', 'cry'])

        # get meaningfull words
        self.e = Emotions()
        self.e.load_dictionary('emotions.json')
        self.e.load_compact()

        # load audio 
        self.voice = Audio()

    # get current mood of agent
    def get_mood(self, insert_emotion=None, prob=None):
        if insert_emotion and prob:
            # change mood if emotion is added with some probability
            p = int(prob*100)
            if np.random.randint(0, 100) <= p:
                happy = ['happy', 'joy', 'trust', 'anticipations']
                sad = ['fear', 'sadness', 'disgust']

                if insert_emotion in happy:
                    self.current_mood = 'happy'
                elif insert_emotion in sad:
                    self.current_mood = 'sad'
                else:
                    self.current_mood = 'natural'
        else:
            self.current_mood = self.mood.next_state(self.current_mood)
        return self.current_mood

    # get current emotion of agent
    def get_emotion(self):
        self.current_emotion = self.emotion.next_state(self.current_emotion)
        return self.current_emotion


    # high level function
    def word_to_mood(self, key_words):
        if len(key_words) > 0:
            for key in key_words:
                for word in self.e.emotions2:
                    if key in self.e.emotions2[word]:
                        meaningfull_word = {word : self.e.emotions2[key][word]}
                        return meaningfull_word

#p = Personality()


#print(p.word_to_mood(['happy2']))


'''
p = Personality()

print(p.current_mood)
print(p.get_mood('joy', 0.5))

'''
