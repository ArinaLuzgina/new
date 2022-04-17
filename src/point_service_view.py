#!/usr/bin/env python3

from turtlebro_patrol.srv import PatrolPointCallback, PatrolPointCallbackRequest, PatrolPointCallbackResponse 
from ws_turtlebro_package.srv import ArucoDetect, ArucoDetectResponse, ArucoDetectRequest
from ws_turtlebro_package.srv import WayLan_Choice
import rospy
import subprocess

def say_text(text, language):    
    rospy.loginfo(f"Start speech: {text}")
    if language == 'R':
        subprocess.call('echo '+text+'|festival --tts --language russian', shell=True)
    elif language == 'E':
        subprocess.call('echo '+text+'|festival --tts --language english', shell=True)
    rospy.loginfo("Speech end")

def handle_request(req:PatrolPointCallbackRequest):

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

        

        if aruco_result.id > 0:
            text += f". Вижу маркер {aruco_result.id}"
    elif language == 'E':
        if point_name == "home":
            text = "I am at home"
        if aruco_result.id > 0:
            text += f". I can see marker {aruco_result.id}."

    say_text(text, language)

    return PatrolPointCallbackResponse(1, "Speech end")


rospy.init_node('excursion_point_service')
s = rospy.Service('ws_turtlebro_package', PatrolPointCallback, handle_request)
aruco_detect = rospy.ServiceProxy('aruco_detect', ArucoDetect)
rospy.loginfo("Ready to speak points")
rospy.spin()
