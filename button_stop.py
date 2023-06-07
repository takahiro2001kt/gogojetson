#!/usr/bin/python3
#import RPi.GPIO as GPIO
import Jetson.GPIO as GPIO
import subprocess
import signal
import time
import os
import shutil

# ボタンに接続されたGPIOピン番号
button_pin = 40

# ステータスファイルのパス
status_file = "status.txt"

# GPIOのセットアップ
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

f = open(status_file,"w")
f.write("0")
f.close

# ファイルがある場合でも中身を書き換える。(1での起動防止)
with open(status_file,"w") as f:
    f.write("0")

print("ファイルの生成, 初期値の設定が完了")

# ボタンが押された時に呼ばれるコールバック関数
def button_callback(channel):
    with open(status_file, "r") as f:
        status = f.read().strip()

    global process

    if status == "0":
        new_status = "1"
        if not os.path.isfile("stop_flag/stop.txt"):
                # ここにプログラム実行するものを記載する
                print("コピーするよん")
                shutil.copyfile("stop/stop.txt", "stop_flag/stop.txt")
                time.sleep(4)
        os.remove("stop_flag/stop.txt")
        print("stopファイルを消去しました。")
    else:
        new_status = "0"

    with open(status_file, "w") as f:
        f.write(new_status)

    print(f"status.txt: {new_status}")

# ボタンのイベント監視を開始
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    # 無限ループでプログラムを実行し続ける
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    # Ctrl+Cが押されたらプログラムを終了
    pass

finally:
    # GPIOピンを解放
    GPIO.cleanup()
