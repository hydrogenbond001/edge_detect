import cv2
import os

# 定义视频路径和自建目录名称C:\Users\L3101\Pictures\Camera Roll
video_path = r'C:\Users\L3101\Desktop\8.5_2.mp4'
output_dir = r'C:\Users\L3101\Desktop\8.5_2cut'  # 自定义的目录名称

# 检查并创建自定义目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打开视频文件8.5
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print(f"无法打开视频文件: {video_path}")
else:
    # 定义每隔多少帧保存一次图片
    frame_interval = 2  # 每1帧保存一次
    current_frame = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("视频读取完成或读取出错。")
            break

        # 如果当前帧是我们想要保存的，保存成图片到指定目录
        if current_frame % frame_interval == 0:
            # 使用零填充到5位数，例如: frame_00001.jpg
            image_name = f'{output_dir}/frame85_{current_frame:05d}.jpg'# frame_ frame1_ ...
            cv2.imwrite(image_name, frame)
            print(f'Saved: {image_name}')
        
        current_frame += 1

    cap.release()
    cv2.destroyAllWindows()
