Aquí tienes una guía paso a paso para crear un workspace de ROS 2 y un paquete de Python en ROS 2:

### 1. **Instalar ROS 2 (si no lo tienes ya)**
   Sigue las instrucciones de la [documentación oficial](https://docs.ros.org/en/rolling/Installation.html) para instalar ROS 2 en tu sistema. Por ejemplo, para Ubuntu:

   ```bash
   sudo apt update
   sudo apt install ros-humble-desktop
   ```

   Luego, asegúrate de tener las herramientas necesarias:

   ```bash
   sudo apt install python3-colcon-common-extensions python3-rosdep
   ```

   Fuente ROS 2 en tu terminal:

   ```bash
   source /opt/ros/humble/setup.bash
   ```

### 2. **Crear un Workspace de ROS 2**

   Un workspace es un entorno de desarrollo donde puedes crear y compilar tus paquetes ROS. Sigue estos pasos:

   #### Paso 1: Crear directorios del workspace

   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/
   ```

   #### Paso 2: Inicializar `rosdep`

   `rosdep` es una herramienta que ayuda a instalar dependencias necesarias para ROS 2. Solo necesitas hacerlo una vez:

   ```bash
   sudo rosdep init
   rosdep update
   ```

### 3. **Crear un Paquete de Python en ROS 2**

   Ahora, vamos a crear un paquete de Python dentro del workspace que acabas de crear.

   #### Paso 1: Navegar al directorio `src` del workspace

   ```bash
   cd ~/ros2_ws/src
   ```

   #### Paso 2: Crear el paquete de Python

   Usa el comando `ros2 pkg create` para crear un paquete:

   ```bash
   ros2 pkg create --build-type ament_python my_python_package
   ```

   Esto creará la estructura básica de tu paquete.

### 4. **Modificar los archivos del paquete**

   #### Paso 1: Editar el archivo `setup.py`

   Abre el archivo `setup.py` en tu editor y ajusta el contenido:

   ```python
   from setuptools import setup

   package_name = 'my_python_package'

   setup(
       name=package_name,
       version='0.0.0',
       packages=[package_name],
       install_requires=['setuptools'],
       zip_safe=True,
       maintainer='Tu Nombre',
       maintainer_email='tu_email@example.com',
       description='Ejemplo de paquete Python para ROS 2',
       license='Apache License 2.0',
       entry_points={
           'console_scripts': [
               'my_node = my_python_package.my_node:main',
           ],
       },
   )
   ```

   #### Paso 2: Crear un nodo en Python

   Crea el archivo `my_node.py` dentro de la carpeta `my_python_package/`:

   ```bash
   mkdir my_python_package
   touch my_python_package/my_node.py
   ```

   Luego, abre el archivo `my_node.py` y añade el siguiente código:

   ```python
   import rclpy
   from rclpy.node import Node
   from std_msgs.msg import String

   class MyNode(Node):

       def __init__(self):
           super().__init__('my_node')
           self.publisher_ = self.create_publisher(String, 'topic', 10)
           timer_period = 2.0  # segundos
           self.timer = self.create_timer(timer_period, self.timer_callback)

       def timer_callback(self):
           msg = String()
           msg.data = 'Hola desde ROS 2'
           self.publisher_.publish(msg)
           self.get_logger().info('Publicando: "%s"' % msg.data)

   def main(args=None):
       rclpy.init(args=args)
       node = MyNode()
       rclpy.spin(node)
       node.destroy_node()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()
   ```

   #### Paso 3: Editar `CMakeLists.txt`

   Aunque es un paquete de Python, el archivo `CMakeLists.txt` es necesario para `ament`. Añade estas líneas:

   ```cmake
   cmake_minimum_required(VERSION 3.5)
   project(my_python_package)

   find_package(ament_cmake REQUIRED)
   find_package(rclpy REQUIRED)

   install(DIRECTORY my_python_package
     DESTINATION lib/${PROJECT_NAME}
   )

   ament_package()
   ```

   #### Paso 4: Editar `package.xml`

   Define las dependencias necesarias en el archivo `package.xml`:

   ```xml
   <package format="2">
     <name>my_python_package</name>
     <version>0.0.0</version>
     <description>Mi primer paquete Python en ROS 2</description>

     <maintainer email="tu_email@example.com">Tu Nombre</maintainer>

     <license>Apache 2.0</license>

     <buildtool_depend>ament_cmake</buildtool_depend>
     <exec_depend>rclpy</exec_depend>
   </package>
   ```

### 5. **Compilar el Paquete**

   #### Paso 1: Compilar el paquete

   Vuelve a la raíz del workspace y usa `colcon` para compilar el paquete:

   ```bash
   cd ~/ros2_ws
   colcon build --packages-select my_python_package
   ```

   #### Paso 2: Sourcing del workspace

   Después de la compilación, debes "sourcer" tu workspace para usar los nodos:

   ```bash
   source install/setup.bash
   ```

### 6. **Ejecutar el Nodo**

   Finalmente, puedes ejecutar el nodo de Python:

   ```bash
   ros2 run my_python_package my_node
   ```

   Verás en la terminal algo como:

   ```bash
   [INFO] [my_node]: Publicando: "Hola desde ROS 2"
   ```

### 7. **(Opcional) Verificar con `ros2 topic`**

   Puedes verificar los mensajes publicados con el siguiente comando:

   ```bash
   ros2 topic echo /topic
   ```

¡Con esto, has creado y ejecutado un paquete de Python en ROS 2 desde cero!