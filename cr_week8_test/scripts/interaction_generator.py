#!/usr/bin/env python

import rospy
from cr_week8_test.msg import object_info
from cr_week8_test.msg import human_info
import random
import numpy as np


# Function increments id and generated random data with every new interaction
def interaction_generator():

    # Initialising the node with the name interaction_generator
    rospy.init_node('interaction_generator', anonymous=True)
    
    # Declaring the publishing nodes
    # pub1 node is publishing to the obejct_info topic using object_info as message type
    pub1 = rospy.Publisher('objectInfo', object_info, queue_size=10)
    # pub2 node is publishing to the human_info topic using human_info as message type
    pub2 = rospy.Publisher('humanInfo', human_info, queue_size=10)

    # Setting the interaction rate every 10 sec
    rate = rospy.Rate(0.1)

    # Creaing objects of the object_info and human_info msg
    obj_objectInfo = object_info()
    obj_humanInfo = human_info()

    # Initializing the interaction id= 0
    interaction_id =1

    # Checking the flag whether to exit or not
    while not rospy.is_shutdown():
        # Setting the id
        obj_objectInfo.id = interaction_id
        obj_humanInfo.id = interaction_id
        
        # Randomly initializing between the range for every interaction
        obj_objectInfo.object_size = round(np.random.uniform(1,2))
        obj_humanInfo.human_expression = round(np.random.uniform(1,3))
        obj_humanInfo.human_action = round(np.random.uniform(1,3))
        
        rospy.loginfo(obj_objectInfo)
        rospy.loginfo(obj_humanInfo)

        # Publishing the id and object size to the object_info topic
        pub1.publish(obj_objectInfo)
        # Publishing the id, expression and action to the human_info topic
        pub2.publish(obj_humanInfo)

        rate.sleep()

        # Incrementing the interaction id for every new interaction
        interaction_id += 1


if __name__ == "__main__":
    try:
        interaction_generator()  
    #Making sure to not accidently continue executing the code after sleep()
    except rospy.ROSInterruptException:
        pass
