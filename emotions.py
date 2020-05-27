import json

class Emotions:
  def __init__(self):
    # basic structure
    self.emotions = {
      'fear' : [],
      'happy' : [],
      'sadness' : [],
      'joy' : [],
      'disgust' : [],
      'surprise' : [],
      'trust' : [],
      'anticipation' : []
    }
    # optimized for searching
    self.emotions2 = {
      'fear' : {},
      'happy' : {},
      'sadness' : {},
      'joy' : {},
      'disgust' : {},
      'surprise' : {},
      'trust' : {},
      'anticipation' : {}
    }

  # add word to dictionary
  def add_word(self, word, emotion, prob):
    self.emotions[emotion] += [{word : prob}]

  # basic load from file
  def load_dictionary(self, dict_name):
    with open(dict_name) as file:
      data = json.load(file)
    self.emotions = data

  # save 
  def save_dictionary(self, dict_name):
    with open(dict_name,'w') as fp:
      json.dump(self.emotions, fp, sort_keys=True, indent=4)


  # transform state from emotion to emotions2, for faster searching
  def load_compact(self):
    for key in list(self.emotions):
      [self.emotions2[key].update(x) for x in self.emotions[key]] 


'''
common_emotions = {
  'Fear' : {
    'name' : prob
  }

'''

em = Emotions()
em.load_dictionary('emotions.json')

#em.add_word('lucky', 'happy', 0.2)
#em.save_dictionary('emotions.json')
em.load_compact()

print(em.emotions)
print(em.emotions2['trust'])
