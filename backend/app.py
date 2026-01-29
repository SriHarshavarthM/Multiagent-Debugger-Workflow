from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend communication
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Import and register routes
from routes.analysis import analysis_bp
from routes.websocket import register_websocket_handlers

app.register_blueprint(analysis_bp, url_prefix='/api')
register_websocket_handlers(socketio)

@app.route('/')
def index():
    return {
        "name": "Multiagent Debugger API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/api/analyze",
            "websocket": "ws://localhost:5000"
        }
    }

@app.route('/health')
def health():
    return {"status": "healthy", "message": "All systems operational"}

if __name__ == '__main__':
    print("🚀 Starting Multiagent Debugger Backend...")
    print("📡 API running on http://localhost:5000")
    print("🔌 WebSocket available for real-time updates")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
