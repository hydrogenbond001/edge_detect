import base64
from pyLoRa import LoRa
import time

# LoRa配置
lora = LoRa(serial_port='COM18', frequency=915000000, tx_power=14, acks=True)

def receive_image(total_packets, packet_size=64):
    """接收图片数据并重组"""
    received_data = [""] * total_packets  # 初始化数据列表
    received_packets = 0

    print("Waiting for packets...")

    while received_packets < total_packets:
        packet = lora.receive_packet()
        if packet:
            try:
                packet_data = packet.decode('utf-8')
                packet_num, data = packet_data.split("|", 1)
                packet_index = int(packet_num.split("/")[0]) - 1

                # 存储数据
                received_data[packet_index] = data
                received_packets += 1
                print(f"Received packet {packet_index + 1}/{total_packets}")
            except Exception as e:
                print(f"Error processing packet: {e}")

    print("All packets received. Reconstructing image...")

    # 将所有数据拼接并解码
    image_data = base64.b64decode("".join(received_data))
    with open("received_image.jpg", "wb") as f:
        f.write(image_data)
    print("Image saved as 'received_image.jpg'.")

if __name__ == "__main__":
    # 假设发送端已告知总包数（可以使用先发包传总包数或其它通信方式）
    total_packets = 100  # 设置预计总包数
    receive_image(total_packets)
