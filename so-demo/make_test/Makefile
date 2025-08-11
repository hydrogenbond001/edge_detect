# 编译器
CXX = g++
CXXFLAGS = -Wall -O2

# 源文件 & 目标文件
SRCS = main.cpp mylib.cpp
OBJS = $(SRCS:.cpp=.o)

# 可执行文件名
TARGET = myapp

# 默认目标
all: $(TARGET)

# 生成可执行文件
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# 生成 .o 文件
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# 清理目标
clean:
	rm -f $(OBJS) $(TARGET)
