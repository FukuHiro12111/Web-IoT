"""Import Module"""
import time
import requests
import schedule
import RPi.GPIO as GPIO
import picamera


# ピン番号指定
gpio_led = 17
gpio_sw = 26
# GPIO指定します
GPIO.setmode(GPIO.BCM)
# チャンネルを設定します
GPIO.setup(gpio_sw,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_led,GPIO.OUT)

# 画像が保存されるパス
CAM_DIR ="/home/pi/Web-IoT-/"
camera = picamera.PiCamera()

def line_notify_post():
    """Line Notify Api"""
    # トークンID
    line_notify_token = "V30inRo2W7u9Tvxb7Mfh7r0eqIBZY3FywmDNUa6kEJZ"
    # LINE Notify APIのURL
    line_notify_api = "https://notify-api.line.me/api/notify"
    # Notify URL
    headers = {'Authorization': 'Bearer ' + line_notify_token}

    # 画像が保存されるディレクトリのパス
    # images = "/home/pi/Web-IoT-/"

    # 画像の読み込み
    files = {'imageFile': open(CAM_DIR + "in_fridge.jpg","rb")}

    # message内容
    text = '画像取得'
    payload = {'message': text}

    requests.post(line_notify_api, data=payload, headers=headers, files=files)

# カメラ撮影
def camera_func():
    if GPIO.input(gpio_sw) == 0:
        filename = ("in_fridge") + ".jpeg"
        save_dir_filename = CAM_DIR + filename
        GPIO.output(gpio_led, 1)
        time.sleep(2)
        camera.capture(save_dir_filename)
        GPIO.output(gpio_led, 0)

GPIO.add_event_detect(gpio_sw, GPIO.FALLING, callback=camera_func)
times = ["01:38", "01:39"]
schedule.every().day.at(times[0]).do(line_notify_post)
schedule.every().day.at(times[1]).do(line_notify_post)
try:
    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
