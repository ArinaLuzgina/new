#!/usr/bin/env python3

from turtlebro_patrol.srv import PatrolPointCallback, PatrolPointCallbackRequest, PatrolPointCallbackResponse 
import rospy
import subprocess

def say_text(text):    
    rospy.loginfo(f"Start speech: {text}")
    subprocess.call('echo '+text+'|festival --tts --language russian', shell=True)
    rospy.loginfo("Speech end")

def handle_request(req:PatrolPointCallbackRequest):

    point_name = req.patrol_point.name

    if point_name == "1":
        text = "Я в точке 1"

    if point_name == "2":
        text = "Я в точке 2"

    if point_name == "home":
        text = "Я дома"

    say_text(text)

    return PatrolPointCallbackResponse(1, "Speech end")


rospy.init_node('excursion_point_service')
s = rospy.Service('turtlebro_excursion', PatrolPointCallback, handle_request)
rospy.loginfo("Ready to speak points")
rospy.spin()