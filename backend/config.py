import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-multiagent-debugger'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    
    # Docker settings
    DOCKER_TIMEOUT = 30  # seconds
    DOCKER_MEMORY_LIMIT = '512m'
    DOCKER_CPU_QUOTA = 50000  # 50% of one CPU
    
    # Analysis settings
    MAX_CODE_SIZE = 1024 * 1024  # 1MB
    SUPPORTED_LANGUAGES = [
        'python', 'javascript', 'typescript', 'java', 
        'cpp', 'c', 'go', 'rust', 'ruby', 'php'
    ]
    
    # Agent settings
    ENABLE_ERROR_DETECTION = True
    ENABLE_COMPLEXITY_ANALYSIS = True
    ENABLE_MEMORY_PROFILING = True
    ENABLE_SECURITY_ANALYSIS = True
    ENABLE_QUALITY_CHECK = True
    ENABLE_ALGORITHM_VISUALIZATION = True
    ENABLE_FIX_SUGGESTIONS = True
    
    # AI settings (optional)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    USE_AI_SUGGESTIONS = bool(OPENAI_API_KEY)
    
    # Cache settings
    CACHE_ENABLED = True
    CACHE_TTL = timedelta(hours=1)
    
    # Visualization settings
    MAX_VISUALIZATION_STEPS = 1000  # Limit frames for large datasets
    VISUALIZATION_SAMPLING_THRESHOLD = 100  # Start sampling after this many elements
