import cv2
import numpy as np
import serial
import time
import math

# 初始化串口通信
def init_serial(port, baudrate):
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # 给串口一些初始化时间
    return ser

# 初始化摄像头
def init_camera(camera_id=0):
    return cv2.VideoCapture(camera_id)

# 图像处理和直线检测
def process_frame(frame, left_lower_hsv, left_upper_hsv, right_lower_hsv, right_upper_hsv, kernel):
    height, width = frame.shape[:2]
    x1, y1, x2, y2 = width // 4, height // 3, 3 * width // 4, 3 * height // 4

    # 截取ROI区域
    roi = frame[y1:y2, x1:x2]

    # 将图像从BGR转换为HSV
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 创建左右颜色掩膜
    left_mask = cv2.inRange(hsv_image, left_lower_hsv, left_upper_hsv)
    right_mask = cv2.inRange(hsv_image, right_lower_hsv, right_upper_hsv)

    # 使用掩膜分割颜色区域
    left_result = cv2.bitwise_and(frame, frame, mask=left_mask)
    right_result = cv2.bitwise_and(frame, frame, mask=right_mask)

    # 合并左右分割结果
    combined_result = cv2.addWeighted(left_result, 1, right_result, 1, 0)

    # 去除噪点 - 应用开运算
    combined_result = cv2.morphologyEx(combined_result, cv2.MORPH_OPEN, kernel)
    
    # 二值化
    _, combined_result = cv2.threshold(combined_result, 127, 255, cv2.THRESH_BINARY)

    # 检测边缘
    edges = cv2.Canny(roi, 50, 150, apertureSize=3)

    # 霍夫变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=130, minLineLength=50, maxLineGap=200)

    return roi, combined_result, edges, lines

