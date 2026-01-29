from typing import Dict, Any, List
from .base_agent import BaseAgent
import os

class FixSuggesterAgent(BaseAgent):
    """
    Generates intelligent fix suggestions for detected issues.
    Can use AI if OpenAI API key is available.
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        self.use_ai = bool(os.environ.get('OPENAI_API_KEY'))
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fix suggestions based on all agent findings."""
        
        # Get findings from other agents
        all_findings = context.get('all_findings', {})
        suggestions = []
        
        # Generate fixes for errors
        if 'error_detector' in all_findings:
            suggestions.extend(self._suggest_error_fixes(
                all_findings['error_detector'], code, language
            ))
        
        # Generate optimization suggestions
        if 'complexity_analyzer' in all_findings:
            suggestions.extend(self._suggest_optimizations(
                all_findings['complexity_analyzer'], code, language
            ))
        
        # Generate security fixes
        if 'security_analyzer' in all_findings:
            suggestions.extend(self._suggest_security_fixes(
                all_findings['security_analyzer'], code, language
            ))
        
        return {
            "agent": self.name,
            "status": "success",
            "findings": suggestions,
            "metadata": {
                "total_suggestions": len(suggestions),
                "auto_fixable": len([s for s in suggestions if s.get('auto_fixable')])
            }
        }
    
    def _suggest_error_fixes(self, findings: List[Dict], code: str, language: str) -> List[Dict]:
        """Generate fixes for error findings."""
        suggestions = []
        
        for finding in findings:
            if finding.get('category') == 'syntax':
                if 'Division by zero' in finding.get('message', ''):
                    suggestions.append({
                        'issue': 'Division by zero',
                        'fix_type': 'error_fix',
                        'severity': 'high',
                        'suggestion': 'Add zero check before division',
                        'code_example': 'if divisor != 0:\n    result = numerator / divisor',
                        'auto_fixable': False
                    })
        
        return suggestions
    
    def _suggest_optimizations(self, findings: List[Dict], code: str, language: str) -> List[Dict]:
        """Generate optimization suggestions."""
        suggestions = []
        
        for finding in findings:
            if finding.get('category') == 'time_complexity':
                big_o = finding.get('big_o', '')
                if 'O(n²)' in big_o or 'O(n^2)' in big_o:
                    suggestions.append({
                        'issue': 'Quadratic time complexity',
                        'fix_type': 'optimization',
                        'severity': 'medium',
                        'suggestion': 'Consider using hash table for O(n) lookup',
                        'explanation': 'Replace nested loops with hash-based approach',
                        'auto_fixable': False
                    })
        
        return suggestions
    
    def _suggest_security_fixes(self, findings: List[Dict], code: str, language: str) -> List[Dict]:
        """Generate security fix suggestions."""
        suggestions = []
        
        for finding in findings:
            vuln_type = finding.get('vulnerability', '')
            
            if vuln_type == 'sql_injection':
                suggestions.append({
                    'issue': 'SQL Injection vulnerability',
                    'fix_type': 'security_fix',
                    'severity': 'critical',
                    'suggestion': 'Use parameterized queries',
                    'code_example': 'cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))',
                    'auto_fixable': False,
                    'line': finding.get('line')
                })
            
            elif vuln_type == 'hardcoded_secrets':
                suggestions.append({
                    'issue': 'Hardcoded credentials',
                    'fix_type': 'security_fix',
                    'severity': 'high',
                    'suggestion': 'Use environment variables',
                    'code_example': 'password = os.environ.get("DB_PASSWORD")',
                    'auto_fixable': False,
                    'line': finding.get('line')
                })
        
        return suggestions
