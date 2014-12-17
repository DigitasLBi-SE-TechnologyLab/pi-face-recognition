
import json
import random

class Greeter:
  GREETINGS_FILE = 'greetings.json'

  def __init__(self):
    self.load_greetings()

  def load_greetings(self):
    with open(self.GREETINGS_FILE, 'r') as file:
      self.greetings = json.load(file)

  def greet(self, name=None):
    greetings_category = 'known'
    if name is None:
      greetings_category = 'unknown'

    greetings = self.greetings[greetings_category]
    greeting = greetings[random.randint(0, len(greetings)-1)]

    greeting = greeting.replace('{name}', name or 'stranger')

    print greeting

