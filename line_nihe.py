import cv2
import numpy as np

# 读取图像
img = cv2.imread('7777.png')
h, w = img.shape[:2]

# 转灰度 + 去噪
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)

# 只关注图像中间区域（垂直方向）
roi_top = h // 2 - 120
roi_bot = h // 2 + 530
roi_left=150
roi_right=1200
roi = blur[roi_top:roi_bot, :]
cv2.imshow('roi', roi)

# Canny边缘检测
edges = cv2.Canny(roi, 50, 150)

# 显示中间 ROI 边缘图像
cv2.imshow("Edges", edges)

# 原图副本，用于画点
out_img = img.copy()
# cv2.line(out_img, (0, roi_top), (w , roi_bot), (255, 0, 0), 12)
# print("roi_top",roi_top,"roi_bot",roi_bot)
line_points = []

# 分割区域
left_roi = edges[:, :w // 3]
middle_roi = edges[:, w // 3 : 2 * w // 3]
offset_middle =  w // 3  # 中间区域偏移回整图
right_roi = edges[:, -w // 3:]
offset_right = 2 * w // 3 # 右区域偏移回整图

cv2.imshow('left_roi', left_roi)
cv2.imshow('middle_roi', middle_roi)
cv2.imshow('right_roi', right_roi)

# 提取左、右边缘点
def get_edge_points(sub_edges, x_offset=0):
    points = []
    for y in range(sub_edges.shape[0]):
        row = sub_edges[y]
        edge_x = np.where(row > 0)[0]
        if len(edge_x) > 0:
            x_mean = int(np.mean(edge_x)) + x_offset
            y_real = y + roi_top
            points.append((x_mean, y_real))
    return points

left_points = get_edge_points(left_roi)
middle_points= get_edge_points(middle_roi,offset_middle)
right_points = get_edge_points(right_roi, offset_right)

# # 合并左右点
fit_points = left_points + middle_points + right_points



import random

def ransac_line_fit(points, num_iters=100, distance_threshold=3):
    best_inliers = []
    best_model = None

    for _ in range(num_iters):
        # 随机选2个点
        sample = random.sample(points, 2)
        (x1, y1), (x2, y2) = sample

        # 跳过垂直线避免除零
        if x2 == x1:
            continue

        # 拟合直线参数 y = kx + b
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1

        inliers = []
        for (x, y) in points:
            # 计算点到直线的距离
            distance = abs(k * x - y + b) / np.sqrt(k**2 + 1)
            if distance < distance_threshold:
                inliers.append((x, y))

        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_model = (k, b)

    return best_model, best_inliers


# 可视化所有拟合点
for (x, y) in fit_points:
    cv2.circle(out_img, (x, y), 2, (0, 0, 255), -1)

# 用 RANSAC 拟合直线
(k, b), inliers = ransac_line_fit(fit_points)

# 拟合线端点
x_start = 0
y_start = int(k * x_start + b)

x_end = w
y_end = int(k * x_end + b)

# 在图像上画线
cv2.line(out_img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

# 输出斜率
print(f"斜率 k = {k:.4f}")

# 计算中间区域左右边界的 x 值
middle_left_x = w // 3
middle_right_x = 2 * w // 3

# 对应直线上的 y 值
y_left = k * middle_left_x + b
y_right = k * middle_right_x + b

# 中间的“高度间距”
middle_gap = abs(y_right - y_left)

print(f"中间区域直线 y 值差（间距）: {middle_gap:.2f} 像素")


# 可视化 inliers 点（拟合点）
for (x, y) in inliers:
    cv2.circle(out_img, (x, y), 2, (255, 0, 0), -1)

# 再次显示图像
cv2.imshow("Fitted Line", out_img)
cv2.waitKey(0)
cv2.destroyAllWindows()