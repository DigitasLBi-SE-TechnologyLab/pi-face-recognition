# detect.py


import httplib
import urllib
import base64
import threading
import json

import config

from greeter import Greeter

# IP = '157.125.54.102'
IP = 'localhost'
PORT = '8090'
# PORT = '8095'
# PORT = '54465'

# TODO
# Throttle requests when receiving errors from server

class Detector:
  headers = {
    'form': {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
  }
  threading_enabled = False

  confidence_threshold = 4000

  def __init__(self, ip=None, port=None):
    self.config = config.get()
    self.ip = ip or ('server_ip' in self.config['server_ip'] or IP)
    self.port = port or ('server_port' in self.config['server_port'] or PORT)
    self.greeter = Greeter()
    # self.greeter.set_output_methods('voice|print')


  def set_threading_enabled(self, value):
    self.threading_enabled = value


  def detect_image(self, image_data):
    if self.threading_enabled:
      t = threading.Thread(target=self.send_request, args=(image_data,))
      t.start()
    else:
      self.send_request(image_data)


  def send_request(self, image_data):
    params = {
      '': base64.b64encode(image_data)
    }
    headers = self.headers['form']

    conn = httplib.HTTPConnection(self.ip, self.port)
    conn.request('POST', '/api/face/detect', urllib.urlencode(params), headers)
    self.handle_response(conn.getresponse())
    conn.close()


  def handle_response(self, response):
    if response.status != 200 or response.reason != 'OK':
      print 'Error in response from server', response.status, response.reason
      # print response.read()
      return

    faces = json.loads(response.read())

    self.greeter.greet_faces(faces)

    # if not faces:
    #   print 'no faces detected'
    #   return

    # # Only one face
    # if len(faces) == 1:
    #   face = faces[0]
    #   name = face['Name']
    #   confidence = face['Confidence']
    #   print 'Found %s with confidence %s' % (name, confidence)
    #   if name is 'Unknown' or confidence > self.confidence_threshold:
    #     name = None;
    #   self.greeter.greet(name)
    # else:
    #   self.greeter.greet(None)
