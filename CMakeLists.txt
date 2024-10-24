cmake_minimum_required(VERSION 3.10)

project(fenge)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(fenge fenge.cc)
target_link_libraries(fenge ${OpenCV_LIBS})
