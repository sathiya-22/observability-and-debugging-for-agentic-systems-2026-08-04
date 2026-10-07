2026-10-07: Implemented a safer shutdown mechanism for the Flask-SocketIO background thread using `threading.Event` to prevent resource leaks and improve graceful termination.
