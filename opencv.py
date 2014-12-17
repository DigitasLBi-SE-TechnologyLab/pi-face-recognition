
import cv2
import numpy
import base64

import httplib
import urllib

cap = cv2.VideoCapture(0)

IP = 'localhost'
PORT = '54465'

content_types = {
  'form': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def capture_frame_jpg():
	_, frame = cap.read()
	_, data = cv2.imencode('.jpg', image)
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# cv2.imshow('image', frame)
	# cv2.waitKey(0)
	return frame.toString()


def capture_and_send(ip, port):
	frame = capture_frame_jpg()
	send_image(ip, port, frame)

def send_image(ip, port, image_data):
  params = {
    '': base64.b64encode(image_data)
  }
  headers = {
    'Content-Type': content_types['form']
  }

  conn = httplib.HTTPConnection(ip, port)
  conn.request('POST', '/api/face/detect', urllib.urlencode(params), headers)
  response = conn.getresponse()
  print(response.status, response.reason)
  print(response.read())
  conn.close()


capture_and_send(IP, PORT)

cap.release()
cv2.destroyAllWindows()

