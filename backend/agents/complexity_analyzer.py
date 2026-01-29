import ast
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ComplexityAnalyzerAgent(BaseAgent):
    """
    Analyzes code complexity including:
    - Time complexity (Big O notation)
    - Space complexity
    - Cyclomatic complexity
    - Cognitive complexity
    """
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code complexity."""
        findings = []
        
        if language == 'python':
            findings.extend(self._analyze_python_complexity(code))
        else:
            findings.append({
                'type': 'info',
                'message': f'Complexity analysis for {language} coming soon',
                'severity': 'info'
            })
        
        return {
            "agent": self.name,
            "status": "success",
            "findings": findings,
            "metadata": self._extract_metadata(findings)
        }
    
    def _analyze_python_complexity(self, code: str) -> List[Dict[str, Any]]:
        """Analyze Python code complexity."""
        findings = []
        
        try:
            # Cyclomatic complexity
            cc_results = cc_visit(code)
            for item in cc_results:
                severity = 'info' if item.complexity <= 5 else 'warning' if item.complexity <= 10 else 'error'
                findings.append({
                    'category': 'cyclomatic_complexity',
                    'name': item.name,
                    'complexity': item.complexity,
                    'line': item.lineno,
                    'severity': severity,
                    'message': f'{item.name} has cyclomatic complexity of {item.complexity}',
                    'suggestion': 'Consider breaking down into smaller functions' if item.complexity > 10 else None
                })
            
            # Maintainability Index
            try:
                mi_results = mi_visit(code, True)
                mi_score = mi_results
                severity = 'info' if mi_score >= 70 else 'warning' if mi_score >= 50 else 'error'
                findings.append({
                    'category': 'maintainability',
                    'metric': 'Maintainability Index',
                    'score': round(mi_score, 2),
                    'severity': severity,
                    'message': f'Maintainability Index: {mi_score:.2f}/100',
                    'interpretation': self._interpret_mi(mi_score)
                })
            except:
                pass
            
            # Halstead metrics
            try:
                h_results = h_visit(code)
                findings.append({
                    'category': 'halstead',
                    'metrics': {
                        'vocabulary': h_results.total.vocabulary,
                        'length': h_results.total.length,
                        'difficulty': round(h_results.total.difficulty, 2),
                        'effort': round(h_results.total.effort, 2),
                        'time': round(h_results.total.time, 2),
                        'bugs': round(h_results.total.bugs, 2)
                    },
                    'severity': 'info',
                    'message': f'Estimated bugs: {h_results.total.bugs:.2f}'
                })
            except:
                pass
            
            # Time complexity analysis (basic pattern matching)
            findings.extend(self._estimate_time_complexity(code))
            
        except Exception as e:
            findings.append({
                'category': 'error',
                'severity': 'error',
                'message': f'Complexity analysis failed: {str(e)}'
            })
        
        return findings
    
    def _estimate_time_complexity(self, code: str) -> List[Dict[str, Any]]:
        """Estimate Big O time complexity using AST analysis."""
        findings = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_big_o(node)
                    if complexity:
                        findings.append({
                            'category': 'time_complexity',
                            'function': node.name,
                            'big_o': complexity['notation'],
                            'line': node.lineno,
                            'severity': complexity['severity'],
                            'message': f'{node.name} has time complexity {complexity["notation"]}',
                            'explanation': complexity['explanation']
                        })
        except:
            pass
        
        return findings
    
    def _calculate_big_o(self, func_node: ast.FunctionDef) -> Dict[str, Any]:
        """Calculate Big O notation from function AST."""
        nested_loops = 0
        has_recursion = False
        max_depth = 0
        current_depth = 0
        
        def count_loops(node, depth=0):
            nonlocal max_depth, has_recursion
            max_depth = max(max_depth, depth)
            
            for child in ast.walk(node):
                if isinstance(child, (ast.For, ast.While)):
                    count_loops(child, depth + 1)
                elif isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name) and child.func.id == func_node.name:
                        has_recursion = True
        
        count_loops(func_node)
        
        # Determine complexity
        if has_recursion:
            return {
                'notation': 'O(2^n)',
                'severity': 'warning',
                'explanation': 'Recursive function detected - may have exponential complexity'
            }
        elif max_depth == 0:
            return {
                'notation': 'O(1)',
                'severity': 'info',
                'explanation': 'Constant time - no loops detected'
            }
        elif max_depth == 1:
            return {
                'notation': 'O(n)',
                'severity': 'info',
                'explanation': 'Linear time - single loop'
            }
        elif max_depth == 2:
            return {
                'notation': 'O(n²)',
                'severity': 'warning',
                'explanation': 'Quadratic time - nested loops'
            }
        elif max_depth >= 3:
            return {
                'notation': f'O(n^{max_depth})',
                'severity': 'error',
                'explanation': f'Polynomial time with {max_depth} nested loops'
            }
        
        return None
    
    def _interpret_mi(self, score: float) -> str:
        """Interpret maintainability index score."""
        if score >= 70:
            return "Excellent - Easy to maintain"
        elif score >= 50:
            return "Good - Moderately maintainable"
        elif score >= 30:
            return "Poor - Difficult to maintain"
        else:
            return "Critical - Very difficult to maintain"
    
    def _extract_metadata(self, findings: List[Dict]) -> Dict[str, Any]:
        """Extract summary metadata from findings."""
        metadata = {
            'avg_cyclomatic': 0,
            'max_cyclomatic': 0,
            'maintainability_index': 0,
            'dominant_complexity': 'Unknown'
        }
        
        cc_values = [f['complexity'] for f in findings if f.get('category') == 'cyclomatic_complexity']
        if cc_values:
            metadata['avg_cyclomatic'] = round(sum(cc_values) / len(cc_values), 2)
            metadata['max_cyclomatic'] = max(cc_values)
        
        for f in findings:
            if f.get('category') == 'maintainability':
                metadata['maintainability_index'] = f.get('score', 0)
        
        return metadata
