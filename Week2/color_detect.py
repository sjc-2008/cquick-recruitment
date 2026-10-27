# -*- coding: utf-8 -*-
"""
第 2 周 · 任务 1：HSV 颜色分割与目标中心点检测

功能：
  1. 读取图片并检查是否成功；
  2. 转换到 HSV，根据颜色范围生成二值 mask；
  3. 形态学处理（开运算去噪）；
  4. 提取外轮廓，按面积阈值过滤噪声；
  5. 对筛选出的目标计算中心点 (u, v)；
  6. 无目标时输出明确提示，不返回未初始化坐标；
  7. 多目标时按面积排序，选择最大目标。

支持颜色：orange(橙) / red(红) / purple(紫)

用法：
  python color_detect.py <图片路径> <颜色> [--min-area 500]

说明：
  红色在 HSV 色相环上跨越 0 度和 180 度两端，因此使用两段阈值合并。
"""

import sys
import argparse
import cv2
import numpy as np


# HSV 阈值定义（H: 0-179, S: 0-255, V: 0-255）
# 注意 OpenCV 的 H 范围是 [0, 179]
COLOR_RANGES = {
    "orange": {"name": "橙色", "ranges": [((5, 120, 120), (25, 255, 255))]},
    "purple": {"name": "紫色", "ranges": [((130, 80, 80), (165, 255, 255))]},
    # 红色跨越色相环两端，需要两段
    "red": {
        "name": "红色",
        "ranges": [
            ((0, 120, 120), (10, 255, 255)),    # 低段
            ((170, 120, 120), (179, 255, 255)),  # 高段
        ],
    },
}


def build_mask(hsv, color_name):
    """根据颜色名生成二值 mask（支持多段阈值合并）。"""
    cfg = COLOR_RANGES[color_name]
    mask = None
    for lower, upper in cfg["ranges"]:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        m = cv2.inRange(hsv, lower, upper)
        mask = m if mask is None else cv2.bitwise_or(mask, m)
    return mask


def detect(img, color_name, min_area=500, use_morph=True):
    """
    检测指定颜色目标，返回 (detected, u, v, area, result_img)。

    detected: 是否检测到目标
    u, v:     目标中心像素坐标（未检测到时为 0）
    area:     目标轮廓面积（未检测到时为 0）
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1) 生成 mask
    mask = build_mask(hsv, color_name)

    # 2) 形态学处理：开运算去噪（可选）
    if use_morph:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 3) 提取外轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4) 按面积过滤
    valid = [c for c in contours if cv2.contourArea(c) >= min_area]
    if not valid:
        # 未检测到目标：返回明确的失败状态，坐标用 0
        return False, 0, 0, 0.0, mask

    # 5) 多目标时按面积排序，选择最大目标
    valid.sort(key=cv2.contourArea, reverse=True)
    target = valid[0]
    area = cv2.contourArea(target)

    # 6) 计算中心点：使用轮廓矩（处理 m00 为 0 的情况）
    M = cv2.moments(target)
    if M["m00"] != 0:
        u = int(M["m10"] / M["m00"])
        v = int(M["m01"] / M["m00"])
    else:
        # 面积不为 0 但 m00 为 0 的极端情况，回退到外接矩形中心
        x, y, w, h = cv2.boundingRect(target)
        u = x + w // 2
        v = y + h // 2

    return True, u, v, area, mask


def main():
    parser = argparse.ArgumentParser(description="颜色目标检测")
    parser.add_argument("image", help="图片路径")
    parser.add_argument("color", choices=["orange", "red", "purple"], help="目标颜色")
    parser.add_argument("--min-area", type=int, default=500, help="最小轮廓面积")
    parser.add_argument("--no-morph", action="store_true", help="关闭形态学处理")
    args = parser.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        print(f"[错误] 图片读取失败: {args.image}")
        sys.exit(1)

    detected, u, v, area, mask = detect(
        img, args.color, min_area=args.min_area, use_morph=not args.no_morph
    )

    color_name = COLOR_RANGES[args.color]["name"]
    print("=" * 50)
    print(f"图片: {args.image}")
    print(f"目标颜色: {color_name}")
    print(f"最小面积阈值: {args.min_area}")
    print("-" * 50)
    if detected:
        print(f"[检测到目标] 中心点 (u, v) = ({u}, {v})")
        print(f"             面积 area = {area:.1f}")
    else:
        print("[未检测到目标] 本帧未找到符合条件的颜色目标")
        print("               (u, v, area 均视为无效，使用默认值 0)")
    print("=" * 50)


if __name__ == "__main__":
    main()
