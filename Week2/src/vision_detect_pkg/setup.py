from setuptools import setup

package_name = "vision_detect_pkg"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="shuaijuncheng",
    maintainer_email="shuaijuncheng@example.com",
    description="视觉目标检测 ROS2 发布/订阅节点",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "target_publisher = vision_detect_pkg.target_publisher:main",
            "target_subscriber = vision_detect_pkg.target_subscriber:main",
        ],
    },
)
