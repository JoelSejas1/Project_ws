# Proyecto ROS 2: Sensor y Obstáculo
Este repositorio contiene la implementación de la lógica de comunicación entre dos nodos:

* **pkg1 (sensor):** Nodo que solicita una distancia por teclado.
* **pkg2 (obstaculo):** Nodo que procesa la distancia (distancia - 5) y lanza alertas.

## Instalación
```bash
cd ~/Project_ws
colcon build
source install/setup.bash
```

## Ejecución
**Terminal 1:**
```bash
ros2 run pkg2 obstaculo
```

**Terminal 2:**
```bash
ros2 run pkg1 sensor
```
