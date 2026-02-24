import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

def main(args=None):
    rclpy.init(args=args)
    node = Node('sensor_manual')
    publisher = node.create_publisher(Float32, 'distancia', 10)

    try:
        while rclpy.ok():
            # Pedir datos por teclado
            entrada = input("Ingresa la distancia medida (o 'q' para salir): ")
            
            if entrada.lower() == 'q':
                break
                
            msg = Float32()
            msg.data = float(entrada)
            publisher.publish(msg)
            node.get_logger().info(f'Enviando: {msg.data}')
            
    except ValueError:
        print("Error: Por favor ingresa solo números.")
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
