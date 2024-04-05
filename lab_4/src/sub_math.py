#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

def pos_callback(data):
    pos = data.data
    omega = 20
    velocity = omega * pos
    print(velocity)

def velocity_sub():
    rospy.init_node('velocity_sub_node', anonymous=True)
    rospy.Subscriber('position_out', Int32, pos_callback)
    rospy.spin()

if __name__ == "__main__":
    velocity_sub()
