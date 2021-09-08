#!/usr/bin/env python3
import rospy

import subprocess
text = 'Привет мир'
subprocess.call('echo '+text+'|festival --tts --language russian', shell=True)
print("end")