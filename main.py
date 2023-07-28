import base64

your_code = base64.b64encode(b"""
import datetime
import json
import math
import os
import random
import re
import subprocess as sp
import sys
import time
import tkinter as tk
from tkinter import filedialog


DO_LOG = True
DO_LOG = False
def log(text):
    if DO_LOG: print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {text}')


class AppDataManager:

    APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'video_maker_9ca449554d06')
    FILE = os.path.join(APP_DATA_DIR, '__ffmpeg_and_ffprobe_loc__.json')

    def app_data_dir_is_found():
        log(f'App data dir {repr(AppDataManager.APP_DATA_DIR)} is {"found" if os.path.isdir(AppDataManager.APP_DATA_DIR) else "not found"}.')
        return os.path.isdir(AppDataManager.APP_DATA_DIR)

    def get_ffmpeg():
        if not (os.path.isfile(AppDataManager.FILE) and AppDataManager.FILE.endswith('.json')): raise AssertionError(f'Invalid {repr(AppDataManager.FILE)}.')
        with open(AppDataManager.FILE, 'r') as f:
            ffmpeg, ffprobe = json.load(f)
            log(f'Loaded ffmpeg : {repr(ffmpeg)}')
            log(f'Loaded ffprobe: {repr(ffprobe)}')
            if (not os.path.isfile(ffmpeg)) or (not os.path.isfile(ffprobe)):
                if (len(os.listdir(AppDataManager.APP_DATA_DIR)) == 1) and (os.listdir(AppDataManager.APP_DATA_DIR)[0] == os.path.basename(AppDataManager.FILE)):
                    log(f'Deleting file {repr(AppDataManager.FILE)}.')
                    os.remove(AppDataManager.FILE)
                    log(f'Deleting dir {repr(AppDataManager.APP_DATA_DIR)}.')
                    os.rmdir(AppDataManager.APP_DATA_DIR)
                raise FileNotFoundError('ffmpeg and/or ffprobe not found.')
        return ffmpeg, ffprobe

    def store(ffmpeg, ffprobe):
        log(f'Creating dir {repr(AppDataManager.APP_DATA_DIR)}.')
        if os.path.exists(AppDataManager.APP_DATA_DIR): raise AssertionError(f'Already exists: {repr(AppDataManager.APP_DATA_DIR)}')
        os.mkdir(AppDataManager.APP_DATA_DIR)

        log(f'Creating file {repr(AppDataManager.FILE)}.')
        if os.path.exists(AppDataManager.FILE): raise AssertionError(f'Already exists: {repr(AppDataManager.FILE)}')
        with open(AppDataManager.FILE, 'w') as f: json.dump([ffmpeg, ffprobe], f)


class Rt:
    ffmpeg = None
    ffprobe = None
    video = None
    logo = None
    logo2 = None
    output_dir = None
    dur = 55

    root = None
    
    btn1 = None
    btn2 = None
    btn3 = None
    btn4 = None
    btn5 = None
    btn6 = None

    label = None
    slider = None

def get_ffmpeg():
    Rt.ffmpeg = filedialog.askopenfilename()
    log(f'Selected ffmpeg: {repr(Rt.ffmpeg)}')
    Rt.btn1.config(state=tk.DISABLED)

    show_text('set ffprobe')
    Rt.btn2.config(state=tk.NORMAL)
    
    if not Rt.ffmpeg.lower().endswith('ffmpeg.exe'):
        show_text('invalid ffmpeg')
        Rt.btn2.config(state=tk.DISABLED)

def get_ffprobe():
    Rt.ffprobe = filedialog.askopenfilename()
    log(f'Selected ffprobe: {repr(Rt.ffprobe)}')
    Rt.btn2.config(state=tk.DISABLED)
    
    show_text('set video')
    Rt.btn3.config(state=tk.NORMAL)
    
    if not Rt.ffprobe.lower().endswith('ffprobe.exe'):
        show_text('invalid ffprobe')
        Rt.btn3.config(state=tk.DISABLED)
        return
    AppDataManager.store(Rt.ffmpeg, Rt.ffprobe)

def get_video():
    Rt.video = filedialog.askopenfilename()
    log(f'Selected vid: {repr(Rt.video)}')
    Rt.btn3.config(state=tk.DISABLED)
    
    show_text('select logo')
    Rt.btn4.config(state=tk.NORMAL)
    
    if not Rt.video.lower().endswith(('.mp4', '.mov', '.avi')):
        show_text('invalid video')
        Rt.btn4.config(state=tk.DISABLED)

def get_logo():
    Rt.logo = filedialog.askopenfilename()
    log(f'Selected logo: {repr(Rt.logo)}')
    Rt.btn4.config(state=tk.DISABLED)
    
    show_text('select logo (down)')
    Rt.btn5.config(state=tk.NORMAL)
    
    if not Rt.logo.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
        show_text('invalid logo')
        Rt.btn5.config(state=tk.DISABLED)

def get_logo2():
    Rt.logo2 = filedialog.askopenfilename()
    log(f'Selected logo2: {repr(Rt.logo2)}')
    Rt.btn5.config(state=tk.DISABLED)
    
    show_text('select save')
    Rt.btn6.config(state=tk.NORMAL)
    
    if not Rt.logo2.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
        show_text('invalid logo (down)')
        Rt.btn6.config(state=tk.DISABLED)

def get_output_dir():
    Rt.output_dir = filedialog.askdirectory()
    log(f'Selected output dir: {repr(Rt.output_dir)}')
    Rt.btn6.config(state=tk.DISABLED)
    Rt.slider.configure(state='disabled')
    show_text('loading...')
    render()

def get_dur(pth):
    cmd = [
        Rt.ffprobe, '-v', 'error',
        '-select_streams', 'v',
        '-of', 'csv=p=0',
        '-show_entries', 'stream=duration',
        pth
    ]
    log(f'cmd: {repr(cmd)}')
    stdout = sp.check_output(cmd, stderr=sp.STDOUT, text=True)
    res = re.match(r'^(?P<dur>\d+(?:\.\d+)?)', stdout)
    return float(res.group('dur'))

def show_text(text):
    Rt.label.config(text=text)
    Rt.root.update()

def render():
    sp.run(['explorer', os.path.abspath(Rt.output_dir)], shell=True)

    vdur = get_dur(Rt.video)
    n_out = math.ceil(vdur/Rt.dur)
    log(f'vdur: {vdur}  n_out: {n_out}')

    filter_complex = (
        '[1:v]scale=720:-1[o1] ;'
        '[2:v]scale=600:-1[o2] ;'
        '[3:v]scale=600:-1[o3] ;'
        '[0:v][o1]overlay=(W-w)/2:(H-h)*0.50[oo1] ;'
        '[oo1][o2]overlay=(W-w)/2:(H-h)*0.13[oo2] ;'
        '[oo2][o3]overlay=(W-w)/2:(H-h)*0.83[out_v]'
    )

    anchor_t = 0
    n_done = 0
    while True:
        time.sleep(0.005)  # Guard
        show_text(f'Loading... ({round(100*n_done/n_out)}%)')
        curr_dur = min(vdur-anchor_t, Rt.dur)

        optional_args = ['-stats'] if DO_LOG else []
        cmd = [
            Rt.ffmpeg,
            '-v', 'error',
            *optional_args,
            '-f', 'lavfi', '-i', f'color=s=720x1280:c=0x000000:d={curr_dur}:r=30',
            '-ss', str(anchor_t), '-t', str(curr_dur), '-i', Rt.video,
            '-t', str(curr_dur), '-stream_loop', '-1', '-i', Rt.logo,
            '-t', str(curr_dur), '-stream_loop', '-1', '-i', Rt.logo2,
            '-filter_complex', filter_complex,
            '-map', '[out_v]',
            '-map', '1:a',
            '-q:v', '5',
            '-r', '30',
            os.path.join(Rt.output_dir, f'vid-{str(int(time.time())).zfill(13)}-{"".join(random.choices("0123456789", k=13))}.mp4')
        ]
        log(repr(' '.join(cmd)))
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
    root.title('app_7')
    root.iconbitmap(None)
    root.geometry('530x410+200+130')
    root.configure(bg='#111')
    Rt.root = root

    btn1 = tk.Button(root, width=10, text='ffmpeg', command=get_ffmpeg)
    Rt.btn1 = btn1

    btn2 = tk.Button(root, width=10, text='ffprobe', command=get_ffprobe, state=tk.DISABLED)
    Rt.btn2 = btn2

    if AppDataManager.app_data_dir_is_found():
        X, Y, G = 30, -40, 40
        Rt.ffmpeg, Rt.ffprobe = AppDataManager.get_ffmpeg()
        btn3lock = tk.NORMAL
        first_set = 'video'
    else:
        X, Y, G = 30, 40, 40
        btn1.place(x=X, y=Y+G*0)
        btn2.place(x=X, y=Y+G*1)
        btn3lock = tk.DISABLED
        first_set = 'ffmpeg'

    btn3 = tk.Button(root, width=10, text='video', command=get_video, state=btn3lock)
    btn3.place(x=X, y=Y+G*2)
    Rt.btn3 = btn3

    btn4 = tk.Button(root, width=10, text='logo (up)', command=get_logo, state=tk.DISABLED)
    btn4.place(x=X, y=Y+G*3)
    Rt.btn4 = btn4

    btn5 = tk.Button(root, width=10, text='logo (down)', command=get_logo2, state=tk.DISABLED)
    btn5.place(x=X+100, y=Y+G*3)
    Rt.btn5 = btn5

    btn6 = tk.Button(root, width=10, text='save', command=get_output_dir, state=tk.DISABLED)
    btn6.place(x=X, y=Y+G*4)
    Rt.btn6 = btn6

    def fn(e):
        Rt.dur = int(slider.get())
        slider.config(label=f'{Rt.dur} seconds/clip')
    slider = tk.Scale(root, from_=5, to=120, orient='horizontal', command=fn, label='55 seconds/clip', length=220)
    slider.place(x=X, y=Y+G*5)
    slider.set(55)
    Rt.slider = slider

    label = tk.Label(root, text='', background='#555', foreground='#ddd')
    label.place(x=X, y=Y+G*7, anchor='w')
    Rt.label = label

    show_text(f'set {first_set}')
    root.bind('<Escape>', lambda e: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    main()
""")

exec(base64.b64decode(your_code))
