import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class RobotMonitor(Node):
    def __init__(self):
        super().__init__('robot_monitor')
        
        # Atributos de clase (reemplazan las globales)
        self.ultima_vel = 0.0
        self.ultima_batt = 100.0

        # Suscripciones
        self.create_subscription(Float32, '/robot_velocity', self.callback_velocidad, 10)
        self.create_subscription(Float32, '/robot_battery', self.callback_bateria, 10)

        # Timer para el diagnóstico
        self.create_timer(0.5, self.revisar_y_mostrar)
        self.get_logger().info("--- Monitor de Estado Iniciado ---")

    def callback_velocidad(self, msg):
        self.ultima_vel = msg.data

    def callback_bateria(self, msg):
        self.ultima_batt = msg.data

    def revisar_y_mostrar(self):
        # Lógica de estados mejorada
        alertas = []
        
        if self.ultima_vel > 2.0:
            alertas.append("ALERTA VELOCIDAD")
        
        if self.ultima_batt < 10:
            alertas.append("CRITICAL BATTERY")
        elif self.ultima_batt < 20:
            alertas.append("ALERTA BATERIA BAJA")
            
        estado = " | ".join(alertas) if alertas else "OK"
        
        # Usamos el logger del nodo en lugar de print para mejores prácticas
        self.get_logger().info(
            f"Velocidad: {self.ultima_vel:.2f} m/s | "
            f"Batería: {self.ultima_batt:.1f}% | "
            f"ESTADO: {estado}"
        )

def main(args=None):
    rclpy.init(args=args)
    nodo = RobotMonitor()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()