import cv2
import numpy as np

# 打开摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    # 读取摄像头的一帧
    ret, frame = cap.read()

    if not ret:
        print("无法获取摄像头帧")
        break

    # 显示当前帧
    cv2.imshow('Camera Feed', frame)

    # 按 'c' 键拍照并计算平均RGB值
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # 获取图像的尺寸
        h, w, _ = frame.shape
        
        # 计算每个通道的平均值
        avg_b = np.mean(frame[:, :, 0])  # B通道平均值
        avg_g = np.mean(frame[:, :, 1])  # G通道平均值
        avg_r = np.mean(frame[:, :, 2])  # R通道平均值

        # 打印平均RGB值
        print(f"图像的平均RGB值为: R={avg_r:.2f}, G={avg_g:.2f}, B={avg_b:.2f}")

        # 在图像上显示平均RGB值
        avg_rgb_text = f"Avg RGB: R={avg_r:.2f}, G={avg_g:.2f}, B={avg_b:.2f}"
        cv2.putText(frame, avg_rgb_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示拍照的图像及平均RGB值
        cv2.imshow('Captured Image with Avg RGB', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
