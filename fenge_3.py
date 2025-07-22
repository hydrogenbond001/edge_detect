import cv2
import numpy as np

def detect_lines_and_calculate_slope(image_path):
    # 1. 加载图像并灰度化
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. 高斯滤波去噪
    blurred = cv2.GaussianBlur(gray, (7, 5), 0)

    # 3. 使用Canny边缘检测
    edges = cv2.Canny(blurred, 100, 150)

    # 4. 使用霍夫变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 720, threshold=140, minLineLength=100, maxLineGap=100)
    
    # 5. 过滤短线段和不规则直线
    slopes = []
    min_length = 30  # 设置直线的最小长度
    for line in lines:
        for x1, y1, x2, y2 in line:
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if length > min_length:  # 过滤掉较短的直线
                # 计算斜率
                if x2 - x1 != 0:  # 避免除以零
                    slope = (y2 - y1) / (x2 - x1)
                    # 过滤掉不在指定范围内的斜率，例：只保留接近水平的直线
                    if -0.5 < slope < 0.5:  
                        slopes.append(slope)
                        # 在图像上绘制检测到的直线
                        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # 6. 计算并返回平均斜率
    avg_slope = None
    if slopes:
        avg_slope = sum(slopes) / len(slopes)
        print("平均斜率：", avg_slope)
    else:
        print("未检测到符合条件的直线")
    
    # 显示检测结果
    cv2.imshow('1', gray)
    cv2.imshow('2', blurred)
    cv2.imshow('3', edges)
    cv2.imshow('Detected Lines', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return avg_slope

# 调用函数并传入图像路径
image_path = r'C:\Users\L3101\Pictures\Camera Roll\newcut\frame_100.jpg'  # 替换为实际的图像路径
average_slope = detect_lines_and_calculate_slope(image_path)
