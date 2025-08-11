FROM ubuntu:22.04

# 不联网安装任何包，只使用系统原有或你带进来的依赖
WORKDIR /app

# 拷贝程序和依赖
COPY bin/test /app/test 
COPY lib/ /usr/lib/

# 设为默认启动程序
ENTRYPOINT ["./test"]
