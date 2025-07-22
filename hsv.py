import cv2
import numpy as np

def process_frame(frame):
    height, width = frame.shape[:2]

    # ROI 区域
    x1 = width // 3
    y1 = height // 8
    x2 = 3 * width // 4
    y2 = 3 * height // 4
    roi = frame[y1:y2, x1:x2]

    # 转 HSV
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v= cv2.split(hsv_image)
    h_colored = cv2.applyColorMap(h, cv2.COLORMAP_HSV)
    # 二值化 (HSV → BGR → 灰度 → 二值)
    bina = cv2.threshold(h_colored, 59, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(bina, cv2.COLOR_BGR2GRAY)

    # 模糊
    blurred = cv2.GaussianBlur(gray, (1, 1), 0)

    # 边缘检测
    edges = cv2.Canny(blurred, 70, 150)

    # 霍夫直线检测
    lines = cv2.HoughLinesP(edges, 1, np.pi / 720, 160, minLineLength=100, maxLineGap=60)
    if lines is not None:
        for line in lines:
            x1_, y1_, x2_, y2_ = line[0]
            cv2.line(frame, (x1_, y1_), (x2_, y2_), (0, 255, 0), 2)

    # 显示图像
    cv2.imshow("Edges", edges)
    cv2.imshow("bina", bina)
    # cv2.imshow("roi", roi)
    cv2.imshow("frame", frame)
    # print(h,s,v)
    # print(bina.shape) #(1069, 1903, 3)
    
    # np.savetxt("bina_pixels.txt", bina, fmt='%3d')
    # print("bina 图像像素值已保存到 'bina_pixels.txt'")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ========= 主函数区域 =========

if __name__ == "__main__":
    # 读取图像
    img = cv2.imread("5678.png")  # 改成你上传的图片路径

    if img is None:
        print("无法读取图片，请检查路径")
        exit()


    # 核，用于腐蚀/膨胀等操作
    kernel = np.ones((3, 3), np.uint8)

    process_frame(img)
    
