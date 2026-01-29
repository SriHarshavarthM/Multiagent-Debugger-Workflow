import ast
import sys
from io import StringIO
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ErrorDetectorAgent(BaseAgent):
    """
    Detects syntax errors, runtime errors, and logical errors in code.
    Supports multiple programming languages.
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        self.error_types = {
            'syntax': [],
            'runtime': [],
            'logical': []
        }
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for errors."""
        findings = []
        
        if language == 'python':
            findings.extend(self._check_python_syntax(code))
            findings.extend(self._check_python_runtime(code))
            findings.extend(self._check_logical_errors(code, language))
        elif language in ['javascript', 'typescript']:
            findings.extend(self._check_javascript_syntax(code))
            findings.extend(self._check_logical_errors(code, language))
        else:
            findings.append({
                'type': 'info',
                'message': f'Limited error detection for {language}',
                'line': 0
            })
        
        return {
            "agent": self.name,
            "status": "success",
            "findings": findings,
            "metadata": {
                "total_errors": len(findings),
                "syntax_errors": len([f for f in findings if f.get('category') == 'syntax']),
                "runtime_errors": len([f for f in findings if f.get('category') == 'runtime']),
                "logical_errors": len([f for f in findings if f.get('category') == 'logical'])
            }
        }
    
    def _check_python_syntax(self, code: str) -> List[Dict[str, Any]]:
        """Check Python syntax errors."""
        errors = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({
                'category': 'syntax',
                'severity': 'error',
                'message': f'Syntax Error: {e.msg}',
                'line': e.lineno,
                'column': e.offset,
                'text': e.text.strip() if e.text else ''
            })
        except Exception as e:
            errors.append({
                'category': 'syntax',
                'severity': 'error',
                'message': f'Parse Error: {str(e)}',
                'line': 0
            })
        return errors
    
    def _check_python_runtime(self, code: str) -> List[Dict[str, Any]]:
        """Check for potential runtime errors using static analysis."""
        errors = []
        try:
            tree = ast.parse(code)
            
            # Check for common runtime error patterns
            for node in ast.walk(tree):
                # Division by zero
                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                    if isinstance(node.right, ast.Constant) and node.right.value == 0:
                        errors.append({
                            'category': 'runtime',
                            'severity': 'error',
                            'message': 'Division by zero detected',
                            'line': node.lineno,
                            'suggestion': 'Add zero check before division'
                        })
                
                # Undefined variable usage (basic check)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    # This is a simplified check - full analysis needs scope tracking
                    pass
                    
        except:
            pass
        
        return errors
    
    def _check_javascript_syntax(self, code: str) -> List[Dict[str, Any]]:
        """Check JavaScript syntax (basic checks)."""
        errors = []
        
        # Basic syntax checks
        if code.count('(') != code.count(')'):
            errors.append({
                'category': 'syntax',
                'severity': 'error',
                'message': 'Mismatched parentheses',
                'line': 0
            })
        
        if code.count('{') != code.count('}'):
            errors.append({
                'category': 'syntax',
                'severity': 'error',
                'message': 'Mismatched braces',
                'line': 0
            })
        
        if code.count('[') != code.count(']'):
            errors.append({
                'category': 'syntax',
                'severity': 'error',
                'message': 'Mismatched brackets',
                'line': 0
            })
        
        return errors
    
    def _check_logical_errors(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for logical errors and anti-patterns."""
        errors = []
        
        if language == 'python':
            try:
                tree = ast.parse(code)
                
                for node in ast.walk(tree):
                    # Check for infinite loops (basic pattern)
                    if isinstance(node, ast.While):
                        if isinstance(node.test, ast.Constant) and node.test.value is True:
                            errors.append({
                                'category': 'logical',
                                'severity': 'warning',
                                'message': 'Potential infinite loop detected (while True)',
                                'line': node.lineno,
                                'suggestion': 'Ensure loop has proper exit condition'
                            })
                    
                    # Check for comparison with None
                    if isinstance(node, ast.Compare):
                        for op, comparator in zip(node.ops, node.comparators):
                            if isinstance(comparator, ast.Constant) and comparator.value is None:
                                if isinstance(op, (ast.Eq, ast.NotEq)):
                                    errors.append({
                                        'category': 'logical',
                                        'severity': 'info',
                                        'message': 'Use "is None" instead of "== None"',
                                        'line': node.lineno,
                                        'suggestion': 'Replace == with is for None comparison'
                                    })
            except:
                pass
        
        return errors
