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
        elif language in ['cpp', 'c', 'java']:
            findings.extend(self._analyze_c_family_complexity(code, language))
        elif language in ['javascript', 'typescript']:
            findings.extend(self._analyze_js_complexity(code, language))
        else:
            findings.extend(self._analyze_generic_complexity(code, language))
        
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
    
    def _analyze_c_family_complexity(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Analyze C/C++/Java code complexity using pattern matching."""
        import re
        findings = []
        
        # Count functions/methods
        if language in ['cpp', 'c']:
            func_pattern = r'\b(?:void|int|float|double|char|bool|string|auto)\s+(\w+)\s*\([^)]*\)\s*{'
        else:  # java
            func_pattern = r'\b(?:public|private|protected)?\s*(?:static)?\s*(?:void|int|float|double|char|boolean|String|\w+)\s+(\w+)\s*\([^)]*\)\s*{'
        
        functions = re.findall(func_pattern, code)
        
        # Count loops for cyclomatic complexity
        for_loops = len(re.findall(r'\bfor\s*\(', code))
        while_loops = len(re.findall(r'\bwhile\s*\(', code))
        if_statements = len(re.findall(r'\bif\s*\(', code))
        switch_cases = len(re.findall(r'\bcase\s+', code))
        
        # Estimate cyclomatic complexity
        base_complexity = 1 + for_loops + while_loops + if_statements + switch_cases
        
        findings.append({
            'category': 'cyclomatic_complexity',
            'name': 'Overall',
            'complexity': base_complexity,
            'line': 1,
            'severity': 'info' if base_complexity <= 10 else 'warning' if base_complexity <= 20 else 'error',
            'message': f'Estimated cyclomatic complexity: {base_complexity}',
            'suggestion': 'Consider refactoring if complexity exceeds 20' if base_complexity > 20 else None
        })
        
        # Analyze nested loops
        nested_depth = self._count_c_loop_depth(code)
        time_complexity = self._estimate_c_time_complexity(nested_depth)
        
        findings.append({
            'category': 'time_complexity',
            'function': 'main',
            'big_o': time_complexity['notation'],
            'line': 1,
            'severity': time_complexity['severity'],
            'message': f'Estimated time complexity: {time_complexity["notation"]}',
            'explanation': time_complexity['explanation']
        })
        
        # Memory usage patterns
        pointer_count = len(re.findall(r'\*\s*\w+', code))
        new_allocations = len(re.findall(r'\bnew\s+', code))
        malloc_calls = len(re.findall(r'\bmalloc\s*\(', code))
        
        if new_allocations > 0 or malloc_calls > 0:
            findings.append({
                'category': 'memory',
                'severity': 'info',
                'message': f'Dynamic allocations: {new_allocations + malloc_calls} (new: {new_allocations}, malloc: {malloc_calls})',
                'suggestion': 'Ensure proper deallocation to prevent memory leaks'
            })
        
        # Function count
        findings.append({
            'category': 'structure',
            'severity': 'info',
            'message': f'Functions detected: {len(functions)}',
            'functions': functions[:10]  # Limit to first 10
        })
        
        return findings
    
    def _analyze_js_complexity(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Analyze JavaScript/TypeScript complexity."""
        import re
        findings = []
        
        # Count functions
        arrow_funcs = len(re.findall(r'=>', code))
        func_declarations = len(re.findall(r'\bfunction\s+\w+', code))
        
        # Loops and conditions
        for_loops = len(re.findall(r'\bfor\s*\(', code))
        while_loops = len(re.findall(r'\bwhile\s*\(', code))
        if_statements = len(re.findall(r'\bif\s*\(', code))
        
        complexity = 1 + for_loops + while_loops + if_statements
        
        findings.append({
            'category': 'cyclomatic_complexity',
            'name': 'Overall',
            'complexity': complexity,
            'line': 1,
            'severity': 'info' if complexity <= 10 else 'warning',
            'message': f'Cyclomatic complexity: {complexity}'
        })
        
        nested_depth = self._count_c_loop_depth(code)
        time_complexity = self._estimate_c_time_complexity(nested_depth)
        
        findings.append({
            'category': 'time_complexity',
            'function': 'module',
            'big_o': time_complexity['notation'],
            'line': 1,
            'severity': time_complexity['severity'],
            'message': f'Estimated time complexity: {time_complexity["notation"]}',
            'explanation': time_complexity['explanation']
        })
        
        findings.append({
            'category': 'structure',
            'severity': 'info',
            'message': f'Functions: {func_declarations} declared, {arrow_funcs} arrow functions'
        })
        
        return findings
    
    def _analyze_generic_complexity(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Generic complexity analysis for unsupported languages."""
        import re
        findings = []
        
        lines = code.count('\n') + 1
        
        # Basic loop detection
        for_loops = len(re.findall(r'\bfor\b', code))
        while_loops = len(re.findall(r'\bwhile\b', code))
        if_statements = len(re.findall(r'\bif\b', code))
        
        complexity = 1 + for_loops + while_loops + if_statements
        
        findings.append({
            'category': 'cyclomatic_complexity',
            'name': 'Estimated',
            'complexity': complexity,
            'line': 1,
            'severity': 'info',
            'message': f'Estimated complexity for {language}: {complexity}'
        })
        
        findings.append({
            'category': 'structure',
            'severity': 'info',
            'message': f'Lines of code: {lines}, Loops: {for_loops + while_loops}, Conditions: {if_statements}'
        })
        
        return findings
    
    def _count_c_loop_depth(self, code: str) -> int:
        """Count maximum nested loop depth in C-style code."""
        max_depth = 0
        current_depth = 0
        
        for char in code:
            if char == '{':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == '}':
                current_depth = max(0, current_depth - 1)
        
        # Estimate loop depth (simplified)
        return min(max_depth, 5)  # Cap at 5
    
    def _estimate_c_time_complexity(self, depth: int) -> Dict[str, Any]:
        """Estimate time complexity from loop depth."""
        if depth <= 1:
            return {'notation': 'O(n)', 'severity': 'info', 'explanation': 'Linear time - single loop level'}
        elif depth == 2:
            return {'notation': 'O(n²)', 'severity': 'warning', 'explanation': 'Quadratic time - nested loops'}
        elif depth == 3:
            return {'notation': 'O(n³)', 'severity': 'error', 'explanation': 'Cubic time - deeply nested loops'}
        else:
            return {'notation': f'O(n^{depth})', 'severity': 'error', 'explanation': f'Polynomial time with depth {depth}'}

