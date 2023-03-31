# parallel_dual_nvenc_transcoding
Simple script to convert videos throught ffmpeg using two NVENC transcoder in parallel

GTX980 (GM204) owns 2 Nvidia encoders NVENC
The GPU is not powerful enought to process two resizing conversion simultaneously alone
The Python script start two batch conversion, both use the NVENC for encoding but one
use CPU for resizing while the other uses GPU
VideoIN directory contains the file that will be processed to VideoOUT via a queue

## How to
1. Place the script wherever you like
2. Edit script settings and edit inputDIR variable to point to the input folder
3. Or start the script, it will create a new folder where you can put the videos
4. Done, the script will run two istances of ffmpeg until all videos are converted
