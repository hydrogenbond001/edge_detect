import cv2
import os

def extract_frames(video_path, start_frame, end_frame, frame_interval, output_dir):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # 获取总帧数
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if start_frame < 0 or start_frame >= end_frame:
        print("Error: Invalid frame range.")
        return

    current_frame = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检查是否在指定帧范围内
        if current_frame >= start_frame and current_frame <= end_frame:
            # 如果当前帧符合间隔条件，则保存图像
            if current_frame % frame_interval == 0:
                output_filename = os.path.join(output_dir, f"frame_{current_frame}.jpg")
                cv2.imwrite(output_filename, frame)
                print(f"Saved: {output_filename}")

        current_frame += 1

    cap.release()

if __name__ == "__main__":
    video_path = "C:/Users/L3101/Pictures/Camera Roll/WIN_20241023_13_46_00_Pro.mp4"  # 视频路径
    output_dir = "C:/Users/L3101/Pictures/Camera Roll/newcut"  # 输出目录
    start_frame = 0  # 起始帧
    end_frame = 2000  # 结束帧
    frame_interval = 5  # 每5帧保存一张

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    extract_frames(video_path, start_frame, end_frame, frame_interval, output_dir)
