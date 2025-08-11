FROM ubuntu:22.04

# 设置非交互模式避免 tzdata 等阻塞
ENV DEBIAN_FRONTEND=noninteractive

# 安装 gcc
RUN apt update && apt install -y gcc

# 拷贝代码
COPY . /src
WORKDIR /src

# 编译 .so 动态库
RUN gcc -fPIC -shared -o libexample.so example.c

# 编译测试程序并链接 .so
RUN gcc -o test test.c -L. -lexample

# 设置 LD_LIBRARY_PATH 以运行
ENV LD_LIBRARY_PATH=/src
CMD ["ldd --version"]
# 默认执行测试程序
CMD ["./test"]
