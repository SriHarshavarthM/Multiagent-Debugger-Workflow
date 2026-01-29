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
        elif language in ['cpp', 'c']:
            findings.extend(self._check_cpp_quality(code))
        elif language == 'java':
            findings.extend(self._check_java_quality(code))
        else:
            findings.extend(self._check_generic_quality(code, language))
        
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
    
    def _check_cpp_quality(self, code: str) -> List[Dict[str, Any]]:
        """Check C/C++ code quality."""
        findings = []
        lines = code.split('\n')
        
        # Check for using namespace std
        if 'using namespace std;' in code:
            findings.append({
                'category': 'best_practice',
                'severity': 'info',
                'message': 'Avoid "using namespace std;" in headers',
                'suggestion': 'Use std:: prefix or targeted using declarations'
            })
        
        # Check for raw pointers
        raw_ptr_count = len(re.findall(r'\*\s*\w+\s*=\s*new', code))
        if raw_ptr_count > 0:
            findings.append({
                'category': 'best_practice',
                'severity': 'warning',
                'message': f'{raw_ptr_count} raw pointer allocation(s) detected',
                'suggestion': 'Consider using smart pointers (std::unique_ptr, std::shared_ptr)'
            })
        
        # Check function length
        func_pattern = re.compile(r'(void|int|float|double|bool|auto|string)\s+\w+\s*\([^)]*\)\s*\{')
        func_starts = [(m.start(), m.group()) for m in func_pattern.finditer(code)]
        
        for start, func in func_starts:
            # Rough estimate of function length
            brace_count = 1
            pos = start + len(func)
            while pos < len(code) and brace_count > 0:
                if code[pos] == '{':
                    brace_count += 1
                elif code[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            func_length = code[start:pos].count('\n')
            if func_length > 50:
                findings.append({
                    'category': 'code_smell',
                    'severity': 'warning',
                    'message': f'Long function detected (~{func_length} lines)',
                    'suggestion': 'Break down into smaller functions'
                })
        
        # Check for magic numbers
        magic_numbers = re.findall(r'[^0-9][0-9]{2,}[^0-9\.\w]', code)
        if len(magic_numbers) > 3:
            findings.append({
                'category': 'code_smell',
                'severity': 'info',
                'message': f'{len(magic_numbers)} magic numbers detected',
                'suggestion': 'Use named constants instead of magic numbers'
            })
        
        # Check for commented code
        comment_blocks = len(re.findall(r'//.*\{|/\*.*\{.*\*/', code))
        if comment_blocks > 0:
            findings.append({
                'category': 'code_smell',
                'severity': 'info',
                'message': 'Commented code blocks detected',
                'suggestion': 'Remove commented code and use version control'
            })
        
        if not findings:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': 'No obvious quality issues detected in C++ code'
            })
        
        return findings
    
    def _check_java_quality(self, code: str) -> List[Dict[str, Any]]:
        """Check Java code quality."""
        findings = []
        
        # Check for public fields
        public_fields = re.findall(r'public\s+(?!static|class|void|abstract|final|interface)\w+\s+\w+\s*;', code)
        if public_fields:
            findings.append({
                'category': 'best_practice',
                'severity': 'warning',
                'message': f'{len(public_fields)} public field(s) detected',
                'suggestion': 'Use private fields with getters/setters'
            })
        
        # Check for missing final on local variables
        local_vars = len(re.findall(r'\b(?!final\s)(int|String|Object|List|Map|Set)\s+\w+\s*=', code))
        if local_vars > 5:
            findings.append({
                'category': 'best_practice',
                'severity': 'info',
                'message': 'Consider using final for local variables that don\'t change',
                'suggestion': 'Add final keyword to immutable local variables'
            })
        
        # Check for empty catch blocks
        if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', code):
            findings.append({
                'category': 'code_smell',
                'severity': 'warning',
                'message': 'Empty catch block detected',
                'suggestion': 'Log the exception or handle it properly'
            })
        
        # Check for very long lines
        long_lines = [i for i, line in enumerate(code.split('\n'), 1) if len(line) > 120]
        if len(long_lines) > 3:
            findings.append({
                'category': 'code_smell',
                'severity': 'info',
                'message': f'{len(long_lines)} lines exceed 120 characters',
                'suggestion': 'Break long lines for better readability'
            })
        
        # Check for System.out.println
        if 'System.out.println' in code:
            findings.append({
                'category': 'best_practice',
                'severity': 'info',
                'message': 'System.out.println detected',
                'suggestion': 'Use a proper logging framework (SLF4J, Log4j)'
            })
        
        if not findings:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': 'No obvious quality issues detected in Java code'
            })
        
        return findings
    
    def _check_generic_quality(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Generic quality check for unsupported languages."""
        findings = []
        lines = code.split('\n')
        
        # Check line count
        if len(lines) > 500:
            findings.append({
                'category': 'code_smell',
                'severity': 'warning',
                'message': f'File has {len(lines)} lines - consider splitting',
                'suggestion': 'Break into multiple smaller files'
            })
        
        # Check for very long lines
        long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 120]
        if len(long_lines) > 5:
            findings.append({
                'category': 'code_smell',
                'severity': 'info',
                'message': f'{len(long_lines)} lines exceed 120 characters',
                'suggestion': 'Break long lines for better readability'
            })
        
        # Check for TODO comments
        todos = len(re.findall(r'TODO|FIXME|HACK|XXX', code, re.IGNORECASE))
        if todos > 0:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': f'{todos} TODO/FIXME comments found',
                'suggestion': 'Address outstanding TODO items'
            })
        
        if not findings:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': f'Basic quality check passed for {language}'
            })
        
        return findings

