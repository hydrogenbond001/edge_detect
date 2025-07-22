#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define MAX_POINTS 10000

using namespace cv;

// 初始化摄像头
VideoCapture init_camera_or_video(int camera_id, const std::string& video_path) {
    VideoCapture cap(camera_id);
    if (!cap.isOpened()) {
        fprintf(stderr, "警告：摄像头 %d 打开失败，尝试打开视频文件：%s\n", camera_id, video_path.c_str());

        cap.open(video_path);
        if (!cap.isOpened()) {
            fprintf(stderr, "错误：无法打开视频文件 %s\n", video_path.c_str());
            exit(1);
        } else {
            printf("提示：已切换为本地视频输入\n");
        }
    } else {
        printf("提示：成功打开摄像头 %d\n", camera_id);
    }
    return cap;
}

// 提取边缘中点（每行一个平均 x）
int get_edge_points(Mat edge_img, int y_offset, int x_offset, Point* out_points) {
    int count = 0;
    for (int y = 0; y < edge_img.rows; y++) {
        uchar* row = edge_img.ptr<uchar>(y);
        int sum_x = 0, cnt = 0;
        for (int x = 0; x < edge_img.cols; x++) {
            if (row[x] > 0) {
                sum_x += x;
                cnt++;
            }
        }
        if (cnt > 0) {
            int avg_x = sum_x / cnt + x_offset;
            int real_y = y + y_offset;
            out_points[count++] = Point(avg_x, real_y);
            if (count >= MAX_POINTS) break;
        }
    }
    return count;
}

// RANSAC 拟合直线
int ransac_fit(Point* points, int num_points, float* out_k, float* out_b) {
    if (num_points < 2) return 0;  // 防止传入点过少

    int best_inliers = 0;
    float best_k = 0, best_b = 0;

    srand((unsigned int)time(NULL));

    for (int i = 0; i < 100; i++) {
        int idx1 = rand() % num_points;
        int idx2 = rand() % num_points;
        if (idx1 == idx2) continue;

        Point p1 = points[idx1];
        Point p2 = points[idx2];

        if (p1.x == p2.x) continue;

        float k = (float)(p2.y - p1.y) / (p2.x - p1.x);
        if (fabs(k) > 1.0f) continue; // ✅ 斜率过滤

        float b = p1.y - k * p1.x;

        int inliers = 0;
        for (int j = 0; j < num_points; j++) {
            Point p = points[j];
            float dist = fabs(k * p.x - p.y + b) / sqrt(k * k + 1);
            if (dist < 3.0)
                inliers++;
        }

        if (inliers > best_inliers) {
            best_inliers = inliers;
            best_k = k;
            best_b = b;
        }
    }

    *out_k = best_k;
    *out_b = best_b;
    return best_inliers;
}


int main() {
VideoCapture cap;
    //VideoCapture cap = init_camera_or_video(2,"/home/orangepi/rknn-cpp-Multithreading-main/output.mp4"); // 使用 2 号摄像头
    if (!cap.open("/home/orangepi/rknn-cpp-Multithreading-main/output.mp4")) {
        return -1;
    }
    while (true) {
        Mat img;
        cap >> img;
        if (img.empty()) {
            fprintf(stderr, "Error: Frame capture failed\n");
            break;
        }

        int h = img.rows;
        int w = img.cols;

        Mat gray, blur, edges;
        cvtColor(img, gray, COLOR_BGR2GRAY);
        GaussianBlur(gray, blur, Size(7, 7), 0);

        int roi_top = h / 2 - 120;
        int roi_bot = h / 2 + 120;
        if (roi_top < 0 || roi_bot > h) continue; // 检查边界
        Mat roi = blur(Range(roi_top, roi_bot), Range::all());
        
        imshow("roi", roi);
        
        Canny(roi, edges, 50, 150);

        Point all_points[MAX_POINTS];
        int total = 0;

        int w1 = w / 3;
        int w2 = 2 * w / 3;

        Mat left = edges(Range::all(), Range(0, w1));
        total += get_edge_points(left, roi_top, 0, all_points + total);

        Mat mid = edges(Range::all(), Range(w1, w2));
        total += get_edge_points(mid, roi_top, w1, all_points + total);

        Mat right = edges(Range::all(), Range(w2, w));
        total += get_edge_points(right, roi_top, w2, all_points + total);
        
        
        if (total < 2) {
            printf("警告：未检测到足够的边缘点用于拟合，跳过此帧\n");
            imshow("Line Fitting", img);
            if (waitKey(1) == 27) break;
            continue;
        }


        float k, b;
        ransac_fit(all_points, total, &k, &b);

        float y_left = k * w1 + b;
        float y_right = k * w2 + b;
        float gap = fabs(y_right - y_left);

        printf("斜率 k = %.4f, 中间间距 = %.2f 像素\n", k, gap);

        Mat out_img = img.clone();
        Point pt1(0, (int)(b));
        Point pt2(w, (int)(k * w + b));
        line(out_img, pt1, pt2, Scalar(0, 255, 0), 2);
        //打印所有点
        // 可视化所有拟合点（红色小圆点）
        for (int i = 0; i < total; i++) {
            circle(out_img, all_points[i], 2, Scalar(0, 0, 255), -1); // 红色
        }
        imshow("Line Fitting", out_img);
        if (waitKey(1) == 27) break; // 按 ESC 退出
    }

    cap.release();
    destroyAllWindows();
    return 0;
}
