import os
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Paths to the default YAML config files
    default_geometric_yaml = os.path.join(
        get_package_share_directory('geometric_controller_ros'),
        'config',
        'geometric_controller.yaml'
    )
    
    default_geometric_mavros_yaml = os.path.join(
        get_package_share_directory('geometric_controller_ros'),
        'config',
        'geometric_mavros.yaml'
    )

    # Declare launch arguments
    yaml_path_arg = DeclareLaunchArgument(
        'geometric_controller_yaml',
        default_value=default_geometric_yaml,
        description='Path to the YAML file with parameters for the geometric_attitude_controller node'
    )

    param_file_arg = DeclareLaunchArgument(
        'geometric_mavros_yaml',
        default_value=default_geometric_mavros_yaml,
        description='Full path to the YAML parameter file to use for geometric_mavros_node'
    )

    # Include mavros.launch.py
    mavros_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ThisLaunchFileDir(), '/mavros.launch.py']),
        launch_arguments={'fcu_url': 'udp://:14540@127.0.0.1:14557'}.items()
    )

    # Include geometric_controller.launch.py
    geometric_controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ThisLaunchFileDir(), '/geometric_controller.launch.py']),
        launch_arguments={'yaml_path': LaunchConfiguration('geometric_controller_yaml')}.items()
    )

    # Include se3controller_to_mavros.launch.py
    geometric_to_mavros_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ThisLaunchFileDir(), '/se3controller_to_mavros.launch.py']),
        launch_arguments={'param_file': LaunchConfiguration('geometric_mavros_yaml')}.items()
    )

    return LaunchDescription([
        yaml_path_arg,
        param_file_arg,
        mavros_launch,
        geometric_controller_launch,
        geometric_to_mavros_launch,
        LogInfo(msg=["Geoemtric controller with MAVROS interface launch files initiated."]),
    ])

