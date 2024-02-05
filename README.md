# parallel_dual_nvenc_transcoding
Simple script to convert videos throught ffmpeg using two NVENC transcoder in parallel

My GTX980 (GM204) owns 2 Nvidia encoders NVENC but it is not powerful enought to process two resizing conversion simultaneously without performance degradation.

The Python script start two batch conversion, both use the NVENC for encoding but one of them
uses CPU for resizing while the other uses GPU

VideoIN directory contains the files that will be processed to VideoOUT via a queue

## Requirements

- `ffmpeg` installed

## How to
1. Place the script wherever you like
2. Put the videos whetever you like
3. Edit settings in script (dirs, quality, ecc)
4. Start the script
5. Done, the script will run two istances of ffmpeg until all videos are converted

## To Do list
- [ ] Implement logging
- [ ] Report time passed to convert each video
- [x] Use path lib instead of strings
- [X] Paths need to be in settings structure
- [X] Better handling of args
