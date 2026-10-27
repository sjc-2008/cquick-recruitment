# -*- coding: utf-8 -*-
"""
第 1 周 · 任务 3：基础图像处理小实验

功能：
  1. 灰度化：彩色图 -> 灰度图；
  2. HSV 转换：BGR -> HSV，并可视化；
  3. 阈值分割：生成二值图，并比较两组不同阈值/颜色范围的结果。

输出文件（保存在与脚本同级的 output/ 目录）：
  01_original.png     原图
  02_gray.png         灰度图
  03_hsv.png          HSV 可视化
  04_threshold_a.png  阈值方案 A
  05_threshold_b.png  阈值方案 B

用法：
  python image_process.py <图片路径>
"""

import os
import sys
import cv2
import numpy as np


def main():
    # 1) 读取图片路径
    if len(sys.argv) < 2:
        print("用法: python image_process.py <图片路径>")
        sys.exit(1)

    image_path = sys.argv[1]
    img = cv2.imread(image_path)
    if img is None:
        print(f"[错误] 图片读取失败: {image_path}")
        sys.exit(1)

    # 输出目录
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)

    def save(name, data):
        path = os.path.join(out_dir, name)
        cv2.imwrite(path, data)
        print(f"已保存: {path}")

    # 2) 原图
    save("01_original.png", img)

    # 3) 灰度化：彩色(BGR 3通道) -> 灰度(单通道)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save("02_gray.png", gray)
    print(f"灰度图 shape: {gray.shape}  (通道数从 3 变为 1)")

    # 4) HSV 转换
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # HSV 是 H(色调)/S(饱和度)/V(明度) 三通道，直接保存会显示成伪彩色，
    # 这里保存 HSV 原数据用于查看
    save("03_hsv.png", hsv)

    # 5) 阈值分割：两组方案对比
    #    方案 A：灰度图固定阈值二值化（阈值 127）
    _, thresh_a = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    save("04_threshold_a.png", thresh_a)

    #    方案 B：灰度图 Otsu 自动阈值
    _, thresh_b = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    save("05_threshold_b.png", thresh_b)

    # 6) 打印对比信息
    print("-" * 50)
    print("阈值方案对比:")
    print(f"  方案 A: 固定阈值 127  -> 非零像素数 {np.count_nonzero(thresh_a)}")
    print(f"  方案 B: Otsu 自动阈值 -> 非零像素数 {np.count_nonzero(thresh_b)}")
    print("  说明: 阈值不同会改变前景/背景的划分，从而影响分割结果。")
    print("=" * 50)


if __name__ == "__main__":
    main()
