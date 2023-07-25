import base64

your_code = base64.b64encode(b"""
import math
import os
import random
import re
import subprocess as sp
import sys
import time
import tkinter as tk
from tkinter import filedialog


FFMPEG  = os.path.join('C:', 'ffmpeg', 'ffmpeg.exe')
FFPROBE = os.path.join('C:', 'ffmpeg', 'ffprobe.exe')


class Rt:
    video = None
    logo = None
    output_dir = None

    root = None
    
    btn1 = None
    btn2 = None
    btn3 = None

    label = None

def get_video():
    pth = filedialog.askopenfilename()
    if not pth.lower().endswith(('.mp4', '.mov', '.avi')):
        sys.exit(1)
    Rt.video = pth
    Rt.btn1.config(state=tk.DISABLED)
    Rt.btn2.config(state=tk.NORMAL)

def get_logo():
    pth = filedialog.askopenfilename()
    if not pth.lower().endswith(('.jpg', '.png', '.jpeg')):
        sys.exit(1)
    Rt.logo = pth
    Rt.btn2.config(state=tk.DISABLED)
    Rt.btn3.config(state=tk.NORMAL)

def get_output_dir():
    Rt.output_dir = filedialog.askdirectory()
    Rt.btn3.config(state=tk.DISABLED)
    render()

def get_dur(pth):
    stdout = sp.check_output(
        [
            FFPROBE, '-v', 'error',
            '-select_streams', 'v',
            '-of', 'csv=p=0',
            '-show_entries', 'stream=duration',
            pth
        ],
        stderr=sp.STDOUT, text=True
    )
    res = re.match(r'^(?P<dur>\d+(?:\.\d+)?)', stdout)
    return float(res.group('dur'))

def show_text(text):
    Rt.label.config(text=text)
    Rt.root.update()

def render():

    vdur = get_dur(Rt.video)
    n_out = math.ceil(vdur/55)

    filter_complex = (
        '[1:v]scale=720:-1[v1] ;'
        '[2:v]scale=600:-1[v2] ;'
        '[0:v][v1]overlay=(W-w)/2:(H-h)/2[v3] ;'
        '[v3][v2]overlay=(W-w)/2:(H-h)*0.13[out_v]'
    )

    anchor_t = 0
    n_done = 0
    while True:
        time.sleep(0.005)  # Guard
        show_text(f'Loading... ({round(100*n_done/n_out)}%)')
        curr_dur = min(vdur-anchor_t, 55)

        QUALITY = '24'
        cmd = [
            FFMPEG,
            '-v', 'error',
            '-hwaccel', 'auto',
            '-f', 'lavfi', '-i', f'color=s=720x1280:c=0x000000:d={curr_dur}:r=30',
            '-ss', str(anchor_t), '-t', str(curr_dur), '-i', Rt.video,
            '-t', str(curr_dur), '-i', Rt.logo,
            '-filter_complex', filter_complex,
            '-map', '[out_v]',
            '-map', '1:a',
            '-c:v', 'h264_nvenc',
            '-qp', QUALITY,
            '-r', '30',
            os.path.join(Rt.output_dir, f'vid-{str(int(time.time())).zfill(13)}-{"".join(random.choices("abcdef", k=13))}.mp4')
        ]
        # print(repr(' '.join(cmd)))
        # if input('Continue? ') == 'n': sys.exit(1)
        code = sp.call(cmd)
        if code != 0: sys.exit(1)

        anchor_t += curr_dur
        n_done += 1
        if n_done == n_out: break

    ## Finished
    sp.run(['explorer', os.path.abspath(Rt.output_dir)], shell=True)
    sys.exit(1)


def main():

    root = tk.Tk()
    root.title('app_1')
    root.iconbitmap(None)
    root.geometry('355x230+30+30')
    root.configure(bg='#111')
    Rt.root = root

    X, Y, G = 30, 40, 40
    btn1 = tk.Button(root, width=10, text='Video', command=get_video)
    btn1.place(x=X, y=Y+G*0)
    Rt.btn1 = btn1

    btn2 = tk.Button(root, width=10, text='Logo', command=get_logo, state=tk.DISABLED)
    btn2.place(x=X, y=Y+G*1)
    Rt.btn2 = btn2

    btn3 = tk.Button(root, width=10, text='Save', command=get_output_dir, state=tk.DISABLED)
    btn3.place(x=X, y=Y+G*2)
    Rt.btn3 = btn3

    label = tk.Label(root, text='')
    label.place(x=X, y=Y+G*3+25, anchor='w')
    Rt.label = label

    root.mainloop()


if __name__ == '__main__':
    main()
""")

exec(base64.b64decode(your_code))
