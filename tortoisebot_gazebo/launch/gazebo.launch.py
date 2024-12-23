import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
from launch_ros.actions import Node
import os

def launch_setup(context, *args, **kwargs):
    pkg_share = launch_ros.substitutions.FindPackageShare(package='tortoisebot_gazebo').find('tortoisebot_gazebo')
    world_path=os.path.join(pkg_share, 'worlds/room2.sdf')
    use_sim_time = LaunchConfiguration('use_sim_time')
    headless = LaunchConfiguration('headless')

    headless_value = headless.perform(context)
    if headless_value == 'true' or headless_value == 'True' :
        gazebo_cmd = ['gzserver', '--verbose', '-s',
                      'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path]
    else:
        gazebo_cmd = ['gazebo', '--verbose', '-s',
                      'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path]


    return [
        launch.actions.ExecuteProcess(
            cmd=gazebo_cmd,
            output='screen'
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'tortoisebot', '-topic', 'robot_description'],
            parameters= [{'use_sim_time': use_sim_time}],
            output='screen'
        )
    ]

def generate_launch_description():
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='False',
                                description='Flag to enable use_sim_time'),
        launch.actions.DeclareLaunchArgument(
            name='headless', default_value='false', description='Enable headless mode for Gazebo'
        ),
        launch.actions.OpaqueFunction(function=launch_setup)
    ])

