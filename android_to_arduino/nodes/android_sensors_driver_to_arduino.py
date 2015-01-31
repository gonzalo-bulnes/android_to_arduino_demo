#!/usr/bin/env python
import roslib; roslib.load_manifest('android_to_arduino')
import rospy

# Input messages type
from sensor_msgs.msg import Imu
# Output messages type
from std_msgs.msg import Empty

class AndroidSensorsDriverToArduino(object):
  
    def __init__(self):
        """Toggle an Arduino board LED from Android Sensors Driver.

        This node links an android_sensors_driver publisher [1]
        and an Arduino subscriber [2].

        [1] http://www.ros.org/wiki/android_sensors_driver/Tutorials/Connecting%20to%20a%20ROS%20Master
        [2] http://www.ros.org/wiki/rosserial_arduino/Tutorials/Blink

        """
        # Create a publisher for the topic the Arduino node listens to.
        self.pub = rospy.Publisher('toggle_led', Empty)
        # Intitialize variables
        self.last_status = 0
        self.status = 0

    def callback(self, data):
        """A sensor_msgs/Imu callback method.

        This method is called each time a sensor_msgs/Imu message
        is received from the /android/imu topic.

        """
        if data.linear_acceleration.x > 0:
            self.status = 0
        else:
            self.status = 1
        if self.status != self.last_status:
            # Send toggle_led message
            self.pub.publish(Empty())
            self.last_status = self.status

    def run(self):
        while not rospy.is_shutdown():
            rospy.init_node('android_sensors_driver_to_arduino')
            # Subscribe the node to the /android/Imu topic
            rospy.Subscriber('android/imu', Imu, self.callback)
            rospy.loginfo("Welcome to the android_sensors_driver_to_arduino node!")
            # Wait for incoming messages
            rospy.spin()

if __name__ == '__main__':
    try:
        node = AndroidSensorsDriverToArduino()
        node.run()
    except rospy.ROSInterruptException: pass

