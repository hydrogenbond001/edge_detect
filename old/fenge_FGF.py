import cv2
import numpy as np
from scipy.ndimage import gaussian_filter

def guided_filter(I, p, r, eps):
    mean_I = cv2.boxFilter(I, cv2.CV_64F, (r, r))
    mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))
    mean_Ip = cv2.boxFilter(I * p, cv2.CV_64F, (r, r))
    cov_Ip = mean_Ip - mean_I * mean_p

    mean_II = cv2.boxFilter(I * I, cv2.CV_64F, (r, r))
    var_I = mean_II - mean_I * mean_I

    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))

    q = mean_a * I + mean_b
    return q

def gamma_correction(image, gamma):
    inv_gamma =  0.3 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)

def preprocess_image(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Apply guided filter on V channel for light adjustment
    v_filtered = guided_filter(v, v, r=8, eps=0.1)

    # Apply adaptive gamma correction
    avg_brightness = np.mean(v_filtered) / 255.0
    gamma = 0.3 if avg_brightness < 0.3 else 0.4            #gamma = 0.5时试试理解这里
    v_corrected = gamma_correction(v_filtered.astype(np.uint8), gamma)

    # Merge the corrected V channel back
    hsv_corrected = cv2.merge([h, s, v_corrected])
    img_corrected = cv2.cvtColor(hsv_corrected, cv2.COLOR_HSV2BGR)
    return img_corrected

def detect_guideline(img):
    height, width = img.shape[:2]
    x1, y1, x2, y2 = width // 3, height // 8, 3 * width // 4, 3 * height // 4
    roi = img[y1:y2, x1:x2]
    
    img=cv2.GaussianBlur(roi, (3,3), 0)
    # Edge detection using Canny
    edges = cv2.Canny(img, 50, 150)
    #edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, (7,7))
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 720, threshold=80, minLineLength=500, maxLineGap=60)

    # 初始化变量以存储最下面的直线
    lowest_line = None
    max_y = 0

    # 遍历检测到的直线
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                # 找到所有端点中最大的y值
                if y1 > max_y or y2 > max_y:
                    max_y = max(y1, y2)
                    lowest_line = (x1, y1, x2, y2)

    # 在图像上绘制最下面的直线
    if lowest_line:
        x1, y1, x2, y2 = lowest_line
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        print(f"The lowest line coordinates: ({x1}, {y1}) to ({x2}, {y2})")
        
    
    return edges,img,

# Test function to process and detect guideline in an image
def process_agv_image(img_path):
    img = cv2.imread(img_path)
    preprocessed_img = preprocess_image(img)
    line_mask ,img= detect_guideline(preprocessed_img)

    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    preprocessed_img = cv2.resize(preprocessed_img, None, fx=0.5, fy=0.5)
    line_mask = cv2.resize(line_mask, None, fx=0.5, fy=0.5)
    # Show the results
    cv2.imshow("Original Image", img)
    cv2.imshow("Preprocessed Image", preprocessed_img)
    cv2.imshow("Detected Guideline", line_mask)
    # print("Navigation Deviation (pixels):", deviation)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Run the function with a sample image path
process_agv_image(r'C:\Users\L3101\Pictures\1111.png')
# process_agv_image(r'C:\Users\L3101\Pictures\Camera Roll\1245.png')
