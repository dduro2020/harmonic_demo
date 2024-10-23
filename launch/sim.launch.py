import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    AppendEnvironmentVariable
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    roll = LaunchConfiguration('R')
    pitch = LaunchConfiguration('P')
    yaw = LaunchConfiguration('Y')

    package_dir = get_package_share_directory('harmonic_demo')

    gz_model_path = os.path.join(package_dir,
        'models'
    )
    package_dir2 = get_package_share_directory('aws_robomaker_small_house_world')

    robot_launch_dir = os.path.join(get_package_share_directory('harmonic_demo'), 'launch')
    robot_model_dir = os.path.join(get_package_share_directory('harmonic_demo'), 'models')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='1.0')
    y_pose = LaunchConfiguration('y_pose', default='-1.5')
    z_pose = LaunchConfiguration('z_pose', default='7.1')

    model_folder = 'turtlebot3_waffle'
    urdf_path = os.path.join(
        get_package_share_directory('harmonic_demo'),
        'models',
        model_folder,
        'model.sdf'
    )
    
    world = os.path.join(get_package_share_directory('harmonic_demo'), 'maps', 'harmonic.world')
    # world = os.path.join(
    #     get_package_share_directory('aws_robomaker_small_house_world'),
    #     'worlds',
    #     'small_house.world'
    # )

    gazebo_client = IncludeLaunchDescription(
	PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-g -v4 '}.items()
     )
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r -s -v4 ', world], 'on_exit_shutdown': 'true'}.items()
    )

    declare_x_cmd = DeclareLaunchArgument(
        'x', default_value='1.0'
    )

    declare_y_cmd = DeclareLaunchArgument(
        'y', default_value='-1.5'
    )

    declare_z_cmd = DeclareLaunchArgument(
        'z', default_value='7.1'
    )

    declare_roll_cmd = DeclareLaunchArgument(
        'R', default_value='0.0'
    )

    declare_pitch_cmd = DeclareLaunchArgument(
        'P', default_value='0.0'
    )

    declare_yaw_cmd = DeclareLaunchArgument(
        'Y', default_value='1.57079'
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_launch_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_robot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_launch_dir, 'spawn_robot.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose,
            'z_pose': z_pose
        }.items()
    )

    world_entity_cmd = Node(package='ros_gz_sim', executable='create',
                            arguments=['-name',
                                       'world',
                                       '-file',
                                       world
                                       ],
                            output='screen')

    ld = LaunchDescription()

    ld.add_action(SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', gz_model_path))
    set_env_vars_resources = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.join(package_dir,'models'))
    ld.add_action(set_env_vars_resources)
    ld.add_action(gazebo_server)
    ld.add_action(gazebo_client)
    ld.add_action(declare_x_cmd)
    ld.add_action(declare_y_cmd)
    ld.add_action(declare_z_cmd)
    ld.add_action(declare_roll_cmd)
    ld.add_action(declare_pitch_cmd)
    ld.add_action(declare_yaw_cmd)
    ld.add_action(world_entity_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_robot_cmd)

    return ld
