from flask import Blueprint, request, jsonify
from orchestrator import WorkflowManager
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Main analysis endpoint.
    
    Expects JSON body:
    {
        "code": "source code string",
        "language": "python|javascript|...",
        "context": {...}  # optional
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        code = data.get('code', '')
        language = data.get('language', 'python')
        context = data.get('context', {})
        
        # Validate inputs
        if not code:
            return jsonify({
                "status": "error",
                "message": "Code is required"
            }), 400
        
        if language not in Config.SUPPORTED_LANGUAGES:
            return jsonify({
                "status": "error",
                "message": f"Language '{language}' not supported",
                "supported_languages": Config.SUPPORTED_LANGUAGES
            }), 400
        
        if len(code) > Config.MAX_CODE_SIZE:
            return jsonify({
                "status": "error",
                "message": f"Code size exceeds limit ({Config.MAX_CODE_SIZE} bytes)"
            }), 400
        
        logger.info(f"📝 Received analysis request for {language} ({len(code)} bytes)")
        
        # Create workflow manager and run analysis
        workflow = WorkflowManager()
        result = workflow.analyze(code, language, context)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@analysis_bp.route('/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported programming languages."""
    return jsonify({
        "languages": Config.SUPPORTED_LANGUAGES
    }), 200

@analysis_bp.route('/agents', methods=['GET'])
def get_agent_info():
    """Get information about available agents."""
    agents = [
        {
            "name": "Error Detector",
            "id": "error_detector",
            "description": "Detects syntax, runtime, and logical errors",
            "enabled": Config.ENABLE_ERROR_DETECTION
        },
        {
            "name": "Complexity Analyzer",
            "id": "complexity_analyzer",
            "description": "Analyzes time/space complexity and code metrics",
            "enabled": Config.ENABLE_COMPLEXITY_ANALYSIS
        },
        {
            "name": "Memory Profiler",
            "id": "memory_profiler",
            "description": "Profiles memory usage and detects leaks",
            "enabled": Config.ENABLE_MEMORY_PROFILING
        },
        {
            "name": "Security Analyzer",
            "id": "security_analyzer",
            "description": "Scans for security vulnerabilities",
            "enabled": Config.ENABLE_SECURITY_ANALYSIS
        },
        {
            "name": "Quality Checker",
            "id": "quality_checker",
            "description": "Checks code quality and best practices",
            "enabled": Config.ENABLE_QUALITY_CHECK
        },
        {
            "name": "Algorithm Visualizer",
            "id": "algorithm_visualizer",
            "description": "Visualizes algorithms and data structures",
            "enabled": Config.ENABLE_ALGORITHM_VISUALIZATION
        },
        {
            "name": "Fix Suggester",
            "id": "fix_suggester",
            "description": "Generates intelligent fix suggestions",
            "enabled": Config.ENABLE_FIX_SUGGESTIONS
        }
    ]
    
    return jsonify({
        "agents": agents,
        "total": len(agents),
        "enabled": len([a for a in agents if a['enabled']])
    }), 200
