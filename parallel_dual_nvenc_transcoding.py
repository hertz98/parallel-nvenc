import os
import queue
import sys
from pathlib import Path
import subprocess
from subprocess import CREATE_NEW_CONSOLE, STDOUT, Popen, PIPE
import threading
import time
import logging
from datetime import datetime

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable) + '\\'
elif __file__:
    application_path = os.path.dirname(__file__) + '\\'

inputDIR = Path("videoIN")
outputDIR = Path("videoOUT")

settings = {
    "quality" : "36",
    "scale" : "1280:-1",
    "inputExt" : "mp4",
    "outputExt" : "mkv"
}

hw_cmd = "ffmpeg -y -hide_banner -hwaccel cuda -hwaccel_output_format cuda -i -c:v hevc_nvenc -preset medium -cq -vf scale_cuda= -c:a copy"
sw_cmd = "ffmpeg -y -hide_banner -i -c:v hevc_nvenc -preset medium -cq -vf scale= -c:a copy"

q = queue.Queue()

def transcode(hwEnc):
    while True:
        if q.empty():
            return
        item = q.get()
        cmd = None
        if hwEnc:
            cmd = hw_cmd
        else:
            cmd = sw_cmd

        cmd = cmd.split(" ") #Creo lista per subprocess

        cmd.insert(cmd.index('-i') + 1,  str( item.absolute() ))
        cmd.append( str( outputDIR.joinpath(item.stem + '.' + settings["outputExt"] ).absolute() ))
        print()
        
        SW_HIDE = 0
        SW_MINIMIZE = 6
        print(" ".join(cmd))
        try:
            process = subprocess.check_call(cmd, 
                            creationflags= CREATE_NEW_CONSOLE, 
                            startupinfo= subprocess.STARTUPINFO(dwFlags=1, wShowWindow=SW_MINIMIZE),
                            )
        except Exception as e:
            print(e)
            # input(e)
        q.task_done()

def main():

    if not inputDIR.exists():
        inputDIR.mkdir(parents=True, exist_ok=True)
        input("Created folder: " + inputDIR.name + "\nWaiting for input")

    outputDIR.mkdir(parents=True, exist_ok=True)

    global hw_cmd, sw_cmd 
    hw_cmd = hw_cmd.replace("-cq", "-cq " + settings["quality"]).replace("scale_cuda=", "scale_cuda=" + settings["scale"])
    sw_cmd = sw_cmd.replace("-cq", "-cq " + settings["quality"]).replace("scale=", "scale=" + settings["scale"])

    for file in inputDIR.rglob("*." + settings["inputExt"]):
        q.put(file)

    t1 = time.time()
    startTime = datetime.now()

    threading.Thread(target=transcode, daemon=True, args=(0,)).start()
    threading.Thread(target=transcode, daemon=True, args=(1,)).start()
    q.join()

    print("\n")
    print(f"Job started at: {startTime}")
    print(f"Time elapsed: {round(time.time() - t1, 2)} seconds")
    input()
    quit()

if __name__ == "__main__":
    main()