# -*- coding: utf-8 -*-
"""
生成第 2 周颜色目标检测的测试图片。

生成三种颜色（橙 / 红 / 紫）的圆形目标，每种至少一张，
并额外生成"目标较小"与"背景含相近颜色"两种干扰场景，
用于任务 1 的多图测试与任务 2 的参数对比。

输出目录：与脚本同级的 images/ 文件夹。
"""

import os
import cv2
import numpy as np

# 输出目录（与脚本同级）
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT_DIR, exist_ok=True)

# 颜色定义（BGR 顺序）
COLORS = {
    "orange": (0, 128, 255),   # 橙色
    "red":    (0, 0, 255),     # 红色
    "purple": (255, 0, 128),   # 紫色
}

W, H = 640, 480


def make_bg(seed=0):
    """生成一张纯色偏暗背景，便于目标突出。"""
    rng = np.random.default_rng(seed)
    # 背景使用偏灰/偏蓝的暗色，避免与目标颜色相近
    bg_color = (rng.integers(40, 90), rng.integers(40, 90), rng.integers(50, 100))
    img = np.full((H, W, 3), bg_color, dtype=np.uint8)
    return img


def draw_circle(img, color, center, radius):
    """绘制实心圆形目标。"""
    cv2.circle(img, center, radius, color, -1, lineType=cv2.LINE_AA)


def add_noise(img, seed=1):
    """添加少量噪点，模拟真实拍摄。"""
    rng = np.random.default_rng(seed)
    noise = rng.integers(0, 30, img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return img


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    cv2.imwrite(path, img)
    print("已生成:", path)


def main():
    # 1) 目标清晰：三种颜色，各一张
    for color_name, color in COLORS.items():
        img = make_bg(seed=hash(color_name) % 1000)
        draw_circle(img, color, (W // 2, H // 2), 90)
        img = add_noise(img, seed=10)
        save(img, f"01_{color_name}_clear.png")

    # 2) 目标较小：橙色小圆
    img = make_bg(seed=200)
    draw_circle(img, COLORS["orange"], (W // 2, H // 2), 25)
    img = add_noise(img, seed=11)
    save(img, "02_orange_small.png")

    # 3) 背景含相近颜色干扰：紫色目标 + 背景混入相近紫色块
    img = make_bg(seed=300)
    # 背景里放几个偏紫的干扰块
    draw_circle(img, (220, 40, 150), (120, 100), 40)   # 相近紫色干扰块
    draw_circle(img, (230, 60, 160), (500, 350), 45)   # 相近紫色干扰块
    # 真正的目标（更纯的紫色）
    draw_circle(img, COLORS["purple"], (W // 2, H // 2), 70)
    img = add_noise(img, seed=12)
    save(img, "03_purple_similar_bg.png")

    # 4) 红色干扰场景：红色目标 + 背景橙色干扰（红橙相近，测试阈值区分度）
    img = make_bg(seed=400)
    draw_circle(img, COLORS["orange"], (150, 180), 50)   # 橙色干扰块
    draw_circle(img, COLORS["red"], (W // 2, H // 2), 80)  # 红色目标
    img = add_noise(img, seed=13)
    save(img, "04_red_with_orange.png")

    print("\n全部测试图生成完成，输出目录:", OUT_DIR)


if __name__ == "__main__":
    main()
