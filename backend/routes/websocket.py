from flask_socketio import emit
from orchestrator import WorkflowManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_websocket_handlers(socketio):
    """Register WebSocket event handlers for real-time updates."""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        logger.info('🔌 Client connected via WebSocket')
        emit('connected', {'message': 'Connected to Multiagent Debugger'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        logger.info('🔌 Client disconnected')
    
    @socketio.on('analyze')
    def handle_analyze(data):
        """
        Handle real-time analysis request.
        
        Emits progress updates as agents complete.
        """
        try:
            code = data.get('code', '')
            language = data.get('language', 'python')
            context = data.get('context', {})
            
            logger.info(f'📡 WebSocket analysis request for {language}')
            
            # Create workflow with status callback
            workflow = WorkflowManager()
            
            def status_callback(status_data):
                """Emit status updates to client."""
                emit('status_update', status_data)
            
            workflow.set_status_callback(status_callback)
            
            # Run analysis
            emit('analysis_started', {'message': 'Analysis started'})
            result = workflow.analyze(code, language, context)
            
            # Send final result
            emit('analysis_complete', result)
            
        except Exception as e:
            logger.error(f'❌ WebSocket analysis failed: {str(e)}')
            emit('analysis_error', {'error': str(e)})
    
    @socketio.on('get_agent_status')
    def handle_get_agent_status():
        """Get current status of all agents."""
        workflow = WorkflowManager()
        statuses = workflow.get_agent_statuses()
        emit('agent_statuses', statuses)
