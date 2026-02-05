cmake_minimum_required(VERSION 3.0)
project(simple_controller)

find_package(gazebo REQUIRED)

include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})
add_definitions(${GAZEBO_CXX_FLAGS})

add_library(simple_controller SHARED simple_controller.cc)
target_link_libraries(simple_controller ${GAZEBO_LIBRARIES})
