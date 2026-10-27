# -*- coding: utf-8 -*-
"""
第 2 周 · 任务 2：检测结果可视化与参数对比

功能：
  1. 在图像上标注轮廓、中心点、坐标文字；
  2. 保存标注结果到文件；
  3. 参数对比实验：调整 HSV 阈值 / 最小面积 / 是否形态学处理。

用法：
  python visualize.py <图片路径> <颜色>

输出：
  output/ 目录下保存标注图与 mask 图。
"""

import os
import sys
import cv2
import numpy as np

# 将脚本所在目录加入 sys.path，以便导入同目录的 color_detect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 复用 color_detect 的检测逻辑
from color_detect import detect, COLOR_RANGES, build_mask


OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT_DIR, exist_ok=True)


def annotate(img, detected, u, v, area, contours, mask):
    """在原图上标注轮廓、中心点和坐标文字。"""
    result = img.copy()

    if detected:
        # 画轮廓（绿色）
        cv2.drawContours(result, [contours[0]], -1, (0, 255, 0), 2)
        # 画中心点（红色实心圆 + 十字）
        cv2.circle(result, (u, v), 5, (0, 0, 255), -1)
        cv2.drawMarker(result, (u, v), (0, 0, 255), cv2.MARKER_CROSS, 20, 2)
        # 写坐标文字
        text = f"u={u}, v={v}"
        cv2.putText(result, text, (u + 10, v - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(result, f"area={area:.0f}", (u + 10, v + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    else:
        # 未检测到：在图像上明确标注
        cv2.putText(result, "NOT DETECTED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    return result


def run_case(img, color, label, min_area=500, use_morph=True):
    """运行一个检测用例，返回标注图，并打印结果。"""
    detected, u, v, area, mask = detect(img, color, min_area=min_area, use_morph=use_morph)

    # 重新取轮廓用于标注
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = build_mask(hsv, color)
    if use_morph:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid = [c for c in contours if cv2.contourArea(c) >= min_area]
    valid.sort(key=cv2.contourArea, reverse=True)

    annotated = annotate(img, detected, u, v, area, valid, m)

    print(f"[{label}] detected={detected}, u={u}, v={v}, area={area:.1f}, "
          f"min_area={min_area}, morph={use_morph}")
    return annotated, m


def main():
    if len(sys.argv) < 3:
        print("用法: python visualize.py <图片路径> <颜色>")
        sys.exit(1)

    image_path = sys.argv[1]
    color = sys.argv[2]
    img = cv2.imread(image_path)
    if img is None:
        print(f"[错误] 图片读取失败: {image_path}")
        sys.exit(1)

    base = os.path.splitext(os.path.basename(image_path))[0]

    print("=" * 60)
    print("参数对比实验")
    print("=" * 60)

    # 用例 1：默认参数（基准）
    ann1, mask1 = run_case(img, color, "基准(默认参数)", min_area=500, use_morph=True)
    cv2.imwrite(os.path.join(OUT_DIR, f"{base}_baseline.png"), ann1)
    cv2.imwrite(os.path.join(OUT_DIR, f"{base}_mask_baseline.png"), mask1)

    # 用例 2：提高最小面积阈值（过滤更多噪声）
    ann2, mask2 = run_case(img, color, "提高最小面积", min_area=5000, use_morph=True)
    cv2.imwrite(os.path.join(OUT_DIR, f"{base}_minarea5000.png"), ann2)

    # 用例 3：关闭形态学处理
    ann3, mask3 = run_case(img, color, "关闭形态学", min_area=500, use_morph=False)
    cv2.imwrite(os.path.join(OUT_DIR, f"{base}_nomorph.png"), ann3)

    print("=" * 60)
    print(f"标注结果已保存到: {OUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
