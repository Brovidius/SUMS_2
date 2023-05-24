from rclpy.node import Node
from sensor_interfaces.msg import Modem
from unetpy import UnetSocket
import time
import random

# Need More Testing

class ModemCommunicator(Node):
    # Class variable
    start_time = 0.0

    def __init__(self):
        super().__init__('ModemCommunicator')

        self.external_modem_publisher_ = self.create_publisher(Modem, 'external_data', 10)  # Creates a publisher over the topic external_modem_data

        # Get parameters
        self.sample_time  = self.declare_parameter('sample_time', 2.0).value  # Gets sample time as a parameter, default = 2
        self.transfer_delay  = self.declare_parameter('transfer_delay', 6.0).value  # How many seconds a transmition usually takes
        self.MODEM_IP  = self.declare_parameter('modem_IP', '0.0.0.0').value  # IP for the modem
        self.MODEM_PORT  = self.declare_parameter('modem_port', 1100).value  # API port for the modem

        self.LOWER_BOUND  = self.declare_parameter('lower_bound', 3000).value  # API port for the modem
        self.UPPER_BOUND  = self.declare_parameter('upper_bound', 9000).value  # API port for the modem

        # Open a scoket to the modem 
        self.sock  = UnetSocket(self.MODEM_IP, self.MODEM_PORT)

        self.get_logger().info('Bounds for this runtime:\nLower Bound: %i \nUpper Bound: %i' % (self.LOWER_BOUND, self.UPPER_BOUND))

        self.internal_data_subscription = self.create_subscription(
            Modem, 
            '/modem/internal_data', 
            self.modem_callback, 
            10)

    def modem_callback(self, msg:Modem):
        self.start_time = time.time()
        self.sock.cancel()
        data = msg.internal_data
        
        try:
            self.sock.send(data, 0) # Sending to everyone that wants to listen
            self.get_logger().info('Data Sent to Modem')
        except:
            self.get_logger().error('COULD NOT SEND DATA TO MODEM')

        full_time = self.start_time + self.transfer_delay
        while (time.time() - full_time) < self.sample_time:
            self.sock.setTimeout(random.randrange(self.LOWER_BOUND, self.UPPER_BOUND, 300))
            rx = self.sock.receive()
            if rx is not None:
                external_data = str(rx.from_) + ',' + bytearray(rx.data).decode()

                external_msg = Modem()
                external_msg.external_data = external_data
                self.get_logger().info('Recieved data:\n%s' % external_data)
                self.external_modem_publisher_.publish(external_msg)