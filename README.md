HW3 BLE Lab
===

# How to Run Code（For Linux）

## 安裝相關模組
```javascript
// If your Rpi is new
sudo apt update
sudo apt install python3 idle3
sudo apt install python3-pip

// Install required package
sudo apt install libglib2.0-dev
sudo pip3 install bluepy
```

## 執行程式
```javascript
sudo -E python3 {PROGRAM_PATH}
```

# Bluepy

## 相關Python BLE Interfaces
* [Pygattlib](https://github.com/oscaracena/pygattlib)
* [Bluepy](https://github.com/IanHarvey/bluepy)
* [Adafruit Blinka BLE IO](https://github.com/adafruit/Adafruit_Blinka_bleio)

## 相關C BLE Interfaces
* [Gattlib](https://github.com/labapart/gattlib)


# 目標
透過Mobile作為GATT Server，並透過RaspberryPi作為GATT Client來傳送資料、修改Server端的 **CCCD** (Client Characteristic Configuration Descriptor)，可以將CCCD設為Notification、Indication等不同模式，並接收對應的訊息。

# 相關設定

## 設定對應的Attribute

```javascript
# user config
DEVICE_NAME = {裝置名稱}    #僅作為提示
SERVICE_UUID = {對應Service的UUID}
CHAR_UUID = {對應Characteristic的UUID}
```

# 程式流程

1. 初始化對應參數
2. 設定Scanner、Peripheral的Delegate（設定handleNotification...等功能）
3. 掃描附近裝置、連線對應裝置
4. 開啟連線、Device=Peripheral(...)
5. 列出當前Service
6. 取得對應的Characteristic
7. 取得CCCD的Descripter，並進行修改
8. 開始接收來自Server的訊息直到斷開連線

# 程式效果
本次使用Android Mobile中的BLE Tool -> GATT Server
透過Show Log可以看到CCCD已被修改的訊息。
關於IOS可以透過LightBlue作為GATT Server，但無法透過程式修改對應Service的CCCD。