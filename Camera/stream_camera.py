#!/usr/bin/env python
import os
from importlib import import_module
from flask import Flask, render_template, Response
import webbrowser
from Detection import detect_branding
from Camera import get_camera_feed

app = Flask("SAS")

host = "localhost"
port = 80


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('Stream.html')


mimetype = 'multipart/x-mixed-replace; boundary=frame'


def gen(camera):
    print("LL")
    """Video streaming generator function."""
    for img1, img2 in detect_branding.captureFrames():
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
        yield img1
        yield b'\r\n\r\n'


def gen1(camera):
    """Video streaming generator function."""
    for img1, img2 in detect_branding.captureFrames():
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
        yield img2
        yield b'\r\n\r\n'


for i in range(get_camera_feed.Streams):
    print(i)
    exec("@app.route(\"/camera"+str(i)+"\")\ndef camera"+str(i) +
         "():return Response(gen(detect_branding.captureFrames()),mimetype=\"multipart/x-mixed-replace; boundary=frame\")")
    exec("@app.route(\"/cameraprocessed"+str(i)+"\")\ndef cameraprocessed"+str(i) +
         "():return Response(gen1(detect_branding.captureFrames()),mimetype=\"multipart/x-mixed-replace; boundary=frame\")")

    # exec("@app.route(\"/camera"+str(i)+"\")\ndef camera"+str(i)+"():return Response(gen(get_camera_feed.Camera" +
    #     str(i)+"()),mimetype=\"multipart/x-mixed-replace; boundary=frame\")")
    # exec("@app.route(\"/cameraprocessed"+str(i)+"\")\ndef cameraprocessed"+str(i) +
    #     "():return Response(gen1(get_camera_feed.Camera"+str(i)+"()),mimetype=\"multipart/x-mixed-replace; boundary=frame\")")


def run():
    app.run(host=host, threaded=True, port=port)


if __name__ == '__main__':
    run()