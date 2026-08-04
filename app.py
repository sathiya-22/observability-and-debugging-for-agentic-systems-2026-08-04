import json
import os
import time
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "agent_events.log"
_thread = None
_thread_stop_event = False

@app.route('/')
def index():
    return render_template('index.html')

def follow_log_file():
    """
    Reads the log file from the beginning and then continuously monitors it
    for new lines, emitting them via SocketIO.
    """
    global _thread_stop_event
    print(f"Monitoring log file: {LOG_FILE}")
    
    # Wait for the file to be created if it doesn't exist yet
    while not os.path.exists(LOG_FILE) and not _thread_stop_event:
        time.sleep(0.5)

    with open(LOG_FILE, 'r') as f:
        # Emit all existing lines first
        for line in f:
            if _thread_stop_event:
                break
            try:
                event = json.loads(line)
                socketio.emit('new_log_event', event, namespace='/')
            except json.JSONDecodeError:
                print(f"Skipping malformed log line: {line.strip()}")
            socketio.sleep(0.01) # Small sleep to allow client to process

        # Then monitor for new lines
        while not _thread_stop_event:
            line = f.readline()
            if not line:
                socketio.sleep(0.1) # Wait for new data
                continue
            try:
                event = json.loads(line)
                socketio.emit('new_log_event', event, namespace='/')
            except json.JSONDecodeError:
                print(f"Skipping malformed log line: {line.strip()}")

@socketio.on('connect')
def test_connect():
    global _thread
    print('Client connected')
    if _thread is None:
        _thread = socketio.start_background_task(follow_log_file)
    emit('status', {'msg': 'Connected to log stream'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print("Starting Agent Log Viewer. Go to http://127.0.0.1:5000")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True) # allow_unsafe_werkzeug for auto-reload with background thread
