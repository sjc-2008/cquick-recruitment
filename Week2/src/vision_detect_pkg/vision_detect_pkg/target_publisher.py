#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 2 周 · 任务 3 · 发布节点

功能：把视觉检测结果（detected/u/v/area）发布到 /target_position 话题。

数据来源：
  优先接入 color_detect 的真实检测结果；若未提供测试图片，
  则回退到固定测试坐标（仅用于验证通信），最终验收必须用真实检测结果。

用法：
  ros2 run vision_detect_pkg target_publisher --ros-args -p image_path:=<图片路径> -p color:=red
"""

import os
import sys

import rclpy
from rclpy.node import Node
from target_position_interfaces.msg import TargetPosition

# 将 color_detect 所在目录加入 sys.path（部署时需把 color_detect.py 放到包内）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cv2
from color_detect import detect


class TargetPublisher(Node):
    def __init__(self):
        super().__init__("target_publisher")
        self.publisher_ = self.create_publisher(TargetPosition, "/target_position", 10)

        # 参数
        self.declare_parameter("image_path", "")
        self.declare_parameter("color", "red")
        self.declare_parameter("min_area", 500)
        self.declare_parameter("rate", 1.0)  # 发布频率 Hz

        self.image_path = self.get_parameter("image_path").value
        self.color = self.get_parameter("color").value
        self.min_area = self.get_parameter("min_area").value
        self.rate = self.get_parameter("rate").value

        # 尝试读取图片
        self.img = None
        if self.image_path and os.path.exists(self.image_path):
            self.img = cv2.imread(self.image_path)
            if self.img is None:
                self.get_logger().warn(f"图片读取失败: {self.image_path}")
        else:
            self.get_logger().warn("未提供有效图片，将使用固定测试坐标（仅用于验证通信）")

        self.timer = self.create_timer(1.0 / self.rate, self.publish_callback)
        self.count = 0

    def publish_callback(self):
        msg = TargetPosition()

        if self.img is not None:
            # 真实检测结果
            detected, u, v, area, _ = detect(
                self.img, self.color, min_area=self.min_area, use_morph=True
            )
            msg.detected = detected
            msg.u = float(u)
            msg.v = float(v)
            msg.area = float(area)
        else:
            # 固定测试坐标（仅验证通信）
            msg.detected = True
            msg.u = 320.0
            msg.v = 240.0
            msg.area = 1000.0

        self.publisher_.publish(msg)
        self.count += 1
        self.get_logger().info(
            f"发布 #{self.count}: detected={msg.detected}, "
            f"u={msg.u}, v={msg.v}, area={msg.area}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = TargetPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
