import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Time
import numpy as np
import time
import sys
import termios
import tty
import select


class JointStatePublisher(Node):

    def __init__(self):
        """super().__init__('joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(
            0.1, self.publish_joint_states)  """
        super().__init__('joint_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(
            0.1, self.publish_joint_states)  
        
        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0
        self.step = 0.1 # Incremento por pulsación
        self.L1 = 1.0
        self.L2 = 1.0
        self.L3 = 1.0

        self.get_logger().info("""
        Control manual iniciado:
        q1: Q(+) A(-) | q2: W(+) S(-) | q3: E(+) D(-)
        Presiona ESC para salir.
        """)
    
    def get_key(self):
        # Configuración para lectura no bloqueante del teclado
        settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = None
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    
    def publish_joint_states(self):
        """msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()  
        msg.name = [
            'q1', 'q2', 'q3'
        ]

        
        q1=np.sin(time.time())  
        q2=np.cos(time.time())  
        q3=np.sin(2*time.time())     
        msg.position = [q1,q2,q3]

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Published Joint States: {msg.position}')  # Debugging info"""
        # 1. Capturar entrada de teclado
        key = self.get_key()
        
        if key == 'q': self.q1 += self.step
        elif key == 'a': self.q1 -= self.step
        elif key == 'w': self.q2 += self.step
        elif key == 's': self.q2 -= self.step
        elif key == 'e': self.q3 += self.step
        elif key == 'd': self.q3 -= self.step
        elif key == '\x1b': # Tecla ESC para cerrar limpiamente
            self.get_logger().info('Cerrando nodo...')
            raise SystemExit
        s1, c1 = np.sin(self.q1), np.cos(self.q1)
        s2, c2 = np.sin(self.q2), np.cos(self.q2)
        s23 = np.sin(self.q2 + self.q3)
        c23 = np.cos(self.q2 + self.q3)
        x = c1 * (self.L2 * c2 + self.L3 * c23)
        y = s1 * (self.L2 * c2 + self.L3 * c23)
        z = self.L1 + self.L2 * s2 + self.L3 * s23
        # 2. Construir el mensaje
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['q1', 'q2', 'q3']
        msg.position = [self.q1, self.q2, self.q3]

        # 3. Publicar
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published Joint States: {msg.position}')
        self.get_logger().info(
            f'JOINTS: [{self.q1:.2f}, {self.q2:.2f}, {self.q3:.2f}] | '
            f'COORD XYZ: [{x:.3f}, {y:.3f}, {z:.3f}]'
        )


def main(args=None):
    rclpy.init(args=args)
    node = JointStatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()
