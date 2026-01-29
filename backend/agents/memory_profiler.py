from typing import Dict, Any, List
from .base_agent import BaseAgent
import re

class MemoryProfilerAgent(BaseAgent):
    """
    Analyzes memory usage patterns and detects potential memory leaks.
    """
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze memory usage patterns."""
        findings = []
        
        if language == 'python':
            findings.extend(self._analyze_python_memory(code))
        elif language in ['cpp', 'c']:
            findings.extend(self._analyze_cpp_memory(code))
        elif language == 'java':
            findings.extend(self._analyze_java_memory(code))
        elif language in ['javascript', 'typescript']:
            findings.extend(self._analyze_js_memory(code))
        else:
            findings.extend(self._analyze_generic_memory(code, language))
        
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
    
    def _analyze_cpp_memory(self, code: str) -> List[Dict[str, Any]]:
        """Analyze C/C++ memory patterns."""
        findings = []
        lines = code.split('\n')
        
        # Count allocations and deallocations
        new_count = len(re.findall(r'\bnew\s+', code))
        delete_count = len(re.findall(r'\bdelete\s+', code))
        malloc_count = len(re.findall(r'\bmalloc\s*\(', code))
        free_count = len(re.findall(r'\bfree\s*\(', code))
        
        # Check for memory leaks
        if new_count > delete_count:
            findings.append({
                'category': 'memory_leak',
                'severity': 'warning',
                'message': f'Potential memory leak: {new_count} new allocations but only {delete_count} delete calls',
                'suggestion': 'Ensure every new has a corresponding delete, or use smart pointers'
            })
        
        if malloc_count > free_count:
            findings.append({
                'category': 'memory_leak',
                'severity': 'warning',
                'message': f'Potential memory leak: {malloc_count} malloc calls but only {free_count} free calls',
                'suggestion': 'Ensure every malloc has a corresponding free'
            })
        
        # Check for smart pointer usage (good practice)
        if 'unique_ptr' in code or 'shared_ptr' in code:
            findings.append({
                'category': 'best_practice',
                'severity': 'info',
                'message': 'Good: Using smart pointers for automatic memory management'
            })
        elif new_count > 0:
            findings.append({
                'category': 'optimization',
                'severity': 'info',
                'message': 'Consider using smart pointers (unique_ptr, shared_ptr) instead of raw pointers',
                'suggestion': 'Replace raw pointers with std::unique_ptr or std::shared_ptr'
            })
        
        # Check for array allocations
        for i, line in enumerate(lines, 1):
            if re.search(r'new\s+\w+\s*\[', line):
                findings.append({
                    'category': 'memory_allocation',
                    'severity': 'info',
                    'message': f'Dynamic array allocation at line {i}',
                    'line': i,
                    'suggestion': 'Consider using std::vector for safer array management'
                })
        
        # Check for potential dangling pointers
        if 'delete' in code and re.search(r'=\s*nullptr', code) == None:
            findings.append({
                'category': 'dangling_pointer',
                'severity': 'warning',
                'message': 'Pointer deleted but not set to nullptr - potential dangling pointer',
                'suggestion': 'Set pointer to nullptr after deletion'
            })
        
        if not findings:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': 'No obvious memory issues detected in C++ code'
            })
        
        return findings
    
    def _analyze_java_memory(self, code: str) -> List[Dict[str, Any]]:
        """Analyze Java memory patterns."""
        findings = []
        
        # Check for resource leaks
        resources = ['FileInputStream', 'FileOutputStream', 'BufferedReader', 
                     'BufferedWriter', 'Connection', 'Statement', 'ResultSet', 'Scanner']
        
        for resource in resources:
            if resource in code:
                if 'try-with-resources' not in code and '.close()' not in code:
                    findings.append({
                        'category': 'resource_leak',
                        'severity': 'warning',
                        'message': f'{resource} detected - ensure proper closure',
                        'suggestion': 'Use try-with-resources: try (Resource r = new Resource()) { ... }'
                    })
        
        # Check for large object creation in loops
        if re.search(r'for\s*\([^)]+\)\s*\{[^}]*new\s+', code):
            findings.append({
                'category': 'optimization',
                'severity': 'info',
                'message': 'Object creation inside loop - may impact memory',
                'suggestion': 'Consider creating objects outside loops when possible'
            })
        
        # Check for StringBuilder usage
        if 'String +' in code or '+= String' in code:
            findings.append({
                'category': 'optimization',
                'severity': 'info',
                'message': 'String concatenation detected - consider StringBuilder for loops',
                'suggestion': 'Use StringBuilder for multiple string concatenations'
            })
        
        if not findings:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': 'No obvious memory issues detected in Java code'
            })
        
        return findings
    
    def _analyze_js_memory(self, code: str) -> List[Dict[str, Any]]:
        """Analyze JavaScript memory patterns."""
        findings = []
        
        # Check for global variables
        if re.search(r'^var\s+', code, re.MULTILINE):
            findings.append({
                'category': 'memory_leak',
                'severity': 'info',
                'message': 'Global var declarations detected',
                'suggestion': 'Use let or const to limit variable scope'
            })
        
        # Check for event listener cleanup
        if 'addEventListener' in code and 'removeEventListener' not in code:
            findings.append({
                'category': 'memory_leak',
                'severity': 'warning',
                'message': 'Event listeners added without removal - potential memory leak',
                'suggestion': 'Remove event listeners when no longer needed'
            })
        
        # Check for closure memory issues
        if 'setInterval' in code and 'clearInterval' not in code:
            findings.append({
                'category': 'memory_leak',
                'severity': 'warning',
                'message': 'setInterval without clearInterval - memory may not be released',
                'suggestion': 'Store interval ID and call clearInterval when done'
            })
        
        if not findings:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': 'No obvious memory issues detected in JavaScript code'
            })
        
        return findings
    
    def _analyze_generic_memory(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Generic memory analysis for unsupported languages."""
        findings = []
        
        # Basic pattern detection
        if re.search(r'\bnew\b', code):
            findings.append({
                'category': 'allocation',
                'severity': 'info',
                'message': 'Dynamic memory allocation detected'
            })
        
        if re.search(r'\b(malloc|alloc)\b', code):
            findings.append({
                'category': 'allocation',
                'severity': 'info',
                'message': 'C-style memory allocation detected'
            })
        
        if not findings:
            findings.append({
                'category': 'info',
                'severity': 'info',
                'message': f'Basic memory analysis for {language} - no issues detected'
            })
        
        return findings

