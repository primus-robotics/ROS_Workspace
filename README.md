# ROS Noetic Cheatsheet and Command Usages

## ROS Noetic Cheatsheet

```bash
# Launching ROS Master
roscore

# Launching a Package Node
rosrun package_name node_name

# Listing Available Topics
rostopic list

# Publishing a Message to a Topic
rostopic pub /topic_name message_type data

# Subscribing to a Topic
rostopic echo /topic_name

# Launching a Launch File
roslaunch package_name launch_file.launch

# Listing Active Nodes
rosnode list

# Getting Information About a Node
rosnode info /node_name



Command Usages
1. Create a ROS Package
catkin_create_pkg my_package rospy std_msgs
2. Build a ROS Package
catkin_make
3. Source ROS Environment
Before using ROS commands, make sure to source your ROS workspace:
source /path/to/your/catkin_workspace/devel/setup.bash

Replace "/path/to/your/catkin_workspace" with the actual path to your catkin workspace.

4. Run ROS Master
roscore

This command launches the ROS Master, which is required for communication between ROS nodes.
