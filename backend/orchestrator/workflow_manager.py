from typing import Dict, Any, List, Callable
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from agents import (
    ErrorDetectorAgent,
    ComplexityAnalyzerAgent,
    MemoryProfilerAgent,
    SecurityAnalyzerAgent,
    QualityCheckerAgent,
    AlgorithmVisualizerAgent,
    FixSuggesterAgent
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowManager:
    """
    Orchestrates the execution of all analysis agents.
    Manages dependencies, parallel execution, and result aggregation.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.results = {}
        self.status_callback = None
        
        # Initialize all agents
        self.agents = {
            'error_detector': ErrorDetectorAgent(config),
            'complexity_analyzer': ComplexityAnalyzerAgent(config),
            'memory_profiler': MemoryProfilerAgent(config),
            'security_analyzer': SecurityAnalyzerAgent(config),
            'quality_checker': QualityCheckerAgent(config),
            'algorithm_visualizer': AlgorithmVisualizerAgent(config),
            'fix_suggester': FixSuggesterAgent(config)
        }
        
        # Define agent execution order and dependencies
        self.execution_groups = [
            # Group 1: Independent agents (parallel)
            ['error_detector', 'complexity_analyzer', 'memory_profiler', 
             'security_analyzer', 'quality_checker', 'algorithm_visualizer'],
            # Group 2: Dependent agents (needs Group 1 results)
            ['fix_suggester']
        ]
    
    def set_status_callback(self, callback: Callable):
        """Set callback function for real-time status updates."""
        self.status_callback = callback
    
    def analyze(self, code: str, language: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute all agents in optimal order.
        
        Args:
            code: Source code to analyze
            language: Programming language
            context: Additional context
            
        Returns:
            Aggregated results from all agents
        """
        context = context or {}
        self.results = {}
        
        logger.info(f"🚀 Starting multiagent analysis for {language}...")
        self._update_status("started", "Initiating analysis workflow")
        
        # Execute agent groups in sequence
        for group_idx, agent_group in enumerate(self.execution_groups):
            logger.info(f"📦 Executing agent group {group_idx + 1}/{len(self.execution_groups)}")
            self._execute_agent_group(agent_group, code, language, context)
        
        # Compile final report
        final_report = self._compile_report()
        
        logger.info("✅ Multiagent analysis completed successfully")
        self._update_status("completed", "Analysis complete")
        
        return final_report
    
    def _execute_agent_group(self, agent_names: List[str], code: str, 
                            language: str, context: Dict[str, Any]):
        """Execute a group of agents in parallel."""
        
        with ThreadPoolExecutor(max_workers=len(agent_names)) as executor:
            # Submit all agents in this group
            future_to_agent = {}
            for agent_name in agent_names:
                if agent_name not in self.agents:
                    continue
                
                agent = self.agents[agent_name]
                self._update_status("running", f"Running {agent_name}")
                
                # Prepare context (add previous results for dependent agents)
                agent_context = context.copy()
                agent_context['all_findings'] = self.results
                
                # Submit agent execution
                future = executor.submit(agent.run, code, language, agent_context)
                future_to_agent[future] = agent_name
            
            # Collect results as they complete
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    result = future.result()
                    self.results[agent_name] = result
                    logger.info(f"✓ {agent_name} completed")
                    self._update_status("progress", f"{agent_name} completed")
                except Exception as e:
                    logger.error(f"✗ {agent_name} failed: {str(e)}")
                    self.results[agent_name] = {
                        "agent": agent_name,
                        "status": "error",
                        "error": str(e),
                        "findings": []
                    }
    
    def _compile_report(self) -> Dict[str, Any]:
        """Compile aggregated report from all agent results."""
        
        total_findings = 0
        critical_issues = 0
        warnings = 0
        infos = 0
        
        # Count findings across all agents
        for agent_name, result in self.results.items():
            findings = result.get('findings', [])
            total_findings += len(findings)
            
            for finding in findings:
                severity = finding.get('severity', 'info')
                if severity in ['critical', 'error']:
                    critical_issues += 1
                elif severity == 'warning':
                    warnings += 1
                else:
                    infos += 1
        
        # Extract visualizations if available
        visualizations = self.results.get('algorithm_visualizer', {}).get('visualizations', [])
        
        # Get quality score
        quality_score = self.results.get('quality_checker', {}).get('metadata', {}).get('quality_score', 0)
        
        # Get complexity metrics
        complexity_metadata = self.results.get('complexity_analyzer', {}).get('metadata', {})
        
        return {
            "status": "success",
            "summary": {
                "total_findings": total_findings,
                "critical_issues": critical_issues,
                "warnings": warnings,
                "infos": infos,
                "quality_score": quality_score,
                "complexity": complexity_metadata
            },
            "agent_results": self.results,
            "visualizations": visualizations,
            "timestamp": self._get_timestamp()
        }
    
    def _update_status(self, status: str, message: str):
        """Send status update via callback if available."""
        if self.status_callback:
            self.status_callback({
                "status": status,
                "message": message,
                "timestamp": self._get_timestamp()
            })
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
    
    def get_agent_statuses(self) -> Dict[str, Any]:
        """Get current status of all agents."""
        statuses = {}
        for name, agent in self.agents.items():
            statuses[name] = agent.get_status()
        return statuses
