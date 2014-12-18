# greeter.py

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


