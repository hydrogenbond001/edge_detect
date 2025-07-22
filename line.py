import cv2
import numpy as np

# 读取图片
img = cv2.imread('/Users/L3101/Pictures/7777.png')

# 转换为 HSV 色彩空间
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# -------------------
# 颜色1：浅黄色区域
# -------------------
lower_yellow = np.array([30, 0, 80])   # H, S, V
upper_yellow = np.array([80, 100, 255])
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
result_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

# -------------------
# 颜色2：浅紫色区域
# -------------------
lower_purple = np.array([75, 0, 100])  # H, S, V
upper_purple = np.array([135, 100, 255])
mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
result_purple = cv2.bitwise_and(img, img, mask=mask_purple)

# -------------------
# 保存结果
# -------------------
# cv2.imwrite('mask_yellow.png', mask_yellow)
# cv2.imwrite('result_yellow.png', result_yellow)

# cv2.imwrite('mask_purple.png', mask_purple)
# cv2.imwrite('result_purple.png', result_purple)

print("分离完成，结果保存在当前目录。")
