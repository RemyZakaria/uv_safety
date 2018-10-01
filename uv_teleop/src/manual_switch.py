#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import std_srvs.srv

class ClassName:
    def __init__(self):
        #      ROSNODE
        rospy.init_node('vision_navigation', anonymous=True)
        self.teleop_joy_subscriber = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.uv_trigger_req = std_srvs.srv.SetBoolRequest()
        rospy.loginfo("Waiting for /switch_uv service...")
        rospy.wait_for_service("/switch_uv")
        self.uv_trigger_client = rospy.ServiceProxy("/switch_uv", std_srvs.srv.SetBool)
        #self.velocity_publisher = rospy.Publisher('/teleop_joy/cmd_vel', Twist, queue_size=10)

        #      MESSAGETYPES
        self.controller = Joy()
        #self.cmd_vel = Twist()

        #      CONSTANTS
        self.rate = rospy.Rate(30)

        #      VARIABLES
        #self.run_state = False


    def joy_callback(self, data):
        self.controller = data
        if self.controller.buttons[0] == 1:
            print("True")
            self.uv_trigger_req.data = True
            result = self.uv_trigger_client.call(self.uv_trigger_req.data)
        if self.controller.buttons[1] == 1:
            print("False")
            self.uv_trigger_req.data = False
            result = self.uv_trigger_client.call(self.uv_trigger_req.data)
        
        # if self.controller.buttons[6] == 1 and self.controller.buttons[7] == 1:
        #     self.run_state = True
        # if self.controller.buttons[6] == 1:
        #     self.run_state = False


    def main_function(self):
        while not rospy.is_shutdown():
            self.rate.sleep()


if __name__ == '__main__':
    print("On")
    try:
        x = ClassName()
        x.main_function()
    except rospy.ROSInterruptException:
        pass
