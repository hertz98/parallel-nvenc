import os
import queue
import sys
import pathlib
import subprocess
import threading
import time
from datetime import datetime

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable) + '\\'
elif __file__:
    application_path = os.path.dirname(__file__) + '\\'

inputDIR = r".\videoIN"
outputDIR = r".\videoOUT"

if not inputDIR[:1].isalpha():
    if inputDIR[:1] == ".":
        inputDIR = inputDIR[1:]
    inputDIR = application_path + inputDIR

if not outputDIR[:1].isalpha():
    if outputDIR[:1] == ".":
        outputDIR = outputDIR[1:]
    outputDIR = application_path + outputDIR

#inputDIR = r"C:\..."
#outputDIR = r"C:\..."

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
        cmd.insert(cmd.index('-i') + 1, inputDIR + "\\" + item) 
        cmd.append(outputDIR + "\\" + item[ : -len(settings["inputExt"]) ] + settings["outputExt"])
        print()
        #print(cmd)

        print(" ".join(cmd))
        subprocess.call(cmd)
        q.task_done()

def main():

    if not os.path.exists(inputDIR):
            pathlib.Path(inputDIR).mkdir(parents=True, exist_ok=True)
            print("Created folder: " + inputDIR + "\nWaiting for input")
            input()

    if not os.path.exists(outputDIR):
            pathlib.Path(outputDIR).mkdir(parents=True, exist_ok=True)
            print("Created folder: " + outputDIR)

    global hw_cmd, sw_cmd 
    hw_cmd = hw_cmd.replace("-cq", "-cq " + settings["quality"]).replace("scale_cuda=", "scale_cuda=" + settings["scale"])
    sw_cmd = sw_cmd.replace("-cq", "-cq " + settings["quality"]).replace("scale=", "scale=" + settings["scale"])

    for filenames in os.listdir(inputDIR):
        if filenames[-len(settings["inputExt"]) : ] != settings["inputExt"]:
            continue
        q.put(filenames)

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