"""Import Module"""
import time
import requests
import schedule
import numpy as np
import cv2 as cv
import os
import RPi.GPIO as GPIO


# ピン番号指定
gpio_led = 17
gpio_sw = 26
# GPIO指定します
GPIO.setmode(GPIO.BCM)
# チャンネルを設定します
GPIO.setup(gpio_sw,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_led,GPIO.OUT)

# 画像が保存されるパス
CAM_DIR =""


def line_notify_post():
    """Line Notify Api"""
    # トークンID
    line_notify_token = "自分のトークンID"
    # LINE Notify APIのURL
    line_notify_api = "https://notify-api.line.me/api/notify"
    # Bearer認証
    headers = {'Authorization': 'Bearer ' + line_notify_token}

    # 画像の読み込み
    files = {'imageFile': open(CAM_DIR + "in_fridge.jpg","rb")}

    # message内容
    text = '画像取得'
    payload = {'message': text}

    requests.post(line_notify_api, data=payload, headers=headers, files=files)

# カメラ撮影
def camera_func(x):
    if GPIO.input(gpio_sw) == 0:
        cap = cv.VideoCapture(0)
        filename = ("in_fridge") + ".jpg"
        GPIO.output(gpio_led, 1)
        time.sleep(2)
        ret, frame = cap.read()
        cv.imwrite(os.path.join(CAM_DIR, filename), frame)
        GPIO.output(gpio_led, 0)
        
def main():
    GPIO.add_event_detect(gpio_sw, GPIO.FALLING, callback=camera_func)
    times = ["09:00", "17:30"] # 何時にしても良い
    schedule.every().day.at(times[0]).do(line_notify_post)
    schedule.every().day.at(times[1]).do(line_notify_post)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__=='__main__':
    main()
    

