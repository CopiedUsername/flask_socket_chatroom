import os

from flask import Flask, render_template, request, redirect, url_for
import atexit
import subprocess as sp
import asyncio
import itertools
import json
import socket

app = Flask(__name__)
messages = []
# server = sp.Popen('python /app/server.py')
print("Server started!")
IP = socket.gethostbyname(socket.gethostname())

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():  # put application's code here

    if request.method == 'GET':
        return render_template('chatroom.html', messages=messages)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("main.html")
    else:
        type = request.form.get('type')
        roomID = request.form.get('ID')
        username = request.form.get('username')
        return render_template('chatroom.html', name=username, ID=roomID, type=type, IP=IP)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)
