
import picamera
import numpy
import io


def record_forever(Detector):
  detector = Detector()
  while True:
    data = io.BytesIO()

    with picamera.PiCamera() as camera:
      camera.capture(data, format='jpeg')

    image_data = numpy.fromstring(data.getvalue(), dtype=numpy.uint8)

    detector.detect_image(image_data)


if __name__ == '__main__':
  import detect
  record_forever(detect.Detector)

