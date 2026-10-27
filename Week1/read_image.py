# -*- coding: utf-8 -*-
"""
第 1 周 · 任务 2：读取图片并分析图像信息

功能：
  1. 使用 cv2.imread 读取图片，并判断是否读取成功；
  2. 输出图像宽、高、数组形状 shape、数据类型 dtype；
  3. 打印一个合法像素位置的通道值，说明 BGR 通道顺序；
  4. 尝试显示图片（无图形界面时保存并说明）。

用法：
  python read_image.py <图片路径>
"""

import os
import sys
import cv2
import numpy as np


def main():
    # 1) 读取命令行参数：图片路径
    if len(sys.argv) < 2:
        print("用法: python read_image.py <图片路径>")
        sys.exit(1)

    image_path = sys.argv[1]

    # 2) 读取图片（OpenCV 默认以 BGR 顺序读取彩色图）
    img = cv2.imread(image_path)

    # 3) 判断是否读取成功，失败时给出明确提示，避免后续崩溃
    if img is None:
        print(f"[错误] 图片读取失败，请检查路径或文件格式: {image_path}")
        sys.exit(1)

    print("=" * 50)
    print("图片读取成功:", image_path)
    print("=" * 50)

    # 4) 图像尺寸：宽、高
    #    shape 为 (高, 宽) 或 (高, 宽, 通道数)
    height = img.shape[0]   # 行数 = 高
    width = img.shape[1]    # 列数 = 宽
    print(f"图像宽 (width)  : {width} 像素")
    print(f"图像高 (height) : {height} 像素")

    # 5) 数组形状 shape
    print(f"数组形状 shape  : {img.shape}")

    # 6) 数据类型 dtype
    print(f"数据类型 dtype  : {img.dtype}")

    # 7) 打印一个合法像素位置的通道值（取图像中心点）
    u = width // 2
    v = height // 2
    pixel = img[v, u]  # 注意：OpenCV 用 [行, 列] 即 [y, x] 索引
    print(f"像素 ({u}, {v}) 的通道值: {pixel}")

    # 8) 说明 BGR 通道顺序
    print("-" * 50)
    print("通道顺序说明:")
    print("  OpenCV 默认以 BGR 顺序存储彩色图，即:")
    print(f"    B (蓝) = {pixel[0]}, G (绿) = {pixel[1]}, R (红) = {pixel[2]}")
    print("  这与常见的 RGB 顺序相反，显示时需注意转换。")
    print("=" * 50)

    # 9) 显示图片；无图形界面时保存并说明
    #    通过环境变量或参数控制是否显示，避免在无界面环境卡住
    headless = os.environ.get("HEADLESS", "") == "1"
    if headless:
        out_path = "01_original.png"
        cv2.imwrite(out_path, img)
        print(f"[提示] 无图形界面模式，已保存图片到: {out_path}")
    else:
        try:
            cv2.imshow("Image", img)
            print("已打开显示窗口，按任意键退出...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except cv2.error:
            out_path = "01_original.png"
            cv2.imwrite(out_path, img)
            print(f"[提示] 当前环境无图形界面，已保存图片到: {out_path}")


if __name__ == "__main__":
    main()