# 发送斜率数据到串口
def send_slope_data(ser, lines, roi):
    for line in lines:
        x1, y1, x2, y2 = line[0]  # 解包为四个点 (x1, y1, x2, y2)

        # 计算斜率
        if x2 - x1 != 0:
            slope = 10*math.degrees(10*(y2 - y1) / (x2 - x1))
            print(f"{(x1/2+x2/2):.0f}", end=' ')
            print(f"{(y1/2+y2/2):.0f}", end=' ')
            print(f"{slope:.0f}")

            # 将斜率发送到串口
            ser.write(b'\x03')
            ser.write(f'{slope:.0f}\n'.encode())
            ser.write(f'{slope:.0f}\n'.encode())  # \n结尾
            ser.write(b'\xFE')

        # 在原图上绘制直线
        cv2.line(roi, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 摄像头和图像处理函数
def capture_and_process(cap, ser, left_lower_hsv, left_upper_hsv, right_lower_hsv, right_upper_hsv, kernel):
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        return

    # 处理图像，检测直线
    roi, combined_result, edges, lines = process_frame(frame, left_lower_hsv, left_upper_hsv, right_lower_hsv, right_upper_hsv, kernel)

    # # 发送斜率数据到串口
    # if lines is not None:
    #     send_slope_data(ser, lines, roi)

    # 显示结果
    cv2.imshow('Combined Result', combined_result)
    cv2.imshow('Edges', edges)
    cv2.imshow('Detected Lines', frame)

# 主函数
def main():
    # 初始化串口和摄像头
    # ser = init_serial('COM6', 9600)  # 根据实际串口号设置
    cap = init_camera(0)
    flag=0
    # HSV颜色范围
    left_lower_hsv = np.array([20, 10, 100])
    left_upper_hsv = np.array([40, 50, 255])
    right_lower_hsv = np.array([50, 10, 50])
    right_upper_hsv = np.array([70, 50, 200])

    # 定义结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))

    while True:
        ret, frame = cap.read()
        if not ret:
            return

        # 处理图像，检测直线
        roi, combined_result, edges, lines = process_frame(frame, left_lower_hsv, left_upper_hsv, right_lower_hsv, right_upper_hsv, kernel)
        # if lines is not None:
        #     send_slope_data(ser, lines, roi)


        # 显示结果
        cv2.imshow('Combined Result', combined_result)
        cv2.imshow('Edges', edges)
        cv2.imshow('Detected Lines', frame)


        # 读取串口接收到的数据
        # if ser.in_waiting > 0:
        #     # 读取串口接收到的字符
        #     flag = ser.read().decode('utf-8')

        # 当接收到字符 'a' 时开始运行图像处理
        if flag == 'a':
            print("Received 'a', starting image processing...")
            # capture_and_process(cap, ser, left_lower_hsv, left_upper_hsv, right_lower_hsv, right_upper_hsv, kernel)
            # 发送斜率数据到串口
            # if lines is not None:
            #     send_slope_data(ser, lines, roi)
            # flag=0
        


        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关闭串口和摄像头
    # ser.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()




# import cv2
# import numpy as np

# # 初始化摄像头
# cap = cv2.VideoCapture(0)

# # 设置字体
# font = cv2.FONT_HERSHEY_SIMPLEX

# # 定义 HSV 范围用于颜色分割（这里以左右颜色为例）
# # 左边颜色范围（根据实际图像调整）
# left_lower_hsv = np.array([20, 10, 100])  # 最小HSV值
# left_upper_hsv = np.array([40, 50, 255])  # 最大HSV值

# # 右边颜色范围（根据实际图像调整）
# right_lower_hsv = np.array([50, 10, 50])  # 最小HSV值
# right_upper_hsv = np.array([70, 50, 200])  # 最大HSV值

# # 定义结构元素
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
# while True:
#     # 读取摄像头帧
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # 将图像从BGR转换为HSV
#     hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # 创建左右颜色掩膜
#     left_mask = cv2.inRange(hsv_image, left_lower_hsv, left_upper_hsv)
#     right_mask = cv2.inRange(hsv_image, right_lower_hsv, right_upper_hsv)

#     # 使用掩膜分割颜色区域
#     left_result = cv2.bitwise_and(frame, frame, mask=left_mask)
#     right_result = cv2.bitwise_and(frame, frame, mask=right_mask)

#     # 合并左右分割结果
#     combined_result = cv2.addWeighted(left_result, 1, right_result, 1, 0)

#     # 计算左右部分的平均HSV值
#     # left_hsv_mean = cv2.mean(cv2.cvtColor(left_result, cv2.COLOR_BGR2HSV), mask=left_mask)[:3]
#     # right_hsv_mean = cv2.mean(cv2.cvtColor(right_result, cv2.COLOR_BGR2HSV), mask=right_mask)[:3]

#     # 将HSV值转换为字符串，便于在图像上显示
#     # left_hsv_text = f"Left HSV: H={left_hsv_mean[0]:.2f}, S={left_hsv_mean[1]:.2f}, V={left_hsv_mean[2]:.2f}"
#     # right_hsv_text = f"Right HSV: H={right_hsv_mean[0]:.2f}, S={right_hsv_mean[1]:.2f}, V={right_hsv_mean[2]:.2f}"

#     # 在图像上显示左右部分的HSV值
#     # cv2.putText(combined_result, left_hsv_text, (10, 30), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
#     # cv2.putText(combined_result, right_hsv_text, (frame.shape[1] // 2 + 10, 30), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

#     #打印hsv
#     # print(left_hsv_text)
#     # print('\r\n')
#     # print(right_hsv_text)
#     # 显示处理后的图像


#     # 二值化
#     _, combined_result = cv2.threshold(combined_result, 127, 255, cv2.THRESH_BINARY)

#     # 去除噪点 - 应用开运算
#     combined_result = cv2.morphologyEx(combined_result, cv2.MORPH_OPEN, kernel)

#     # 检测边缘
#     edges = cv2.Canny(combined_result, 50, 150, apertureSize=3)

#     # 霍夫变换检测直线
#     lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=150)

#     # 绘制检测到的直线并计算斜率
#     if lines is not None:
#         for rho, theta in lines[:, 0]:
#             # 计算直线的两个点
#             a = np.cos(theta)
#             b = np.sin(theta)
#             x0 = a * rho
#             y0 = b * rho
#             x1 = int(x0 + 1000 * (-b))
#             y1 = int(y0 + 1000 * (a))
#             x2 = int(x0 - 1000 * (-b))
#             y2 = int(y0 - 1000 * (a))

#             # 计算斜率
#             if x2 - x1 != 0:
#                 slope = (y2 - y1) / (x2 - x1)
#                 print(f"Slope: {slope:.2f}")

#             # 在原图上绘制直线
#             cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#     # 显示结果
#     cv2.imshow('Combined Result', combined_result)
#     cv2.imshow('Edges', edges)
#     cv2.imshow('Detected Lines', frame)

#     # 按 'q' 键退出
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 释放摄像头和关闭窗口
# cap.release()
# cv2.destroyAllWindows()

