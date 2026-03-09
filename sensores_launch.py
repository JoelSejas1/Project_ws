from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='py_interfaces_test',
            executable='sensor_primitivo',
            name='simulador_sensores',
            output='screen',
            emulate_tty=True 
        )
    ])