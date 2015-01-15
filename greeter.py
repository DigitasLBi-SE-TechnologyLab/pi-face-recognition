# greeter.py

import time
import json
import random
import subprocess
import os

FNULL = open(os.devnull, 'w')

class Greeter:
  GREETINGS_FILE = 'greetings.json'
  enabled_output = {
    "voice": False,
    "print": True
  }

  confidence_threshold = 4000

  # only greet known names with 30s interval
  greeting_delay_s = 30
  recent_greetings = {}



  def __init__(self):
    self.load_greetings()


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


  def get_known_faces(self, faces):
    return [face for face in faces if face['Name'] != 'Unknown' and face['Confidence'] < self.confidence_threshold]


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
      self.greet(name if name is not 'Unknown' else None)
      return

    # Greet multiple
    self.greet_multiple(faces)


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