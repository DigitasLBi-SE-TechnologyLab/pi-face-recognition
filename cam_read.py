
import picamera
import numpy
import io

import httplib
import urllib
import base64

import json

import greeter

IP = 'se-hekwal'
PORT = '8090'

content_types = {
  'form': 'application/x-www-form-urlencoded; charset=UTF-8'
}

Greeter = greeter.Greeter()

def detect_image(image_data):
  params = {
    '': base64.b64encode(image_data)
  }
  headers = {
    'Content-Type': content_types['form']
  }

  conn = httplib.HTTPConnection(IP, PORT)
  conn.request('POST', '/api/face/detect', urllib.urlencode(params), headers)
  handle_response(conn.getresponse())
  conn.close()


def handle_response(response):
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
    Greeter.greet(name)
  else:
    Greeter.greet(None)



def record_cam():
  while True:
    data = io.BytesIO()

    with picamera.PiCamera() as camera:
      camera.capture(data, format='jpeg')

    image_data = numpy.fromstring(data.getvalue(), dtype=numpy.uint8)

    detect_image(image_data)




if __name__ == '__main__':
  record_cam()

