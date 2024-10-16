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

    # 将图像从BGR转换为HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 计算每个通道的平均值
    avg_h = np.mean(hsv_frame[:, :, 0])  # H通道平均值
    avg_s = np.mean(hsv_frame[:, :, 1])  # S通道平均值
    avg_v = np.mean(hsv_frame[:, :, 2])  # V通道平均值

    # 打印平均HSV值
    print(f"图像的平均HSV值为: H={avg_h:.2f}, S={avg_s:.2f}, V={avg_v:.2f}")

    # 在图像上显示平均HSV值
    avg_hsv_text = f"Avg HSV: H={avg_h:.2f}, S={avg_s:.2f}, V={avg_v:.2f}"
    cv2.putText(frame, avg_hsv_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 显示当前帧
    cv2.imshow('Camera Feed with Avg HSV', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭所有窗口
cap.release()
cv2.destroyAllWindows()





# Right HSV: H=58.84, S=13.42, V=169.29
# Left HSV: H=34.30, S=16.12, V=174.51