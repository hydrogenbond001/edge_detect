import numpy as np
import matplotlib.pyplot as plt

# 定义幅度函数 f(x)
def f(x):
    return 20 * np.log10(10 / (x * (x + 1) * (0.5 * x + 1)))

# 设置x的取值范围 (例如从0.1到100，避免x=0时的除零错误)
x = np.linspace(0.1, 100, 1000)

# 计算幅度函数的值
y = f(x)

# 计算幅度的变化率（近似模拟相位）
dy_dx = np.gradient(y, x)  # 计算幅度的导数，模拟相位变化

# 绘制幅频特性和相频特性曲线
plt.figure(figsize=(8, 6))

# 幅频特性
plt.subplot(2, 1, 1)
plt.plot(x, y, label=r'$f(x) = 20 \log_{10}\left( \frac{10}{x (x+1) (0.5x+1)} \right)$', color='b')
plt.title("幅频特性曲线")
plt.xlabel("x")
plt.ylabel("幅度 (dB)")
plt.grid(True)
plt.xscale('log')  # x轴使用对数尺度
plt.legend()

# 相频特性（幅度的变化率）
plt.subplot(2, 1, 2)
plt.plot(x, dy_dx, label="相频特性 (近似)", color='r')
plt.title("相频特性曲线")
plt.xlabel("x")
plt.ylabel("相位变化 (dB/Hz)")
plt.grid(True)
plt.xscale('log')  # x轴使用对数尺度
plt.legend()

# 显示图像
plt.tight_layout()
plt.show()
