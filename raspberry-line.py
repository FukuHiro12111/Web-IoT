import subprocess
import serial
import traceback
import time
import requests

class USBSerial:
    def __init__(self, path):
        # シリアル通信設定
        try:
            self.serialport = serial.Serial(
                port=path,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.5,
            )
        except serial.SerialException:
            print(traceback.format_exc())
        # 受信バッファ、送信バッファクリア
        self.serialport.reset_input_buffer()
        self.serialport.reset_output_buffer()
        time.sleep(1)
    def send_serial(self, cmd): # データ送信関数
        print("send data : {0}".format(cmd))
        try:
            self.serialport.write((cmd + "\n").encode("utf-8")) # 改行コードを付与　バイナリに変換して送信
        except serial.SerialException:
            print(traceback.format_exc())

    def receive_serial(self): # データ受信関数
        try:
            rcvdata = self.serialport.readline()
        except serial.SerialException:
            print(traceback.format_exc())

        return rcvdata.decode("utf-8").rstrip()  # 受信データを文字列に変換　改行コードを削除

def main():
    # subprocess.check_outputはバイト文字列で出力を返す
    res = subprocess.check_output('ls /dev/ttyACM*', shell=True)
    serialports = res.decode('utf-8').split('\n')

    serials = []
    for serial in serialports:
        if serial != "":
            print(serial)
            serials.append(USBSerial(serial))

    if len(serials) > 0:
        while True:
            for s in serials:
                r = s.receive_serial()
                if (r == ""):
                    break

                print(r)
                
                values = r.split(',')
                if len(values) >= 4:
                    if (values[0] == "2"):
                        url = 'https://maker.ifttt.com/trigger/sample/with/key/bhwfZ7ppAsXib1GR6cEhXX'
                        
                        payload = {
                            'value1': values[1],
                            'value2': values[2],
                            'value3': values[3],
                        }
                        
                        requests.post(url, params=payload)
                        
                        print('送信しました')


            time.sleep(0.2)

main()