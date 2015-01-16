# greeter.py

import time
import json
import random
import subprocess
import os

import config

FNULL = open(os.devnull, 'w')

class Greeter:
  GREETINGS_FILE = 'greetings.json'
  # settings overriden by config file
  enabled_output = {
    "voice": False,
    "print": True
  }
  confidence_threshold = 1500
  greeting_delay_s = 30
  recent_greetings = {}


  def __init__(self):
    self.config = config.get()
    self.load_greetings()

    if 'output_methods' in self.config:
      self.set_output_methods(self.config['output_methods'])
    if 'greeting_delay_s' in self.config:
      self.greeting_delay_s = self.config['greeting_delay_s']
    if 'confidence_threshold' in self.config:
      self.confidence_threshold = self.config['confidence_threshold']


  def load_greetings(self):
    with open(self.GREETINGS_FILE, 'r') as file:
      self.greetings = json.load(file)


  def set_output_methods(self, options):
    s = options.split('|')
    self.enabled_output["voice"] = True if "voice" in s else False
    self.enabled_output["print"] = True if "print" in s else False


  def log(self, *argv):
    if self.enabled_output['print']:
      print ' '.join(argv)

  
  def speak(self, message):
    self.log(message)
    if self.enabled_output['voice']:
      subprocess.call(['espeak', message], stdout=FNULL, stderr=subprocess.STDOUT)

  def is_recognized(self, face):
    return face['Name'] != 'Unknown' and face['Confidence'] < self.confidence_threshold

  def get_known_faces(self, faces):
    return [face for face in faces if self.is_recognized(face)]


  def get_greeting(self, category):
    greetings = self.greetings[category]
    greeting = greetings[random.randint(0, len(greetings)-1)]
    # add regex data replace
    return greeting



  def greet(self, name=None):
    if name is not None:
      now = time.time()
      if name in self.recent_greetings:
        last_greeting = self.recent_greetings[name]
        if now - last_greeting < self.greeting_delay_s:
          self.log('recently greeted %s' % name)
          return
      self.recent_greetings[name] = now

    greetings_category = 'known'
    if name is None:
      greetings_category = 'unknown'

    greeting = self.get_greeting(greetings_category)

    greeting = greeting.replace('{name}', name or 'stranger')

    self.speak(greeting)
      

  def greet_multiple(self, faces):
    known = self.get_known_faces(faces)
    unknown = [face for face in faces if face not in known]

    greeting = self.get_greeting('multiple')
    greeting = greeting.replace('{count}', str(len(faces)))
    greeting = greeting.replace('{known_count}', str(len(known)))
    greeting = greeting.replace('{unknown_count}', str(len(unknown)))

    self.speak(greeting)


  def greet_faces(self, faces):
    face_count = len(faces)

    if face_count == 0:
      self.log('no faces detected')
      return

    l = 'faces found %s'% ', '.join(['%s:%s' % (face['Name'],face['Confidence']) for face in faces])
    self.log(l)

    if face_count == 1:
      face = faces[0]
      name = face['Name']
      if not self.is_recognized(face):
        name = None
      self.greet(name)
      return

    # Greet multiple
    # self.greet_multiple(faces)
    self.greet(None)


if __name__ == '__main__':
  greeter = Greeter()
  greeter.set_output_methods('print')
  greeter.greet_faces([{
    "Name": "Hektor",
    "Confidence": 3000
  }, {
    "Name": "Robert",
    "Confidence": 2000
  }, {
    "Name": "Patric",
    "Confidence": 4500
  }])