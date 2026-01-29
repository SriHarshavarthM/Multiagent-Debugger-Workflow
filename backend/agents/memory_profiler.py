from typing import Dict, Any, List
from .base_agent import BaseAgent

class MemoryProfilerAgent(BaseAgent):
    """
    Analyzes memory usage patterns and detects potential memory leaks.
    """
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze memory usage patterns."""
        findings = []
        
        if language == 'python':
            findings.extend(self._analyze_python_memory(code))
        else:
            findings.append({
                'type': 'info',
                'message': f'Memory profiling for {language} coming soon'
            })
        
        return {
            "agent": self.name,
            "status": "success",
            "findings": findings,
            "metadata": {
                "potential_leaks": len([f for f in findings if f.get('severity') == 'warning']),
                "optimizations": len([f for f in findings if f.get('category') == 'optimization'])
            }
        }
    
    def _analyze_python_memory(self, code: str) -> List[Dict[str, Any]]:
        """Analyze Python memory patterns."""
        findings = []
        
        # Check for large list comprehensions
        if '[' in code and 'for' in code and 'in range' in code:
            findings.append({
                'category': 'optimization',
                'severity': 'info',
                'message': 'Consider using generators instead of list comprehensions for large datasets',
                'suggestion': 'Use (x for x in ...) instead of [x for x in ...]'
            })
        
        # Check for global variables
        if 'global ' in code:
            findings.append({
                'category': 'memory_leak',
                'severity': 'warning',
                'message': 'Global variables detected - may cause memory retention',
                'suggestion': 'Consider using local variables or class instances'
            })
        
        # Check for unclosed resources
        if 'open(' in code and 'with' not in code:
            findings.append({
                'category': 'memory_leak',
                'severity': 'warning',
                'message': 'File opened without context manager - may leak file handles',
                'suggestion': 'Use "with open(...) as f:" to ensure proper cleanup'
            })
        
        return findings
