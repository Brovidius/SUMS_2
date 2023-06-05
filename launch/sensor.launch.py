# import launch # Not needed?
from launch import LaunchDescription
from launch_ros.actions import Node
import random

sample_time = 10.0              # Sample time in seconds (float)
n_sensors = 5                   # How many sensors that are in use (int)
transfer_delay = 6.0            # How long transferring data takes in seconds(float)
modem_IP = '192.168.42.86'      # IP for the modem (string)
modem_port = 1100               # Port for the modem (int) [only change if using simulator]
precision = 2                   # Variable for specifying the precision of the transmitted data (int)

# Header for identifying logged data
log_header = 'Time,Pressure,Voltage,Current,Oxygen,Salinity,Temperature'

# Random generator to avoid deadlocks
ms = 1000
step = 200
lower_bounds = [2 * ms, 4 * ms]
upper_bounds = [4 * ms, 6 * ms]

# Generating random bounds for each runtime based on the bounds above
random_bounds = [
    random.randrange(lower_bounds[0], upper_bounds[0], step),
    random.randrange(lower_bounds[1], upper_bounds[1], step)
]


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sensor_oxygen',
            namespace='sensors',
            executable='oxygen_publisher',
            name='oxygen',
            parameters=[{'sample_time': sample_time}]
        ),
        Node(
            package='sensor_thermometer',
            namespace='sensors',
            executable='thermometer_publisher',
            name='thermometer',
            parameters=[{'sample_time': sample_time}]
        ),
        Node(
            package='sensor_barometer',
            namespace='sensors',
            executable='barometer_publisher',
            name='barometer',
            parameters=[{'sample_time': sample_time}]
        ),
        Node(
            package='sensor_salinity',
            namespace='sensors',
            executable='salinity_publisher',
            name='salinity',
            parameters=[{'sample_time': sample_time}]
        ),
        Node(
            package='sensor_battery',
            namespace='sensors',
            executable='battery_publisher',
            name='battery',
            parameters=[{'sample_time': sample_time}]
        ),
        Node(
            package='logger',
            namespace='logger',
            executable='internal_logger',
            name='internal',
            parameters=[{'log_header': log_header}]
        ),
        Node(
            package='logger',
            namespace='logger',
            executable='external_logger',
            name='external',
            parameters=[{'log_header': log_header}]
        ),
        Node(
            package='modem_communication',
            namespace='modem',
            executable='modem_data_handler',
            name='data_handler',
            parameters=[
                        {'sensor_count': n_sensors},
                        {'transfer_precision': precision}
            ]
        ),
        # Node(
        #     package='modem_communication',
        #     namespace='modem',
        #     executable='modem_data_communicator',
        #     name='subnero_communicator',
        #     parameters=[
        #                 {'sample_time': sample_time},
        #                 {'transfer_delay': transfer_delay},
        #                 {'modem_IP': modem_IP},
        #                 {'modem_port': modem_port},
        #                 {'lower_bound': random_bounds[0]},
        #                 {'upper_bound': random_bounds[1]}
        #     ]
        # ),
    ])