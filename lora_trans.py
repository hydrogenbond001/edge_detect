import base64
from PIL import Image
from io import BytesIO
import time
import serial  # 串口通讯
from pyLoRa import LoRa

# LoRa配置
lora = LoRa(serial_port='COM7', frequency=915000000, tx_power=14, acks=True)

def compress_image(image_path, quality=20):
    """压缩图片为低质量以便传输"""
    image = Image.open(image_path)
    output = BytesIO()
    image.save(output, format="JPEG", quality=quality)
    return output.getvalue()

def send_image(image_data, packet_size=64):
    """分包发送图片数据"""
    # 对图片数据进行Base64编码
    encoded_data = base64.b64encode(image_data).decode('utf-8')
    total_packets = len(encoded_data) // packet_size + 1

    print(f"Starting transmission: {total_packets} packets to be sent.")

    for i in range(total_packets):
        start_index = i * packet_size
        end_index = start_index + packet_size
        packet = encoded_data[start_index:end_index]

        # 加入包序号和总包数
        packet = f"{i+1}/{total_packets}|" + packet
        lora.send_packet(packet.encode('utf-8'))
        
        print(f"Packet {i+1}/{total_packets} sent.")

        # 可根据需要加入重发机制
        time.sleep(0.1)  # 等待短暂时间，以确保接收端能够接收数据

    print("Transmission complete.")

if __name__ == "__main__":
    image_path = 'image.jpg'  # 指定图片路径
    image_data = compress_image(r"C:\Users\L3101\Pictures\miku.jpg")
    send_image(image_data)
