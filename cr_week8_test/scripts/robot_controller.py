#!/usr/bin/env python

import rospy
from cr_week8_test.msg import perceived_info
from cr_week8_test.msg import robot_info
from cr_week8_test.srv import predict_robot_expression, predict_robot_expressionResponse
from bayesian.bbn import *



# Callback for the perceived_info topic
def callback(obj_perceivedInfo):
    try:
        predictRobotExpression = rospy.ServiceProxy('predict_robot_expression', predict_robot_expression)
        
        # Declaring the publishing nodes
        # pub4 node is publishing to the robot_info topic using robot_info as message type
        pub4 = rospy.Publisher('robotInfo', robot_info, queue_size=10)

        # Creaing object of the robot_info
        obj_robotInfo = robot_info()

        resp1 = predictRobotExpression(obj_perceivedInfo.object_size, obj_perceivedInfo.human_action, obj_perceivedInfo.human_expression)

        obj_robotInfo.id = obj_perceivedInfo.id
        obj_robotInfo.p_happy = resp1.p_happy
        obj_robotInfo.p_sad = resp1.p_sad
        obj_robotInfo.p_neutral = resp1.p_neutral
        
        rospy.loginfo(obj_robotInfo)
        pub4.publish(obj_robotInfo)
        
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


def robot_controller():

    # Initialising the node with the name robot_controller
    rospy.init_node('robot_controller', anonymous=True)

    # Subscribing to perceived_info topic
    rospy.Subscriber("perceivedInfo", perceived_info, callback)
    
    # keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == "__main__":
    robot_controller()