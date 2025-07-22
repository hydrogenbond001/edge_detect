cmake_minimum_required(VERSION 3.10)
project(fenge VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置 OpenCV 路径
set(OpenCV_DIR "C:\Program Files\opencv\build")

# 开启编译器警告
add_compile_options(-Wall -Wextra)

# 查找 src 目录下所有源文件
file(GLOB DIR_SRCS "src/fenge.cc")

# 添加可执行文件（假设 fenge.cc 也在 src 目录中）
add_executable(fenge ${DIR_SRCS} src/fenge.cc)
