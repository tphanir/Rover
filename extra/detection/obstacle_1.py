#!/usr/bin/env python3

import sys
import argparse
import pyrealsense2 as rs
import numpy as np
from jetson_inference import detectNet
from jetson_utils import cudaFromNumpy, videoOutput, Log

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in RealSense camera frames using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream (e.g., 'display://0')")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g., --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
    args = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

# initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

# create video output
output = videoOutput(args.output, argv=sys.argv)

# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

try:
    while True:
        # wait for a new set of frames from the camera
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        if not color_frame:
            continue

        # Convert RealSense frame to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Convert numpy array to CUDA image
        cuda_image = cudaFromNumpy(color_image)

        # detect objects in the CUDA image (with overlay)
        detections = net.Detect(cuda_image, overlay=args.overlay)

        # print the detections
        print("Detected {:d} objects in image".format(len(detections)))

        for detection in detections:
            print(detection)

        # render the CUDA image
        output.Render(cuda_image)

        # update the title bar
        output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

        # print out performance info
        net.PrintProfilerTimes()

        # exit if the output stops streaming
        if not output.IsStreaming():
            break

finally:
    # Stop RealSense pipeline on exit
    pipeline.stop()
