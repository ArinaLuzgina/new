#!/usr/bin/env python3
import rospy
from turtlebro_patrol.msg import PatrolPoint
from std_msgs.msg import String
import subprocess


rospy.init_node('point_speech')


def patrol_cb(msg: PatrolPoint):

    if msg.name == "1":
        text = "Я в точке 1"

    if msg.name == "2":
        text = "Я в точке 2"

    if msg.name == "home":
        text = "Я дома"

    if text :
        # not make pause at home point
        if msg.name == "home":
            say_text(text)
        else :
            pub.publish("point_pause")
            say_text(text)   
            pub.publish("point_resume")


sub = rospy.Subscriber('/patrol_control/reached', PatrolPoint, patrol_cb)
pub = rospy.Publisher('/patrol_control', String, queue_size=1)


def say_text(text):
    print(f"Ready to Speech: {text}")
    subprocess.call('echo '+text+'|festival --tts --language russian', shell=True)
    print("Speech end")

rospy.spin()
