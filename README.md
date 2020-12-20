# カメラによる冷蔵庫の内容物確認システム

Web×IoTハッカソンにて作成  

## 必要な材料
Raspberry Pi Zero W, リードスイッチ, LED, USBカメラ

<br>

## システム概要
1. 冷蔵庫が閉まったときリードスイッチが反応し、LEDが点灯、カメラモジュールで撮影する
2. 指定された時間にカメラで撮影された際椎の画像をLINE Notify APIを用いてLINEに通知する



![alt text](./images/overview.png "システム構成図")