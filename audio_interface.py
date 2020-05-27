import pyttsx3
import speech_recognition as sr


class Audio:
  def __init__(self):
      self.r = sr.Recognizer()
      self.m = sr.Microphone()
      self.s = pyttsx3.init()

      # calibrate microphone
      with self.m as self.source:
        self.r.adjust_for_ambient_noise(self.source)


  # change talk speed
  def set_talk_speed(self, speed = 125):
      self.s.setProperty('rate', speed)

  # change volume
  def set_volume(self, volume = 0.5):
    self.s.setProperty('volume', volume)

  # get text from user voice
  def get_text_form_audio(self):
    with self.m as source:
      print('Start talking')
      audio = self.r.listen(source)
      print('Sample taken, wait for processing ...')
    try:
      text = r.recognize_google(audio)
    except:
      text = "Sorry, can't understand you"
    print('Interpret audio as:', text)
    return text

  # speak text
  def speak(self,text):
    self.s.say(text)
    self.s.runAndWait()


#a = Audio()
#a.speak('Hello world')
#a.set_talk_speed(100)
#a.set_volume(0.3)
#a.speak('Hello world')


#a.get_text_form_audio()


#r = a.get_audio_text()

#print(r)

#if r is not None:
#  a.speak(r)
