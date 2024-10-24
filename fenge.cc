#include <opencv2/opencv.hpp>
#include <vector>

int main() {
    // 读取图像
    cv::Mat frame = cv::imread("C:\Users\L3101\Pictures\Camera Roll/1245.png        ");
    if (frame.empty()) {
        std::cerr << "Could not open or find the image!" << std::endl;
        return -1;
    }

    int height = frame.rows;
    int width = frame.cols;

    // 定义感兴趣区域ROI
    int x1 = width / 4;
    int y1 = height / 5;
    int x2 = 3 * width / 4;
    int y2 = 3 * height / 4;
    cv::Mat roi = frame(cv::Rect(x1, y1, x2 - x1, y2 - y1));

    // 高斯模糊
    cv::GaussianBlur(frame, frame, cv::Size(7, 7), 0);

    // 将图像从BGR转换为HSV格式
    cv::Mat hsv_image;
    cv::cvtColor(frame, hsv_image, cv::COLOR_BGR2HSV);

    // 定义颜色范围
    cv::Scalar left_lower_hsv(30, 100, 100); // 示例左边颜色范围
    cv::Scalar left_upper_hsv(90, 255, 255);
    cv::Scalar right_lower_hsv(0, 100, 100); // 示例右边颜色范围
    cv::Scalar right_upper_hsv(10, 255, 255);

    // 创建左右颜色掩膜
    cv::Mat left_mask, right_mask;
    cv::inRange(hsv_image, left_lower_hsv, left_upper_hsv, left_mask);
    cv::inRange(hsv_image, right_lower_hsv, right_upper_hsv, right_mask);

    // 使用掩膜分割颜色区域
    cv::Mat left_result, right_result;
    cv::bitwise_and(frame, frame, left_result, left_mask);
    cv::bitwise_and(frame, frame, right_result, right_mask);

    // 合并左右分割结果
    cv::Mat combined_result;
    cv::addWeighted(left_result, 1, right_result, 1, 0, combined_result);

    // 去除噪点 - 应用开运算
    cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));
    cv::morphologyEx(combined_result, combined_result, cv::MORPH_OPEN, kernel);

    // 二值化
    cv::threshold(combined_result, combined_result, 127, 255, cv::THRESH_BINARY);

    // 检测边缘
    cv::Mat edges;
    cv::Canny(roi, edges, 50, 150);

    // 霍夫变换检测直线
    std::vector<cv::Vec4i> lines;
    cv::HoughLinesP(edges, lines, 1, CV_PI / 720, 130, 150, 200);

    // 在图像上绘制直线
    for (size_t i = 0; i < lines.size(); i++) {
        cv::line(roi, cv::Point(lines[i][0], lines[i][1]), cv::Point(lines[i][2], lines[i][3]), cv::Scalar(0, 255, 0), 2);
    }

    // 显示结果
    cv::imshow("Edges", edges);
    cv::imshow("Combined", combined_result);
    cv::imshow("ROI with Lines", roi);
    cv::waitKey(0);
    
    return 0;
}
