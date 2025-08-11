#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <windows.h>

void showError(const std::string& message) {
    MessageBoxA(NULL, message.c_str(), "Error", MB_ICONERROR | MB_OK);
}

void processFrame(cv::Mat& frame) {
    // 1. 缩放图像到固定尺寸（保持比例）
    cv::resize(frame, frame, cv::Size(720, 480));
    
    // 2. 转HSV并提取H通道
    cv::Mat hsv, h_channel;
    cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);
    std::vector<cv::Mat> hsv_channels;
    cv::split(hsv, hsv_channels);
    h_channel = hsv_channels[0];
    
    // 3. 自适应阈值处理
    cv::Mat binary;
    cv::adaptiveThreshold(h_channel, binary, 255, 
                         cv::ADAPTIVE_THRESH_GAUSSIAN_C,
                         cv::THRESH_BINARY, 23, 4);
    
    // 4. 高斯模糊
    cv::GaussianBlur(binary, binary, cv::Size(1,1), 0);
    
    // 5. 形态学操作
    cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(1,1));
    cv::morphologyEx(binary, binary, cv::MORPH_CLOSE, kernel);
    
    // 6. Canny边缘检测
    cv::Mat edges;
    cv::Canny(binary, edges, 70, 150);
    
    // 7. 霍夫变换检测直线
    std::vector<cv::Vec4i> lines;
    cv::HoughLinesP(edges, lines, 1, CV_PI/720, 160, 100, 60);
    
    // 8. 绘制检测到的直线
    for (size_t i = 0; i < lines.size(); i++) {
        cv::line(frame, 
                cv::Point(lines[i][0], lines[i][1]),
                cv::Point(lines[i][2], lines[i][3]), 
                cv::Scalar(0, 255, 0), 2);
    }
    cv::imshow("binary", binary);
}

int main() {
    // 打开摄像头
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        showError("无法打开摄像头！\n请检查：\n1. 摄像头是否连接\n2. 驱动程序是否正常");
        return -1;
    }
    
    // 设置摄像头参数（可选）
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 1280);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 720);
    cap.set(cv::CAP_PROP_FPS, 30);
    
    cv::Mat frame;
    cv::namedWindow("Lane Detection", cv::WINDOW_AUTOSIZE);
    
    while (true) {
        // 捕获帧
        cap >> frame;
        if (frame.empty()) {
            showError("无法从摄像头获取帧！");
            break;
        }
        
        // 处理帧
        processFrame(frame);
        
        // 显示结果
        cv::imshow("Lane Detection", frame);
        
        // 按ESC退出
        if (cv::waitKey(1) == 27) {
            break;
        }
    }
    
    // 释放资源
    cap.release();
    cv::destroyAllWindows();
    return 0;
}