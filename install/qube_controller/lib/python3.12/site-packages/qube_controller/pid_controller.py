import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

class QubePIDController(Node):
    def __init__(self):
        super().__init__('qube_pid_controller')

        self.kp = 2.0
        self.ki = 0.0001
        self.kd = 0.01

        self.target_position = 0.0

        self.integral = 0.0
        self.prev_error = 0.0

        self.prev_time = self.get_clock().now()

        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.velocity_pub = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10
        )

    def joint_state_callback(self, msg):
        current_pos = msg.position[0]

        now = self.get_clock().now()
        dt = (now - self.prev_time).nanoseconds / 1e9
        self.prev_time = now
        if dt <= 0.0:
            return

        error = self.target_position - current_pos

        p_term = self.kp * error

        self.integral += error * dt
        i_term = self.ki * self.integral

        d_term = 0.0
        if dt > 0:
            d_error = (error - self.prev_error) / dt
            d_term = self.kd * d_error

        self.prev_error = error

        cmd_velocity = p_term + i_term + d_term

        cmd_msg = Float64MultiArray()
        cmd_msg.data = [float(cmd_velocity)]
        self.velocity_pub.publish(cmd_msg)


def main(args=None):
    rclpy.init(args=args)
    node = QubePIDController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
