from flask import request, send_file
#, flash, jsonify, redirect, url_for, Response
from flask import render_template, after_this_request
import subprocess
import os
import re

from webScan import app
#from config import Config

@app.route('/')
def index():
    currentDir = os.getcwd()
    dir=str(os.path.join(os.getcwd(),"scanApp"))
    assert os.path.isdir(dir)
    os.chdir(dir)
    for file in os.listdir(os.getcwd()):
        if file.endswith(".jpg"):
            os.remove(file)

    args = ["tryTwain.exe", "-s"]
    if ("p" in request.args):
        args.append("-p")
        args.append(request.args["p"])
    if ("d" in request.args):
        args.append("-d")
        args.append(request.args["d"])

    proc = subprocess.Popen(args, stdout=subprocess.PIPE) 
    output = str(proc.stdout.read())
    
    pattern  = re.compile(r"\stmp[\w?\d?]+[.]jpg")
    filename = pattern.search(output).group().strip()    
    path = os.path.join(dir, filename)
    
    os.chdir(currentDir)
    if (os.path.exists(path)):
        return send_file(path, as_attachment=True, attachment_filename="scan.jpeg")

