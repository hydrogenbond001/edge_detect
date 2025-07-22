import cv2
import numpy as np

def detect_lines_and_calculate_slope(image_path):
    # 1. 加载图像并灰度化
    image = cv2.imread(image_path)
    
    # image = cv2.resize(image, None, fx=0.5, fy=0.5)
    image = cv2.resize(image, (720, 480))

    darker1 = cv2.subtract(image, np.full(image.shape, 50, dtype=np.uint8))
    
    gray = cv2.cvtColor(darker1, cv2.COLOR_BGR2GRAY)

    # 2. 高斯滤波去噪
    blurred = cv2.GaussianBlur(gray, (7, 5), 0)

    # 3. 使用Canny边缘检测
    edges = cv2.Canny(blurred, 100, 150)

    # 4. 使用霍夫变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 720, threshold=140, minLineLength=100, maxLineGap=100)
    
    # 霍夫直线检测
    lines = cv2.HoughLinesP(edges, 1, np.pi / 720, 160, minLineLength=100, maxLineGap=60)
    if lines is not None:
        for line in lines:
            x1_, y1_, x2_, y2_ = line[0]
            cv2.line(image, (x1_, y1_), (x2_, y2_), (0, 255, 0), 2)
    
    # 6. 计算并返回平均斜率
    # avg_slope = None
    # if slopes:
    #     avg_slope = sum(slopes) / len(slopes)
    #     print("平均斜率：", avg_slope)
    # else:
    #     print("未检测到符合条件的直线")
    
    # 显示检测结果
    cv2.imshow('1', gray)
    cv2.imshow('2', blurred)
    cv2.imshow('3', edges)
    cv2.imshow('Detected Lines', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return avg_slope

# 调用函数并传入图像路径
image_path = r'C:\Users\L3101\Pictures\722.png'  # 替换为实际的图像路径
average_slope = detect_lines_and_calculate_slope(image_path)
