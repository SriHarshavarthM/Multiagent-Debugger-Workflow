import React from 'react';
import './ResultsPanel.css';

const ResultsPanel = ({ results }) => {
    if (!results || results.status === 'error') {
        return (
            <div className="results-panel error">
                <h3>❌ Analysis Failed</h3>
                <p>{results?.message || 'An error occurred during analysis'}</p>
            </div>
        );
    }

    const { summary, agent_results } = results;

    const getSeverityClass = (count) => {
        if (count === 0) return 'severity-success';
        if (count <= 5) return 'severity-warning';
        return 'severity-error';
    };

    const renderAgentFindings = (agentId, agentData) => {
        const findings = agentData.findings || [];
        if (findings.length === 0) return null;

        const agentNames = {
            error_detector: { name: 'Error Detector', icon: '🔍' },
            complexity_analyzer: { name: 'Complexity Analyzer', icon: '📊' },
            memory_profiler: { name: 'Memory Profiler', icon: '💾' },
            security_analyzer: { name: 'Security Analyzer', icon: '🔒' },
            quality_checker: { name: 'Quality Checker', icon: '✨' },
            algorithm_visualizer: { name: 'Algorithm Visualizer', icon: '🎬' },
            fix_suggester: { name: 'Fix Suggester', icon: '🔧' }
        };

        const agent = agentNames[agentId] || { name: agentId, icon: '🤖' };

        return (
            <div key={agentId} className="agent-findings">
                <h4 className="agent-findings-title">
                    <span className="icon">{agent.icon}</span>
                    {agent.name}
                    <span className="findings-count">{findings.length}</span>
                </h4>
                <div className="findings-list">
                    {findings.slice(0, 10).map((finding, idx) => (
                        <div key={idx} className={`finding-item severity-${finding.severity || 'info'}`}>
                            <div className="finding-header">
                                <span className="finding-severity">{finding.severity || 'info'}</span>
                                {finding.line && <span className="finding-line">Line {finding.line}</span>}
                            </div>
                            <p className="finding-message">{finding.message}</p>
                            {finding.suggestion && (
                                <p className="finding-suggestion">💡 {finding.suggestion}</p>
                            )}
                            {finding.code_example && (
                                <pre className="code-example">{finding.code_example}</pre>
                            )}
                        </div>
                    ))}
                    {findings.length > 10 && (
                        <p className="more-findings">+ {findings.length - 10} more findings...</p>
                    )}
                </div>
            </div>
        );
    };

    return (
        <div className="results-panel">
            <h3 className="results-title">
                <span className="icon">📈</span>
                Analysis Results
            </h3>

            {/* Summary Cards */}
            <div className="summary-cards">
                <div className="summary-card">
                    <div className="card-value">{summary.total_findings || 0}</div>
                    <div className="card-label">Total Findings</div>
                </div>
                <div className={`summary-card ${getSeverityClass(summary.critical_issues)}`}>
                    <div className="card-value">{summary.critical_issues || 0}</div>
                    <div className="card-label">Critical Issues</div>
                </div>
                <div className={`summary-card ${getSeverityClass(summary.warnings)}`}>
                    <div className="card-value">{summary.warnings || 0}</div>
                    <div className="card-label">Warnings</div>
                </div>
                <div className="summary-card severity-success">
                    <div className="card-value">{summary.quality_score || 0}%</div>
                    <div className="card-label">Quality Score</div>
                </div>
            </div>

            {/* Complexity Overview */}
            {summary.complexity && (
                <div className="complexity-overview">
                    <h4>⚡ Complexity Metrics</h4>
                    <div className="metrics-grid">
                        <div className="metric-item">
                            <span className="metric-label">Avg Cyclomatic:</span>
                            <span className="metric-value">{summary.complexity.avg_cyclomatic || 0}</span>
                        </div>
                        <div className="metric-item">
                            <span className="metric-label">Max Cyclomatic:</span>
                            <span className="metric-value">{summary.complexity.max_cyclomatic || 0}</span>
                        </div>
                        <div className="metric-item">
                            <span className="metric-label">Maintainability:</span>
                            <span className="metric-value">{summary.complexity.maintainability_index || 0}</span>
                        </div>
                    </div>
                </div>
            )}

            {/* Agent Findings */}
            <div className="all-findings">
                {agent_results && Object.entries(agent_results).map(([agentId, agentData]) =>
                    renderAgentFindings(agentId, agentData)
                )}
            </div>
        </div>
    );
};

export default ResultsPanel;
