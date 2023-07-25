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


class Rt:
    ffmpeg = None
    ffprobe = None
    video = None
    logo = None
    output_dir = None

    root = None
    
    btn1 = None
    btn2 = None
    btn3 = None
    btn4 = None
    btn5 = None

    label = None

def get_ffmpeg():
    Rt.ffmpeg = filedialog.askopenfilename()
    print(f'ffmpeg: {repr(Rt.ffmpeg)}')
    Rt.btn1.config(state=tk.DISABLED)
    Rt.btn2.config(state=tk.NORMAL)
    show_text('set ffprobe')
    if not Rt.ffmpeg.lower().endswith('ffmpeg.exe'):
        print('invalid ffmpeg')
        Rt.btn2.config(state=tk.DISABLED)

def get_ffprobe():
    Rt.ffprobe = filedialog.askopenfilename()
    print(f'ffprobe: {repr(Rt.ffprobe)}')
    Rt.btn2.config(state=tk.DISABLED)
    Rt.btn3.config(state=tk.NORMAL)
    show_text('set video')
    if not Rt.ffprobe.lower().endswith('ffprobe.exe'):
        print('invalid ffprobe')
        Rt.btn3.config(state=tk.DISABLED)

def get_video():
    pth = filedialog.askopenfilename()
    Rt.video = pth
    print('vid: ', repr(pth))
    Rt.btn3.config(state=tk.DISABLED)
    Rt.btn4.config(state=tk.NORMAL)
    show_text('select logo')
    if not pth.lower().endswith(('.mp4', '.mov', '.avi')):
        print('invalid video')
        Rt.btn4.config(state=tk.DISABLED)

def get_logo():
    pth = filedialog.askopenfilename()
    Rt.logo = pth
    print('logo: ', repr(pth))
    Rt.btn4.config(state=tk.DISABLED)
    Rt.btn5.config(state=tk.NORMAL)
    show_text('select save')
    if not pth.lower().endswith(('.jpg', '.png', '.jpeg')):
        print('invalid logo')
        Rt.btn5.config(state=tk.DISABLED)

def get_output_dir():
    Rt.output_dir = filedialog.askdirectory()
    print('vid: ', repr(Rt.output_dir))
    Rt.btn5.config(state=tk.DISABLED)
    show_text('loading...')
    render()

def get_dur(pth):
    print('xyz', [
            Rt.ffprobe, '-v', 'error',
            '-select_streams', 'v',
            '-of', 'csv=p=0',
            '-show_entries', 'stream=duration',
            pth
        ])
    stdout = sp.check_output(
        [
            Rt.ffprobe, '-v', 'error',
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
    sp.run(['explorer', os.path.abspath(Rt.output_dir)], shell=True)

    vdur = get_dur(Rt.video)
    n_out = math.ceil(vdur/55)
    print(f'vdur: {vdur}  n_out: {n_out}')

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

        cmd = [
            Rt.ffmpeg,
            '-v', 'error', '-stats',
            '-f', 'lavfi', '-i', f'color=s=720x1280:c=0x000000:d={curr_dur}:r=30',
            '-ss', str(anchor_t), '-t', str(curr_dur), '-i', Rt.video,
            '-t', str(curr_dur), '-i', Rt.logo,
            '-filter_complex', filter_complex,
            '-map', '[out_v]',
            '-map', '1:a',
            '-q:v', '21',
            '-r', '30',
            os.path.join(Rt.output_dir, f'vid-{str(int(time.time())).zfill(13)}-{"".join(random.choices("abcdef", k=13))}.mp4')
        ]
        print(repr(' '.join(cmd)))
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
    root.title('app_6')
    root.iconbitmap(None)
    root.geometry('400x330+100+100')
    root.configure(bg='#111')
    Rt.root = root

    X, Y, G = 30, 40, 40
    btn1 = tk.Button(root, width=10, text='ffmpeg', command=get_ffmpeg)
    btn1.place(x=X, y=Y+G*0)
    Rt.btn1 = btn1

    btn2 = tk.Button(root, width=10, text='ffprobe', command=get_ffprobe, state=tk.DISABLED)
    btn2.place(x=X, y=Y+G*1)
    Rt.btn2 = btn2

    btn3 = tk.Button(root, width=10, text='video', command=get_video, state=tk.DISABLED)
    btn3.place(x=X, y=Y+G*2)
    Rt.btn3 = btn3

    btn4 = tk.Button(root, width=10, text='logo', command=get_logo, state=tk.DISABLED)
    btn4.place(x=X, y=Y+G*3)
    Rt.btn4 = btn4

    btn5 = tk.Button(root, width=10, text='save', command=get_output_dir, state=tk.DISABLED)
    btn5.place(x=X, y=Y+G*4)
    Rt.btn5 = btn5

    label = tk.Label(root, text='')
    label.place(x=X, y=Y+G*5+25, anchor='w')
    Rt.label = label

    show_text('set ffmpeg')
    root.mainloop()


if __name__ == '__main__':
    main()
""")

exec(base64.b64decode(your_code))
