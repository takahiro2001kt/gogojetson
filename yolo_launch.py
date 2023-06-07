#!/usr/bin/python3
import subprocess
 
def act_yolo():
    cmd =  'python3 /home/takahiro/yolov5/detect.py --source 0 --weights /home/takahiro/yolov5/best_BK.pt --save-txt --save-conf --conf 0.1'
    subprocess.call(cmd.split())


def main():
    act_yolo()


if __name__ == '__main__':
    main()
