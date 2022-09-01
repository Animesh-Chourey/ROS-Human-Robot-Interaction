#!/usr/bin/env python
import rospy
from cr_week8_test.msg import human_info
from cr_week8_test.msg import object_info
from cr_week8_test.msg import perceived_info
import numpy as np

class Callback:
    def __init__(self, perceived_info):
        self.id = 0
        self.object_size = 0
        self.human_action = 0
        self.human_expression = 0
        self.perceived_info = perceived_info

    def callback1(self, data):
        #function that return the data(msg) from the object publisher
        rospy.loginfo(rospy.get_caller_id() + "\n object heard \n%s", data) #make log of generated msg 
        
        # Storing the published id and object size
        self.id = data.id
        self.object_size = data.object_size
 
    def callback2(self, data):
        #function that return the data(msg) from the human publisher
        rospy.loginfo(rospy.get_caller_id() + "\n human heard \n%s", data) #make log of generated msg 

        # Storing the published human action and human expression
        self.human_action = data.human_action    
        self.human_expression = data.human_expression

        # Randomly filter the information
        self.filter_information()

        # Publish the data
        self.publish_new_data(perceived_info)
        
    
    def filter_information(self):
        # Function to check whether the random filter is equal to the following conditions
        random_choice = int(np.random.uniform(1,8))
        
        # Changing object size, human action and human expression to 0 if conditions met
        if random_choice==1:
            self.object_size = 0
        elif random_choice==2:
            self.human_action = 0
        elif random_choice==3:
            self.human_expression = 0
        elif random_choice==4:
            self.object_size = 0
            self.human_action = 0
        elif random_choice==5:
            self.object_size = 0
            self.human_expression = 0
        elif random_choice==6:
            self.human_action = 0
            self.human_expression = 0
        elif random_choice==7:
            self.object_size = 0 
            self.human_action = 0
            self.human_expression = 0
        elif random_choice==8:
            pass

    def publish_new_data(self, perceived_info):
        # Declaring the publishing nodes
        # pub3 node is publishing to the perceived_info topic using perceived_info as message type
        pub3 = rospy.Publisher('perceivedInfo', perceived_info, queue_size=10)
    
        # Creaing object of the perceived_info
        obj_perceivedInfo = perceived_info()
        
        # Updating the parameters of perceived_info
        obj_perceivedInfo.id = self.id
        obj_perceivedInfo.object_size = self.object_size 
        obj_perceivedInfo.human_action = self.human_action 
        obj_perceivedInfo.human_expression = self.human_expression 

        # Publishing the id and object size to the perceived_info topic
        pub3.publish(obj_perceivedInfo)

        rospy.loginfo(obj_perceivedInfo)
    

def perception_filter():
    # Initialising the node with the name perception_filter
    rospy.init_node('perception_filter', anonymous=True)
    
    obj = Callback(perceived_info)
    
    # Subscribing to object_info topic and human_info topic
    rospy.Subscriber("objectInfo", object_info, obj.callback1) 
    rospy.Subscriber("humanInfo", human_info, obj.callback2)

    # keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    perception_filter() #calling the subscriber node function