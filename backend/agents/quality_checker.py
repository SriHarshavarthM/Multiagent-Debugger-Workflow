import ast
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent

class QualityCheckerAgent(BaseAgent):
    """
    Checks code quality including:
    - Code smells
    - Best practices
    - Documentation
    - Naming conventions
    """
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code quality."""
        findings = []
        
        if language == 'python':
            findings.extend(self._check_python_quality(code))
        elif language in ['javascript', 'typescript']:
            findings.extend(self._check_javascript_quality(code))
        
        quality_score = self._calculate_quality_score(findings)
        
        return {
            "agent": self.name,
            "status": "success",
            "findings": findings,
            "metadata": {
                "quality_score": quality_score,
                "total_issues": len(findings),
                "code_smells": len([f for f in findings if f.get('category') == 'code_smell']),
                "best_practices": len([f for f in findings if f.get('category') == 'best_practice'])
            }
        }
    
    def _check_python_quality(self, code: str) -> List[Dict[str, Any]]:
        """Check Python code quality."""
        findings = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Long functions
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno
                    if func_lines > 50:
                        findings.append({
                            'category': 'code_smell',
                            'smell_type': 'long_function',
                            'severity': 'warning',
                            'line': node.lineno,
                            'message': f'Function "{node.name}" is too long ({func_lines} lines)',
                            'suggestion': 'Break down into smaller functions'
                        })
                    
                    # Too many parameters
                    if len(node.args.args) > 5:
                        findings.append({
                            'category': 'code_smell',
                            'smell_type': 'too_many_parameters',
                            'severity': 'warning',
                            'line': node.lineno,
                            'message': f'Function "{node.name}" has {len(node.args.args)} parameters',
                            'suggestion': 'Consider using a config object or class'
                        })
                    
                    # Missing docstring
                    if not ast.get_docstring(node):
                        findings.append({
                            'category': 'best_practice',
                            'severity': 'info',
                            'line': node.lineno,
                            'message': f'Function "{node.name}" missing docstring',
                            'suggestion': 'Add docstring to document function purpose'
                        })
                
                # Deep nesting
                if isinstance(node, (ast.If, ast.For, ast.While)):
                    depth = self._get_nesting_depth(node)
                    if depth > 3:
                        findings.append({
                            'category': 'code_smell',
                            'smell_type': 'deep_nesting',
                            'severity': 'warning',
                            'line': node.lineno,
                            'message': f'Deep nesting detected (depth: {depth})',
                            'suggestion': 'Extract nested logic into separate functions'
                        })
        except:
            pass
        
        # Check naming conventions
        findings.extend(self._check_naming_conventions(code))
        
        return findings
    
    def _check_javascript_quality(self, code: str) -> List[Dict[str, Any]]:
        """Check JavaScript code quality."""
        findings = []
        
        # Check for var usage
        if re.search(r'\bvar\s+', code):
            findings.append({
                'category': 'best_practice',
                'severity': 'info',
                'message': 'Use let/const instead of var',
                'suggestion': 'Replace var with let or const'
            })
        
        # Check for console.log
        console_logs = re.findall(r'console\.log', code)
        if len(console_logs) > 3:
            findings.append({
                'category': 'code_smell',
                'severity': 'info',
                'message': f'Multiple console.log statements ({len(console_logs)})',
                'suggestion': 'Remove console.log or use proper logging'
            })
        
        return findings
    
    def _check_naming_conventions(self, code: str) -> List[Dict[str, Any]]:
        """Check naming conventions."""
        findings = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check snake_case for functions
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                        findings.append({
                            'category': 'best_practice',
                            'severity': 'info',
                            'line': node.lineno,
                            'message': f'Function "{node.name}" should use snake_case',
                            'suggestion': 'Use lowercase with underscores'
                        })
                
                elif isinstance(node, ast.ClassDef):
                    # Check PascalCase for classes
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                        findings.append({
                            'category': 'best_practice',
                            'severity': 'info',
                            'line': node.lineno,
                            'message': f'Class "{node.name}" should use PascalCase',
                            'suggestion': 'Start with uppercase letter'
                        })
        except:
            pass
        
        return findings
    
    def _get_nesting_depth(self, node, current_depth=0) -> int:
        """Calculate nesting depth of a node."""
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While)):
                child_depth = self._get_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
        return max_depth
    
    def _calculate_quality_score(self, findings: List[Dict]) -> float:
        """Calculate overall quality score (0-100)."""
        base_score = 100
        
        for finding in findings:
            severity = finding.get('severity', 'info')
            if severity == 'error':
                base_score -= 10
            elif severity == 'warning':
                base_score -= 5
            elif severity == 'info':
                base_score -= 2
        
        return max(0, min(100, base_score))
