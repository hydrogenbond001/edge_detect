#include <fstream>
#include <iostream>
#include <cstdint>
#include <chrono>
#include "edlines/edlines.h"
#define TEST_EDLINE_WITH_OPENCV_LIB 0
#define TEST_OPENCV_EDLINE 0
#define TEST_EDLINE_WITHOUT_ANY_DEPENDENCIES 1
#if TEST_EDLINE_WITH_OPENCV_LIB
// include opencv to display pics
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#endif
// BMP文件头结构
#pragma pack(push, 1)
typedef struct
{
	unsigned short bfType;
	unsigned int bfSize;
	unsigned short bfReserved1;
	unsigned short bfReserved2;
	unsigned int bfOffBits;

	unsigned int biSize;
	int biWidth;
	int biHeight;
	unsigned short biPlanes;
	unsigned short biBitCount;
	unsigned int biCompression;
	unsigned int biSizeImage;
	int biXPelsPerMeter;
	int biYPelsPerMeter;
	unsigned int biClrUsed;
	unsigned int biClrImportant;
} BMPHeader;
#pragma pack(pop)
#if TEST_OPENCV_EDLINE
#include <opencv2/line_descriptor.hpp>
#endif

#define MAX_LINE_BUFFER_SIZE 500
// define the resolution of image
const int pWidth = 1024;
const int pHeight = 768;
const int scaleX = 1, scaleY = 1;

std::vector<line_float_t> lines;

unsigned char *pBuf;

using namespace std;

