from datetime import datetime
from playsound import playsound
import sys
import os

alarm = open("alarm.txt", "r")
alarm_time = alarm.read()
print(alarm_time)
if ":" in alarm_time:
    pass
else:
    sys.exit()
alarm.close()

while alarm_time != datetime.now().strftime('%H:%M'):
    #print(alarm_time)
    if alarm_time == datetime.now().strftime('%H:%M'):
        #print("wake up")
        while os.path.isfile('alarm.stop') != True:
            playsound("alarm-ringtone.mp3")
        os.remove("alarm.stop")
        sys.exit()
        
    else:
        pass