from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Abstract base class for all analysis agents.
    
    All agents must implement the analyze() method and follow
    the standardized result format.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = self.__class__.__name__
        self.status = "initialized"
        self.execution_time = 0
        
    @abstractmethod
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the provided code and return results.
        
        Args:
            code: Source code to analyze
            language: Programming language (python, javascript, etc.)
            context: Additional context (filename, dependencies, etc.)
            
        Returns:
            Dictionary with standardized result format:
            {
                "agent": "AgentName",
                "status": "success" | "error" | "skipped",
                "findings": [...],
                "metadata": {...},
                "execution_time": float
            }
        """
        pass
    
    def run(self, code: str, language: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the agent analysis with timing and error handling.
        """
        context = context or {}
        start_time = time.time()
        self.status = "running"
        
        try:
            logger.info(f"🤖 {self.name} starting analysis for {language}...")
            result = self.analyze(code, language, context)
            
            self.execution_time = time.time() - start_time
            result['execution_time'] = self.execution_time
            self.status = "completed"
            
            logger.info(f"✅ {self.name} completed in {self.execution_time:.2f}s")
            return result
            
        except Exception as e:
            self.execution_time = time.time() - start_time
            self.status = "error"
            
            logger.error(f"❌ {self.name} failed: {str(e)}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "findings": [],
                "metadata": {},
                "execution_time": self.execution_time
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent": self.name,
            "status": self.status,
            "execution_time": self.execution_time
        }
