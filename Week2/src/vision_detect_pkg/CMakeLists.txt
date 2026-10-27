cmake_minimum_required(VERSION 3.8)
project(vision_detect_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(target_position_interfaces REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  vision_detect_pkg/target_publisher.py
  vision_detect_pkg/target_subscriber.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
