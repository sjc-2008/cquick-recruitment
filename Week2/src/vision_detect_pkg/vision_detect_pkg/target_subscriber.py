#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 2 周 · 任务 3 · 订阅节点

功能：订阅 /target_position 话题，打印 detected / u / v / area。

用法：
  ros2 run vision_detect_pkg target_subscriber
"""

import rclpy
from rclpy.node import Node
from target_position_interfaces.msg import TargetPosition


class TargetSubscriber(Node):
    def __init__(self):
        super().__init__("target_subscriber")
        self.subscription = self.create_subscription(
            TargetPosition, "/target_position", self.callback, 10
        )
        self.count = 0

    def callback(self, msg):
        self.count += 1
        self.get_logger().info(
            f"收到 #{self.count}: detected={msg.detected}, "
            f"u={msg.u}, v={msg.v}, area={msg.area}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = TargetSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
