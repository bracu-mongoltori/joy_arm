import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from mt_arm_interfaces.msg import ArmJoints



class JoyInputReader(Node):
    def __init__(self):
        super().__init__('joy_input_reader')
        self.subscription = self.create_subscription(Joy,'/joy',self.joy_callback,10)
        self.pub_topic = '/sixdof'
        self.publisher = self.create_publisher(ArmJoints, self.pub_topic, 10)
        
        self.arm_msg = ArmJoints()
        self.arm_msg.d1 = 0.0
        self.arm_msg.d2 = 0.0
        
        self.default_scale = 50
        self.d1_d2_scale = 100
        self.trigger = False

    def joy_callback(self, msg): # for Xinput mode
        if len(msg.axes) == 6:
            print("Please switch to Xinput Mode. Look at the back of the controller.")
        else:
            for button, value in enumerate(msg.buttons):
                if value == 1:
                    if button == 0:  
                        self.get_logger().info(f"Button A pressed")
                    elif button == 1:  
                        self.get_logger().info(f"Button B pressed")
                    elif button == 2:  
                        self.get_logger().info(f"Button X pressed")
                    elif button == 3:  
                        self.get_logger().info(f"Button Y pressed")
                    elif button == 4:  
                        self.get_logger().info(f"Button LB pressed")
                    elif button == 5:  
                        self.get_logger().info(f"Button RB pressed")
                    elif button == 6:  
                        self.get_logger().info(f"Button BACK pressed")
                    elif button == 7:  
                        self.get_logger().info(f"Button START pressed")

            for axis, value in enumerate(msg.axes):
                if abs(value) >= 0.1 and axis == 0:
                    self.get_logger().info(f"Axis Left (Horizontal) value: {value}")
                elif abs(value) >= 0.1 and axis == 1:
                    self.get_logger().info(f"Axis Left (Vertical) value: {value}")
                elif abs(value) >= 0.1 and axis == 3:
                    self.get_logger().info(f"Axis Right (Horizontal) value: {value}")
                elif abs(value) >= 0.1 and axis == 4:
                    self.get_logger().info(f"Axis Right (Vertical) value: {value}")
                elif axis == 2 and value < 0.9: 
                    self.get_logger().info(f"Axis Left Trigger value: {value}")
                elif axis == 5  and value < 0.9: # Left Trigger and Right Trigger
                    self.get_logger().info(f"Axis Right Trigger value: {value}")
                    
            self.arm_control(msg)

            # self.twist.linear.x = msg.axes[1] * self.linear_scale
            # self.twist.angular.z = msg.axes[3] * self.angular_scale
            # self.get_logger().info(f"prev linear {self.prev_twist.linear.x} prev angular {self.prev_twist.angular.z} current linear {self.twist.linear.x} current angular {self.twist.angular.z}")
            # if self.prev_twist.linear.x != self.twist.linear.x or self.prev_twist.angular.z != self.twist.angular.z:
            #     self.publisher.publish(self.twist)
            #     self.get_logger().info(f"Published {self.twist.linear.x} and {self.twist.angular.z} to {self.pub_topic} :")
            #     self.prev_twist.linear.x = self.twist.linear.x
            #     self.prev_twist.angular.z = self.twist.angular.z
                
    def arm_control(self, msg):
        count = 10
        if abs(msg.axes[3]) != 0.0:
            # rotation for base
            self.arm_msg.base = msg.axes[3] * self.default_scale
        if abs(msg.axes[0]) != 0.0:
            # rotation for shoulder
            self.arm_msg.link1 = msg.axes[0] * self.default_scale
        elif abs(msg.axes[1]) != 0.0:
            # rotation for elbow
            self.arm_msg.link2 = msg.axes[1] * self.default_scale
            
        if abs(msg.axes[7]) == 0.0:
            self.trigger = True
        
        if abs(msg.axes[7]) != 0.0 and self.trigger:
            self.arm_msg.d1 += msg.axes[7] * 10
            self.arm_msg.d2 += msg.axes[7] * 10
            self.trigger = False
            
        if abs(msg.axes[4]) != 1.0:
            self.get_logger().info(f"claw closing")
            
            
        self.publisher.publish(self.arm_msg)
            
        
        

def main(args=None):
    rclpy.init(args=args)
    joy_input_reader = JoyInputReader()
    rclpy.spin(joy_input_reader)
    joy_input_reader.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()