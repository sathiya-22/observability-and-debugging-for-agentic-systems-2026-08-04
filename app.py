import json
import os
import time
from threading import Thread, Event
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "agent_events.log"
_thread = None
_thread_stop_event = Event() # Use threading.Event for safer stop signaling

@app.route('/')
def index():
    return render_template('index.html')

def follow_log_file():
    """
    Reads the log file from the beginning and then continuously monitors it
    for new lines, emitting them via SocketIO.
    """
    print(f"Monitoring log file: {LOG_FILE}")
    
    # Wait for the file to be created if it doesn't exist yet
    while not os.path.exists(LOG_FILE) and not _thread_stop_event.is_set():
        time.sleep(0.5)

    # If the thread was stopped while waiting for file, exit
    if _thread_stop_event.is_set():
        print("Log file monitoring stopped before file was found.")
        return

    with open(LOG_FILE, 'r') as f:
        # Emit all existing lines first
        for line in f:
            if _thread_stop_event.is_set():
                break
            try:
                event = json.loads(line)
                socketio.emit('new_log_event', event, namespace='/')
            except json.JSONDecodeError:
                print(f"Skipping malformed log line: {line.strip()}")
            socketio.sleep(0.01) # Small sleep to allow client to process

        # Then monitor for new lines
        while not _thread_stop_event.is_set():
            line = f.readline()
            if not line:
                socketio.sleep(0.1) # Wait for new data
                continue
            try:
                event = json.loads(line)
                socketio.emit('new_log_event', event, namespace='/')
            except json.JSONDecodeError:
                print(f"Skipping malformed log line: {line.strip()}")
    print("Log file monitoring thread exited.")


@socketio.on('connect')
def test_connect():
    global _thread
    print('Client connected')
    if _thread is None or not _thread.is_alive():
        _thread_stop_event.clear() # Clear stop event for a new run
        _thread = socketio.start_background_task(follow_log_file)
    emit('status', {'msg': 'Connected to log stream'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    # No need to stop the thread on disconnect, as other clients might still be connected
    # or the same client might reconnect. The thread will continue monitoring.

if __name__ == '__main__':
    print("Starting Agent Log Viewer. Go to http://127.0.0.1:5000")
    try:
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True) # allow_unsafe_werkzeug for auto-reload with background thread
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        _thread_stop_event.set() # Signal the background thread to stop
        if _thread and _thread.is_alive():
            _thread.join(timeout=1) # Give the thread a moment to clean up
            if _thread.is_alive():
                print("Warning: Background thread did not terminate gracefully.")
