

import platform
from detect import Detector

if __name__ == '__main__':
  detector = Detector()
  if platform.system() == 'Windows':
    import win_recorder
    win_recorder.record_forever(detector)
  else:  
    import pi_recorder
    pi_recorder.record_forever(detector)