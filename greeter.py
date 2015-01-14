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

  def greet(self, name=None):
    if name is not None:
      now = time.time()
      if name in self.recent_greetings:
        last_greeting = self.recent_greetings[name]
        if now - last_greeting < self.greeting_delay_s:
          if self.enabled_output["print"]:
            print 'recently greeted %s' % name
          return
      self.recent_greetings[name] = now


    greetings_category = 'known'
    if name is None:
      greetings_category = 'unknown'

    greetings = self.greetings[greetings_category]
    greeting = greetings[random.randint(0, len(greetings)-1)]

    greeting = greeting.replace('{name}', name or 'stranger')

    if self.enabled_output['print']:
      print greeting
    if self.enabled_output['voice']:
      subprocess.call(['espeak', greeting], stdout=FNULL, stderr=subprocess.STDOUT)

  def greet_faces(self, faces, known):
    face_count = len(faces)

    if face_count == 0:
      if self.enabled_output['print']:
        print 'no faces detected'
      return

    if face_count == 1:
      self.greet(face if face is not 'Unknow' else None)
      return

    

