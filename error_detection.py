#!/usr/bin/python3
import time
import os
import glob
from MOTOR_CTL import MOTOR_CTL
duty = 75
CTL = MOTOR_CTL()

def cal_error():  
    home_dir = '/home/takahiro/yolov5/runs/detect/*'
    labels = '/labels/*'
    max_acc = 0
    max_num = 0
    list_of_files = glob.glob(home_dir) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    exp_files = latest_file+ labels
    exp_latest = glob.glob(exp_files)
    if exp_latest != []:
        exp_txt = max(exp_latest,key=os.path.getatime)
        txt_file = open(exp_txt,'r')
        txt_list = []
        data_list = txt_file.readlines()
        for i in range(len(data_list)):
            txt_list.append(data_list[i].split())
        for j in range(len(txt_list)):
            txt_j = float(txt_list[j][5])
            if max_acc < txt_j:
                max_acc = txt_j
                max_num = j
        x = float(txt_list[max_num][1]) - 0.5

    else:
        x = "Nondetect"
    return x

def main():
    stop_file = "/home/takahiro/Desktop/Codes/gogoJetson/stop_flag/*"
    turn_flag = 0 # 0:NoTurn 1:Left Turn 2:Right Turn
    th = 0.2 # yoloの閾値
    stop_flag = 0
    try:
        time.sleep(60) #スリープ時間要調整
        CTL.set_STBY(1)
        CTL.set_direction(1)
        print("初期 直進")
        CTL.accORdec("AB",duty,"acc")
        while True:
            print("whileに入ったよ")
            time.sleep(3) #スリープ時間要調整
            print("-----")
            yolo_data = cal_error()
            if cal_error() == "Nondetect": # 検出できなかった（ファイルが生成されなかった）らブレイク
                print("検出できません。")
                pass
            else:
                if turn_flag == 0:#直前の動作が直進であった場合
                    if yolo_data < 0:# 誤差がマイナスであれば、左用の、プラスであれば右用の処理
                        if -yolo_data > th:#誤差が閾値以上ある場合、左ターンを行う
                            print("左に方向変更")
                            CTL.turn("l",25)
                            turn_flag = 1
                        else:#誤差が閾値以下であればそのまま直進
                            print("直進継続")
                            CTL.accORdec("AB",duty,"acc")
                    elif yolo_data > 0:# 誤差がプラスであれば右用の処理
                        if yolo_data > th:#誤差が閾値以上ある場合、右ターンを行う
                            print("右に方向変更")
                            CTL.turn("r",25)
                            turn_flag = 2
                        else:#誤差が閾値以下であればそのまま直進
                            print('直進継続')
                            CTL.accORdec("AB",duty,"acc")
                            
                # ターンでwhileに入ってきた場合
                else: #直前にターンをしていた場合
                    if abs(yolo_data) <= th: #誤差が閾値以下の場合
                        print('ターン終了')
                        CTL.fin_turn()
                        CTL.accORdec("AB",duty,"acc")
                        turn_flag = 0
                    
                    elif turn_flag == 1: #直前に左ターンをしていた場合
                        if yolo_data < 0: # 誤差がマイナスであれば、左用の、プラスであれば右用の処理
                            if -yolo_data > th: #誤差が閾値以上ある場合、左ターンを継続
                                print("左ターン継続")
                                time.sleep(1)
                                turn_flag = 1
                            else:#誤差が閾値以下であればそのまま直進
                                print("左ターン終了 直進に移行")
                                CTL.fin_turn()
                                CTL.accORdec("AB",duty,"acc")
                                turn_flag = 0
                        elif yolo_data > 0: # 誤差がプラスであれば右用の処理
                            if yolo_data > th: # 誤差が閾値以上ある場合、右ターンを行う
                                print("右に方向変更")
                                CTL.fin_turn()
                                CTL.turn("r",25)
                                turn_flag = 2
                            else:#誤差が閾値以下であればそのまま直進
                                print('右に曲がる必要なし（閾値内）- 直進します')
                                CTL.fin_turn()
                                CTL.accORdec("AB",duty,"acc")
                                turn_flag = 0
                
                    elif turn_flag == 2: #直前に右ターンをしていた場合
                        if yolo_data < 0: # 誤差がマイナスであれば、左用の処理
                            if -yolo_data > th: #誤差が閾値以上ある場合、左ターンを行う
                                print("左に方向変更")
                                CTL.fin_turn()
                                CTL.turn("l",25)
                                turn_flag = 1
                            else:#誤差が閾値以下であればそのまま直進
                                print("直進")
                                CTL.fin_turn()
                                CTL.accORdec("AB",duty,"acc")
                        elif yolo_data > 0:# 誤差がプラスであれば右用の処理
                            if yolo_data > th:# 誤差が閾値以上ある場合、右ターンを行う
                                print("右ターン継続")
                                time.sleep(1)
                                turn_flag = 2
                            else:#誤差が閾値以下であればそのまま直進
                                print('右ターン終了 直進へ移行')
                                CTL.fin_turn()
                                CTL.accORdec("AB",duty,"acc")
                    else:
                        pass
                    
            stop_flag = glob.glob(stop_file)
            if stop_flag != []:
                print("ストップ")
                break
                    
    finally:
        print("終わっちゃった。。。")
        CTL.close_CTL()
        pass


if __name__ == '__main__':
    main()

