import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class ControlNode(Node):
    def __init__(self):
        super().__init__('detector_obstaculo')
        self.subscription = self.create_subscription(Float32, 'distancia', self.callback, 10)

    def callback(self, msg):
        # Lógica de la pizarra: distancia - 5
        resultado = msg.data - 5.0
        
        if resultado < 5.0:
            self.get_logger().warn(f'¡ALERTA! Resultado: {resultado:.2f} (Distancia < 5 detectada)')
        else:
            self.get_logger().info(f'Procesado: {resultado:.2f} - Todo despejado')

def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    rclpy.shutdown()
