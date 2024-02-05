import queue
from pathlib import Path
import subprocess
from subprocess import CREATE_NEW_CONSOLE, STDOUT, Popen, PIPE
import threading
import time
import logging
from datetime import datetime

settings = {
    'inputDIR' : Path('videoIN'),
    'outputDIR' : Path('videoOUT'),
    'quality' : '36',
    'scale' : '1280:-1',
    'inputExt' : 'mp4',
    'outputExt' : 'mkv'
}

args = {
    'hw_args' : {
        'ffmpeg' : None,
        '-y' : None,
        '-hide_banner' : None,
        '-hwaccel' : 'cuda',
        '-hwaccel_output_format' : 'cuda',
        '-i' : None,
        '-c:v' : 'hevc_nvenc',
        '-preset' : 'medium',
        '-cq' : settings["quality"],
        '-vf' : None,
        'scale_cuda=' : settings['scale'],
        '-c:a' : 'copy',
        '_OUTPUT' : None
    },
    'sw_args' : {
        'ffmpeg' : None,
        '-y' : None,
        '-hide_banner' : None,
        '-i' : None,
        '-c:v' : 'hevc_nvenc',
        '-preset' : 'medium',
        '-cq' : settings["quality"],
        '-vf' : None,
        'scale=' : settings['scale'],
        '-c:a' : 'copy',
        '_OUTPUT' : None
    },
}

q = queue.Queue()

def transcode(type: str):
    while True:
        if q.empty():
            return
        input = q.get()

        global args
        selArgs = dict(args[type])
        selArgs['-i'] = str( input.absolute() )
        selArgs['_OUTPUT'] = str( settings['outputDIR'].joinpath( input.stem + '.' + settings["outputExt"] ).absolute() )

        print(selArgs['-i'])

        outArgs = []
        for arg, argvalue in selArgs.items():
            if (arg[-1] == '='):
                outArgs.append(arg + argvalue)
                continue
            if arg != None:
                outArgs.append(arg)
            if argvalue != None:
                outArgs.append(argvalue)

        outArgs.remove('_OUTPUT')
        
        windowMode = {
            'SW_HIDE' : 0,
            'SW_NORMAL' : 1,
            'SW_MINIMIZE' : 6
        }
    
        try:
            subprocess.call(outArgs, 
                            creationflags= CREATE_NEW_CONSOLE, 
                            startupinfo= subprocess.STARTUPINFO(dwFlags=1, wShowWindow=windowMode['SW_MINIMIZE']),
                            )
        except Exception as e:
            print(e)

        q.task_done()

def main():

    if not settings['inputDIR'].exists():
        settings['inputDIR'].mkdir(parents=True, exist_ok=True)
        input("Created folder: " + settings['inputDIR'].name + "\nWaiting for input")

    settings['outputDIR'].mkdir(parents=True, exist_ok=True)

    for file in settings['inputDIR'].rglob("*." + settings["inputExt"]):
        q.put(file)

    t1 = time.time()
    startTime = datetime.now()

    threading.Thread(target=transcode, daemon=True, args=('hw_args',)).start()
    threading.Thread(target=transcode, daemon=True, args=('sw_args',)).start()
    q.join()

    print("\n")
    print(f"Job started at: {startTime}")
    print(f"Time elapsed: {round(time.time() - t1, 2)} seconds")
    input()
    quit()

if __name__ == "__main__":
    main()