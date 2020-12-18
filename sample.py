"""Import Module"""
import time
import requests
import schedule

def line_notify_post():
    """Line Notify Api"""
    # トークンID
    line_notify_token = "自分のトークンID"
    # LINE Notify APIのURL
    line_notify_api = "https://notify-api.line.me/api/notify"
    # Notify URL
    headers = {'Authorization': 'Bearer ' + line_notify_token}

    # 画像が保存されるディレクトリのパス
    images = "画像が保存されるディレクトリのパス"

    # 画像の読み込み
    files = {'imageFile': open(images + "camera_capture.png","rb")}

    # message内容
    text = '画像取得'
    payload = {'message': text}

    requests.post(line_notify_api, data=payload, headers=headers, files=files)

def designation_time():
    """ 指定した時刻に通知"""
    times = ["21:32", "21:33"]
    schedule.every().day.at(times[0]).do(line_notify_post)
    schedule.every().day.at(times[1]).do(line_notify_post)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    designation_time()
