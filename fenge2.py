import cv2
import numpy as np

# 读取图像
image = cv2.imread(r'C:\Users\L3101\Pictures\tu.jpg')  # 替换为你的图像文件路径
if image is None:
    print("Image not found!")
    exit()

# 1. 图像预处理：转换为灰度并进行高斯模糊
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 2. 边缘提取：使用 Canny 算法检测边缘
edges = cv2.Canny(blurred, 50, 150)

# 3. 提取感兴趣区域（ROI）：根据实际情况截取图像中的导引线区域
height, width = edges.shape
roi = edges[int(height/2):, :]  # 取图像下半部分

# 4. 轮廓检测：提取导引线轮廓
contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 5. 导引线筛选与绘制
output = image.copy()
for contour in contours:
    # 计算轮廓的周长和面积
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if area > 100:  # 根据实际情况选择合适的面积阈值
        cv2.drawContours(output[int(height/2):, :], [contour], -1, (0, 255, 0), 2)

# 显示结果
cv2.imshow("Original Image", image)
cv2.imshow("Detected Guide Line", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
