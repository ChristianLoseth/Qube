from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro
import os

def generate_launch_description():
    qube_bringup_dir = get_package_share_directory('qube_bringup')
    qube_driver_dir = get_package_share_directory('qube_driver')    

    # Sti til xacro-filen i qube_bringup
    xacro_file = os.path.join(qube_bringup_dir, 'urdf', 'controlled_qube.urdf.xacro')
    description = xacro.process_file(xacro_file).toxml()
    
    # Sti til en launchfil i qube_driver
    qube_driver_launch = os.path.join(qube_driver_dir, 'launch', 'qube_driver.launch.py')

    return LaunchDescription([
        # Inkluder driver-launch (starter ros2_control_node, hardware-driver etc.)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(qube_driver_launch)
        ),

        # Start robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': description}]
        ),

        # Start RViz (valgfritt)
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
        )
    ])

