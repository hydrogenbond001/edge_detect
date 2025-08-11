cmake_minimum_required(VERSION 3.10)
project(line VERSION 1.0)

# Set compiler and standards
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MINGW)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--subsystem,console")
endif()
# 去掉控制台窗口
# if(WIN32)
#     set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")
# endif()
# Only set these if you specifically need to override system defaults
set(CMAKE_C_COMPILER "C:/w64devkit/bin/gcc.exe")
set(CMAKE_CXX_COMPILER "C:/w64devkit/bin/g++.exe")

# Find OpenCV package
if(NOT OpenCV_FOUND)
	set(OpenCV_DIR "C:/Users/L3101/Documents/GitHub/edge_detect/opencv_mingw")
set(OpenCV_DIR "C:/Users/L3101/Documents/GitHub/edge_detect/opencv/build/install")
	
	message( "OpenCV  found.")
endif()


find_package(OpenCV REQUIRED)
message(STATUS "OpenCV_INCLUDE_DIRS = ${OpenCV_INCLUDE_DIRS}")
# Enable compiler warnings
add_compile_options(-Wall -Wextra -Wpedantic)

# Add executable
add_executable(line line.cpp)

# Link OpenCV libraries to your executable
target_link_libraries(line PRIVATE ${OpenCV_LIBS})

# Include OpenCV headers
target_include_directories(line PRIVATE ${OpenCV_INCLUDE_DIRS})