int main()
{
#if TEST_EDLINE_WITHOUT_ANY_DEPENDENCIES
	pBuf = (unsigned char *)malloc(pWidth * pHeight * sizeof(unsigned char));
	line_float_t *lBuf = (line_float_t *)malloc(MAX_LINE_BUFFER_SIZE);
	FILE *infile = fopen("pics/2019-05-06_10-55-52_00016509.bmp", "rb");
	FILE *outfile = fopen("test.bmp", "wb");

	if (infile == NULL)
	{ // Check if file open was successful
		printf("File cannot be opened.\n");
	}

	boundingbox_t bbox = {0, 0, pWidth, pHeight};
	int64_t cycle_us = 1e6 / 34;
	auto start = std::chrono::high_resolution_clock::now();
	int flag = EdgeDrawingLineDetector(pBuf, pWidth, pHeight, 1.0, 1.0, bbox, lBuf);
	auto elapsed_0 = std::chrono::high_resolution_clock::now() - start;
	int64_t microseconds_0 = std::chrono::duration_cast<std::chrono::microseconds>(elapsed_0).count();
	cout << "line detect runtime:" << microseconds_0 / 1000.0 << "ms " << endl;

	// 0:ok; 1:error;
	printf("Succeed: %d\n", !flag);

	// 5. 在内存中绘制线段（白色线段）
	for (int i = 0; i < MAX_LINE_BUFFER_SIZE; i++)
	{
		if (lBuf[i].startx == 0 && lBuf[i].starty == 0 &&
			lBuf[i].endx == 0 && lBuf[i].endy == 0)
			break;

		// 简单的Bresenham画线算法实现
		int x0 = lBuf[i].startx, y0 = lBuf[i].starty;
		int x1 = lBuf[i].endx, y1 = lBuf[i].endy;

		int dx = abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
		int dy = -abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
		int err = dx + dy, e2;

		while (1)
		{
			if (x0 >= 0 && x0 < pWidth && y0 >= 0 && y0 < pHeight)
			{
				pBuf[y0 * pWidth + x0] = 255; // 设为白色
			}
			if (x0 == x1 && y0 == y1)
				break;
			e2 = 2 * err;
			if (e2 >= dy)
			{
				err += dy;
				x0 += sx;
			}
			if (e2 <= dx)
			{
				err += dx;
				y0 += sy;
			}
		}
	}

	// 6. 保存为BMP
	// FILE *outfile = fopen("pics/test.bmp", "wb");
	if (outfile == NULL)
	{
		perror("Error creating output file");
		free(pBuf);
		free(lBuf);
		fclose(infile);
		return -1;
	}

	// 构造BMP头
	BMPHeader header;
	memset(&header, 0, sizeof(BMPHeader));
	header.bfType = 0x4D42;
	header.bfSize = sizeof(BMPHeader) + pWidth * pHeight;
	header.bfOffBits = sizeof(BMPHeader);
	header.biSize = 40;
	header.biWidth = pWidth;
	header.biHeight = pHeight;
	header.biPlanes = 1;
	header.biBitCount = 8;
	header.biSizeImage = pWidth * pHeight;

	// 写入头和像素数据
	fwrite(&header, 1, sizeof(BMPHeader), outfile);
	fwrite(pBuf, 1, pWidth * pHeight, outfile);

	// 7. 清理资源
	free(pBuf);
	free(lBuf);
	fclose(infile);
	fclose(outfile);

	std::cout << "Result saved to test.bmp" << std::endl;
	// free(pBuf);
	// fclose(infile);
	// 如果不使用opencv库，目前不使用其他库对图像进行修改,outfile为空。
	// 你可以打印pBuf查看直线信息
	// fclose(outfile);

#elif TEST_EDLINE_WITH_OPENCV_LIB
	/* 用opencv测试 */
	cv::Mat image;
	image = cv::imread("pics/2019-05-06_10-55-52_00016518.bmp");
	// cv::cvtColor(image, gray_image, CV_BGR2GRAY);
	int W = image.cols * 0.5;
	int H = image.rows * 0.5;
	int image_size = W * H;
	// resize
	unsigned char *input = new unsigned char[image_size];
	cv::Mat temp;
	cv::resize(image, temp, cv::Size(image.cols * 0.5, image.rows * 0.5));
	// 3->1 channel
	cv::Mat img_hsv[3];
	cv::split(temp, img_hsv);
	cv::Mat img_raw_ = img_hsv[2] /* - img_hsv[1] + img_hsv[0]*/;
	// init params
	memcpy(input, img_raw_.data, image_size);
	std::vector<line_float_t> Lines;
	// 左上角是坐标原点
	// 用法和cv::rect一样
	boundingbox_t Bbox = {0, 100, W, H - 100};
	float scalex = 1.0;
	float scaley = 1.0;
	int Flag = 0;
	// Run Edline

	LineDescriptor *ld = new LineDescriptor;
	LineSet Lineset;

	// unsigned char* input = new unsigned char[image_size];
	image_int8u_p int8u_image = new image_int8u_s[1];
	int8u_image->data = input;
	int8u_image->xsize = W;
	int8u_image->ysize = H;
	ld->Run(1, 1, Bbox, int8u_image, Lineset);
	for (int i = 0; i < Lineset.size(); i++)
	{
		cv::line(temp, cv::Point(Lineset[i].startPointX, Lineset[i].startPointY), cv::Point(Lineset[i].endPointX, Lineset[i].endPointY), cv::Scalar(0, 0, 255), 2);
	}
	cv::imshow("image1", temp);
	int64_t cycle_us = 1e6 / 34;
	auto start = std::chrono::high_resolution_clock::now();
	line_float_t lines_buf[MAX_LINE_BUFFER_SIZE] = {0, 0, 0, 0}; /*[MAX_LINE_BUFFER_SIZE];*/
	Flag = EdgeDrawingLineDetector(input, W, H, scalex, scaley, Bbox, lines_buf);
	auto elapsed_0 = std::chrono::high_resolution_clock::now() - start;
	int64_t microseconds_0 = std::chrono::duration_cast<std::chrono::microseconds>(elapsed_0).count();
	cout << "detect:" << microseconds_0 / 1000.0 << "ms " << endl;
	auto bd = cv::line_descriptor::BinaryDescriptor::createBinaryDescriptor();
	std::vector<cv::line_descriptor::KeyLine> lines;
	auto roi_vp = cv::Rect(0, 100, W, H - 100);
	cv::Mat mask_vp_ = cv::Mat::zeros(H, W, CV_8UC1);
	mask_vp_(roi_vp).setTo(255);

	cv::Mat mask = /*mask_ar_ &*/ mask_vp_;
	cv::Mat src_roi(img_raw_.size(), CV_8UC1, cv::Scalar(0));

	img_raw_.copyTo(src_roi, mask);
	elapsed_0 = std::chrono::high_resolution_clock::now() - start;
	bd->detect(src_roi, lines, mask);
	microseconds_0 = std::chrono::duration_cast<std::chrono::microseconds>(elapsed_0).count();
	cout << "OPENCV detect:" << microseconds_0 / 1000.0 << "ms " << endl;

	std::cout << Flag << std::endl;

	cv::Mat temp1;
	temp.copyTo(temp1);
	for (int i = 0; i < lines.size(); i++)
	{
		cv::line(temp1, cv::Point(lines[i].startPointX, lines[i].startPointY), cv::Point(lines[i].endPointX, lines[i].endPointY), cv::Scalar(0, 0, 255), 2);
	}
	cv::imshow("image opencv", temp1);

	for (int i = 0; i < sizeof(lines_buf) / sizeof(line_float_t); i++)
	{
		cv::line(temp, cv::Point(lines_buf[i].startx, lines_buf[i].starty), cv::Point(lines_buf[i].endx, lines_buf[i].endy), cv::Scalar(0, 0, 255), 2);
	}
	cv::imshow("image1", temp);
	cv::waitKey(0);
#endif

	return 0;
}