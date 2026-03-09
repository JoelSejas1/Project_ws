import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class RobotSensorPublisher(Node):
    def __init__(self):
        super().__init__('robot_sensor_publisher')
        self.pub_vel = self.create_publisher(Float32, '/robot_velocity', 10)
        self.pub_batt = self.create_publisher(Float32, '/robot_battery', 10)
        
        # Timer cada 0.5 segundos (frecuencia de 2Hz)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg_v = Float32()
        msg_b = Float32()
        
        msg_v.data = random.uniform(0.0, 2.5)
        msg_b.data = random.uniform(0.0, 100.0)
        
        self.pub_vel.publish(msg_v)
        self.pub_batt.publish(msg_b)
        
        self.get_logger().info(f'Publicando - Vel: {msg_v.data:.2f} | Bat: {msg_b.data:.1f}%')

def main(args=None):
    rclpy.init(args=args)
    node = RobotSensorPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()