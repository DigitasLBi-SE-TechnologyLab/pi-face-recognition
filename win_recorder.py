
import cv2

def get_frame(cam):
	_, frame = cam.read()
	_, data = cv2.imencode('.jpg', frame)
	return data

def record_forever(detector):
	cam = cv2.VideoCapture(0)
	# detector.set_threading_enabled(True)

	while True:
		image_data = get_frame(cam)
		detector.detect_image(image_data)

	cam.release()
