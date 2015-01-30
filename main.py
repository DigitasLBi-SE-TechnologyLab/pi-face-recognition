
import argparse
import platform

from detect import Detector

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Start for face recognition client')
  parser.add_argument('--ip', help='Ip of recognition server')
  parser.add_argument('--port', help='Port of recognition server')

  args = parser.parse_args()

  detector = Detector(args.ip, args.port)

  if platform.system() == 'Windows' or platform.system() == 'Darwin':
    import win_recorder
    win_recorder.record_forever(detector)
  else:  
    import pi_recorder
    pi_recorder.record_forever(detector)