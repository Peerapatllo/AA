import psutil
import requests
import json
import time
import os
from PIL import ImageGrab
from io import BytesIO
from datetime import datetime, timedelta
import subprocess

def get_computer_online_time():
    boot_time = psutil.boot_time()
    current_time = time.time()
    online_time = current_time - boot_time
    online_time_delta = timedelta(seconds=online_time)
    return str(online_time_delta)

def get_gpu_info():
    output = subprocess.check_output(['nvidia-smi', '--query-gpu=temperature.gpu,utilization.gpu', '--format=csv,noheader,nounits'])
    gpu_info = output.decode().strip().split('\n')[0]
    temperature, utilization = gpu_info.split(', ')
    return temperature, utilization

def send_to_webhook(webhook_url, cpu_usage, ram_usage, gpu_temperature, gpu_usage, screenshot):

    current_time = datetime.utcnow() + timedelta(hours=7)  # Adding 7 hours to get GMT+7
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    online_time = get_computer_online_time()

    embed = {
        #"title": "<a:stockup:1123197731876393010> System Info <a:stockup:1123197731876393010>",
        "color": 10181046,
        #"timestamp": timestamp,
        "description": f"# System Info\nCPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}%\nGPU Temperature: {gpu_temperature}°C\nGPU Usage: {gpu_usage}%\nOnline Time: {online_time}",
        "description": f"# <a:stockup:1123197731876393010> System Info <a:stockup:1123197731876393010>\n<a:Dot:923905792162275368> **CPU Usage :** {cpu_usage}% <:cpu:1064222851583979613>\n<a:Dot:923905792162275368> **RAM Usage :** {ram_usage}% <:memory:1064237280358826104>\n<a:Dot:923905792162275368> **GPU Usage :** {gpu_usage}% <:gpu:1124711907283181760>\n<a:Dot:923905792162275368> **GPU °C :** {gpu_temperature}°C <:tmt:1124711903390863381>\n<a:Dot:923905792162275368> **Time :** {online_time} <a:alarmclock51:1123178554084048896>",
        "image": {
            "url": "attachment://screenshot.png"
        },
        "footer": {
            "text": f"INDYBUX • {timestamp}",
            "icon_url": "https://sv1.picz.in.th/images/2022/12/26/JtcDsz.png"
        }
    }

    files = {
        "payload_json": (None, json.dumps({"embeds": [embed]})),
        "file": ("screenshot.png", screenshot)
    }

    r = requests.post(webhook_url, files=files)
    if r.status_code != 204:
        print(f"Failed to send data: {r.text}")


def take_screenshot():
    return ImageGrab.grab()


def main():
    webhook_url = "https://discord.com/api/webhooks/1123910165314408561/ujul3ccJb6JAApGla-9jEVuDj-IeLo4xOGcWUjU4ap6jMmZeLUFJOB3HGNMcX5MGtatE"
    while True:
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        gpu_temperature, gpu_usage = get_gpu_info()
        screenshot = take_screenshot()
        screenshot_bytes = BytesIO()
        screenshot.save(screenshot_bytes, format="PNG")
        screenshot_bytes.seek(0)
        send_to_webhook(webhook_url, cpu_usage, ram_usage, gpu_temperature, gpu_usage, screenshot_bytes)
        time.sleep(120)
        
if __name__ == "__main__":
    main()
