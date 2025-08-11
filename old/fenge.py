import cv2
import numpy as np

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 定义左边和右边颜色的 HSV 范围
# 左边颜色范围
left_lower_hsv = np.array([15, 10, 100])  # 最小 HSV 值
left_upper_hsv = np.array([40, 50, 255])   # 最大 HSV 值

# 右边颜色范围
right_lower_hsv = np.array([45, 10, 45])   # 最小 HSV 值
right_upper_hsv = np.array([70, 50, 200])   # 最大 HSV 值

# 定义结构元素
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))

while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        break
    height, width = frame.shape[:2]
    x1, y1, x2, y2 = width // 4, height // 4, 3 * width // 4, 3 * height // 4

    # 截取ROI区域
    roi = frame[y1:y2, x1:x2]

    # 将图像从 BGR 转换为 HSV
    hsv_image = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # 创建左边颜色的掩膜
    left_mask = cv2.inRange(hsv_image, left_lower_hsv, left_upper_hsv)
    # 创建右边颜色的掩膜
    right_mask = cv2.inRange(hsv_image, right_lower_hsv, right_upper_hsv)

    # 使用掩膜分割颜色区域
    left_result = cv2.bitwise_and(frame, frame, mask=left_mask)
    right_result = cv2.bitwise_and(frame, frame, mask=right_mask)

    # 合并左右分割结果
    combined_result = cv2.addWeighted(left_result, 1, right_result, 1, 0)

    # 二值化
    _, combined_result = cv2.threshold(combined_result, 127, 255, cv2.THRESH_BINARY)

    # 去除噪点 - 应用开运算
    combined_result = cv2.morphologyEx(combined_result, cv2.MORPH_OPEN, kernel)

    # 检测边缘
    edges = cv2.Canny(combined_result, 50, 150, apertureSize=3)

    # 霍夫变换检测直线
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

    # 绘制检测到的直线并计算斜率
    if lines is not None:
        for rho, theta in lines[:, 0]:
            # 计算直线的两个点
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            # 计算斜率
            if x2 - x1 != 0:
                slope = (y2 - y1) / (x2 - x1)
                print(f"Slope: {slope:.2f}")

            # 在原图上绘制直线
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 显示结果
    cv2.imshow('Combined Result', combined_result)
    cv2.imshow('Edges', edges)
    cv2.imshow('Detected Lines', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()
