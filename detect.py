
import httplib
import urllib
import base64
import threading
import json

from greeter import Greeter

IP = 'se-hekwal'
PORT = '8090'

class Detector:
  headers = {
    'form': {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
  }
  threading_enabled = False

  def __init__(self):
    self.greeter = Greeter()


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

    conn = httplib.HTTPConnection(IP, PORT)
    conn.request('POST', '/api/face/detect', urllib.urlencode(params), headers)
    self.handle_response(conn.getresponse())
    conn.close()


  def handle_response(self, response):
    if response.status != 200 or response.reason != 'OK':
      print 'Error in response from server', response.status, response.reason
      print response.read()
      return

    faces = json.loads(response.read())

    if not faces:
      print 'no faces detected'
      return

    # Only one face
    if len(faces) == 1:
      face = faces[0]
      name = face['Name']
      name = name if name is not 'Unknown' else None
      self.greeter.greet(name)
    else:
      self.greeter.greet(None)


