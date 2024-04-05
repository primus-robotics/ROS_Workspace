#!/usr/bin/env python3
import rospy
import actionlib
import sys
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from alexa_ros.msg import AlexaTaskAction, AlexaTaskResult, AlexaTaskGoal


class AlexaServer(object):
    # create messages that are used to publish feedback/result
    result_ = AlexaTaskResult()
    goal_positions = []
                       

    def __init__(self, name):

        self.action_name_ = name
        self.as_ = actionlib.SimpleActionServer(self.action_name_, AlexaTaskAction, execute_cb=self.execute_cb, auto_start = False)
        self.as_.start()
        rospy.loginfo('Simple Action Server Started')


    def execute_cb(self, goal):

        success = True

        #rospy.init_node('KukaArm_traj_msgs_publisher')
        contoller_name='/manipulator/main_controller/command'
        trajectory_publihser = rospy.Publisher(contoller_name,JointTrajectory, queue_size=10) 
        kuka_joints = ['link_1_joint','link_2_joint','link_3_joint','link_4_joint','link_grip_l_joint','link_grip_r_joint']

        if goal.task_number == 0:
            self.goal_positions = [0,0.84,0.53,-1.48,-0.01,0.02]
            rospy.sleep(1)
        elif goal.task_number == 1:
            self.goal_positions = [0.0,1.40,0.40,-0.61,-0.01,0.019]
            rospy.sleep(1)
        elif goal.task_number == 2:
            self.goal_positions = [-0.90,0.4,2.0,-1.075,0.0,0.019]
            rospy.sleep(1)
        elif goal.task_number == 3:
            self.goal_positions = [-0.80,-0.52,2.00,-0.44,-0.01,0.01]
            rospy.sleep(1)
        elif goal.task_number == 4:
            self.goal_positions = [-0.80,-2.0,2.0,-0.44,-0.01,0.01]
            rospy.sleep(1)
        else:
            rospy.logerr('Invalid goal')
            return
        
        ## creating a message to send Joint Trajectory type
        dual_armR_traj_msgs = JointTrajectory()
        dual_armR_traj_msgs.joint_names = kuka_joints
        dual_armR_traj_msgs.points.append(JointTrajectoryPoint())
        dual_armR_traj_msgs.points[0].positions = self.goal_positions
        dual_armR_traj_msgs.points[0].velocities = [0.0 for i in kuka_joints]
        dual_armR_traj_msgs.points[0].accelerations = [0.0 for i in kuka_joints]
        dual_armR_traj_msgs.points[0].time_from_start = rospy.Duration(3)
        rospy.sleep(1)
        trajectory_publihser.publish(dual_armR_traj_msgs) 
        
        # check that preempt has not been requested by the client
        if self.as_.is_preempt_requested():
            rospy.loginfo('%s: Preempted' % self.action_name_)
            self.as_.set_preempted()
            success = False
       
        # check if the goal request has been executed correctly
        if success:
            self.result_.success = True
            rospy.loginfo('%s: Succeeded' % self.action_name_)
            self.as_.set_succeeded(self.result_)  


if __name__ == '__main__':
    rospy.init_node('alexa_task')
    server = AlexaServer(rospy.get_name())
    rospy.spin()

