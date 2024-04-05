#!/usr/bin/env python3

# ROS subscriber code

import rospy
from std_msgs.msg import String  # Correct import statement

def callback(data):
    rospy.loginfo("Received Message: %s", data.data)

def subscriber_node():
    rospy.init_node('subscriber_node', anonymous=True)  # Correct 'anonymous' argument
    rospy.Subscriber('chatter', String, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        subscriber_node()
    except rospy.ROSInterruptException:
        pass
