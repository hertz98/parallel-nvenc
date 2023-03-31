import os
import sys
import pathlib
import subprocess

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable) + '\\'
elif __file__:
    application_path = os.path.dirname(__file__) + '\\'


inputDIR = application_path + "\chainB\\"
outputDIR = r"D:\Users\barto\OneDrive - University of Pisa\Lezioni\Fisica Generale 1 21-22 Agnese Ciocci"

if not os.path.exists(inputDIR):
        pathlib.Path(inputDIR).mkdir(parents=True, exist_ok=True)
        print("Created folder: " + inputDIR)
        input()

if not os.path.exists(outputDIR):
        pathlib.Path(outputDIR).mkdir(parents=True, exist_ok=True)
        print("Created folder: " + outputDIR)

quality = "36"
scale = "1280:-1"
extension = ".mkv"

for filename in os.listdir(inputDIR):
    inputFILE = inputDIR + "\\" + filename
    outputFILE = outputDIR + "\\" + filename[:-4] + extension
    cmd = ["ffmpeg.exe", "-hide_banner","-y", "-i", inputFILE, "-c:v", "hevc_nvenc",
     "-preset", "medium", "-cq", quality, "-vf", "scale=" + scale, 
     "-c:a", "copy", outputFILE]
    print(" ".join(cmd))
    subprocess.call(cmd, shell=True)

print("\nEnd...")
input()