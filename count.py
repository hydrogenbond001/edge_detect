import os

def count_lines(directory, extensions):
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    total_lines += sum(1 for _ in f)
    return total_lines

directory = r"C:/Users/L3101/Desktop/fsdownload/gongxun_video_code/rknn-cpp-Multithreading-main"
extensions = (".cpp", ".h")
total_lines = count_lines(directory, extensions)
print(f"Total lines of code: {total_lines}")
