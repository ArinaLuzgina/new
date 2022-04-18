#!/usr/bin/env python3

from turtlebro_patrol.srv import PatrolPointCallback, PatrolPointCallbackRequest, PatrolPointCallbackResponse 
from ws_turtlebro_package.srv import ArucoDetect, ArucoDetectResponse, ArucoDetectRequest
from ws_turtlebro_package.srv import WayLan_Choice
from std_msgs.msg import UInt16
import rospy
import subprocess

#color = 3 - красный цвет, color = 2 - жёлтый цвет, color = 1 - зелёный цвет
color = 1
def say_text(text, language):    
    rospy.loginfo(f"Start speech: {text}")
    if language == 'R':
        subprocess.call('echo '+text+'|festival --tts --language russian', shell=True)
    elif language == 'E':
        subprocess.call('echo '+text+'|festival --tts --language english', shell=True)
    rospy.loginfo("Speech end")

def handle_request(req:PatrolPointCallbackRequest):
    global color
    point_name = req.patrol_point.name
    
    text = ""
    rospy.wait_for_service("button_srv")
    service_caller = rospy.ServiceProxy("button_srv", WayLan_Choice)
    resp = service_caller()
    language = resp.lan
    aruco_result = aruco_detect.call(ArucoDetectRequest())

    if language == 'R':
        if point_name == "home":
            text = "Я дома"
            color = 3
            pub.publish(3)
        

        if aruco_result.id == 2:
            text += "Это картина под нназванием плачущий мальчик. Она представляет проблему общества связанную с зависимостью от лайков."
        elif aruco_result.id == 3:
            text += "Это картина под названием качели. Она выполнена в стиле графити."
        elif aruco_result.id == 6:
            text += "Это картина под названием кровавой дождь. На ней вы можете увидеть как человек идет с зонтом, прикрываясь от кровавого дождя."
        elif aruco_result.id == 4:
            text += "Это картина под названием граффитист. На ней робот рисует куар код."
    elif language == 'E':
        if point_name == "home":
            text = "I am at home"
            color = 3
            pub.publish(3)
        if aruco_result.id == 2:
            text += "This is a painting called a crying boy. It is a problem associated with addiction to likes."
        elif aruco_result.id == 3:
            text += "This is a picture called swing. It is done in graffiti style."
        elif aruco_result.id == 6:
            text += "It's a painting called bloody rain. On it, you can see how a man walks with an umbrella, hiding from the bloody rain."
        elif aruco_result.id == 4:
            text += "It's a painting called graffiti. On it the robot draws a qar code."
    print(text)
    if color == 3:
        say_text(text, language)
    elif text == '':
        color = 1
        pub.publish(1)
    else:
        color = 2
        pub.publish(2)
        say_text(text, language)
        color = 1
        pub.publish(1)
    color = 1
    return PatrolPointCallbackResponse(1, "Speech end")

rospy.init_node('excursion_point_service')
s = rospy.Service('ws_turtlebro_package', PatrolPointCallback, handle_request)
aruco_detect = rospy.ServiceProxy('aruco_detect', ArucoDetect)
pub = rospy.Publisher('/led_color', UInt16, queue_size = 2)

rospy.loginfo("Ready to speak points")
rospy.spin()
