import re
from typing import Dict, Any, List
from .base_agent import BaseAgent

class SecurityAnalyzerAgent(BaseAgent):
    """
    Scans code for security vulnerabilities including:
    - SQL injection
    - XSS vulnerabilities
    - Command injection
    - Hardcoded secrets
    - Insecure cryptography
    """
    
    SECURITY_PATTERNS = {
        'sql_injection': [
            r'execute\s*\(\s*["\'].*%s.*["\']\s*%',
            r'\.format\s*\(.*\).*execute',
            r'f".*{.*}.*".*execute'
        ],
        'command_injection': [
            r'os\.system\s*\(',
            r'subprocess\.(call|run|Popen).*shell\s*=\s*True',
            r'system\s*\(\s*["\']',  # C/C++ system()
            r'popen\s*\('  # C/C++ popen()
        ],
        'hardcoded_secrets': [
            r'password\s*=\s*["\'].*["\']',
            r'api_key\s*=\s*["\'].*["\']',
            r'secret\s*=\s*["\'].*["\']',
            r'token\s*=\s*["\'].*["\']'
        ],
        'xss': [
            r'innerHTML\s*=',
            r'document\.write\s*\('
        ],
        'insecure_random': [
            r'random\.random\(\)',
            r'Math\.random\(\)',
            r'\brand\s*\(\s*\)',  # C/C++ rand()
            r'\bsrand\s*\('
        ],
        'buffer_overflow': [
            r'strcpy\s*\(',
            r'strcat\s*\(',
            r'sprintf\s*\(',
            r'gets\s*\(',
            r'scanf\s*\([^,]*%s'
        ],
        'format_string': [
            r'printf\s*\(\s*\w+\s*\)',  # printf(variable) without format
            r'sprintf\s*\([^,]+,\s*\w+\s*\)'
        ],
        'null_pointer': [
            r'\*\s*NULL',
            r'\*\s*nullptr'
        ]
    }
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for security vulnerabilities."""
        findings = []
        
        for vuln_type, patterns in self.SECURITY_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    findings.append({
                        'category': 'security',
                        'vulnerability': vuln_type,
                        'severity': self._get_severity(vuln_type),
                        'line': line_num,
                        'code_snippet': match.group(),
                        'message': self._get_message(vuln_type),
                        'recommendation': self._get_recommendation(vuln_type)
                    })
        
        return {
            "agent": self.name,
            "status": "success",
            "findings": findings,
            "metadata": {
                "total_vulnerabilities": len(findings),
                "critical": len([f for f in findings if f['severity'] == 'critical']),
                "high": len([f for f in findings if f['severity'] == 'high']),
                "medium": len([f for f in findings if f['severity'] == 'medium']),
                "low": len([f for f in findings if f['severity'] == 'low'])
            }
        }
    
    def _get_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type."""
        severity_map = {
            'sql_injection': 'critical',
            'command_injection': 'critical',
            'buffer_overflow': 'critical',
            'format_string': 'high',
            'xss': 'high',
            'hardcoded_secrets': 'high',
            'null_pointer': 'high',
            'insecure_random': 'medium'
        }
        return severity_map.get(vuln_type, 'low')
    
    def _get_message(self, vuln_type: str) -> str:
        """Get message for vulnerability type."""
        messages = {
            'sql_injection': 'Potential SQL injection vulnerability detected',
            'command_injection': 'Command injection vulnerability detected',
            'buffer_overflow': 'Buffer overflow vulnerability - unsafe function detected',
            'format_string': 'Format string vulnerability detected',
            'xss': 'Potential XSS vulnerability detected',
            'hardcoded_secrets': 'Hardcoded credential detected',
            'null_pointer': 'Null pointer dereference risk',
            'insecure_random': 'Insecure random number generation'
        }
        return messages.get(vuln_type, 'Security issue detected')
    
    def _get_recommendation(self, vuln_type: str) -> str:
        """Get recommendation for vulnerability type."""
        recommendations = {
            'sql_injection': 'Use parameterized queries or ORM instead of string formatting',
            'command_injection': 'Avoid shell=True, use subprocess with list arguments',
            'buffer_overflow': 'Use strncpy, strncat, snprintf instead of unsafe versions',
            'format_string': 'Always use format specifier: printf("%s", str) not printf(str)',
            'xss': 'Sanitize user input and use textContent instead of innerHTML',
            'hardcoded_secrets': 'Use environment variables or secret management systems',
            'null_pointer': 'Check for NULL/nullptr before dereferencing pointers',
            'insecure_random': 'Use cryptographic RNG: secrets module (Python), std::random_device (C++)'
        }
        return recommendations.get(vuln_type, 'Review and fix security issue')

