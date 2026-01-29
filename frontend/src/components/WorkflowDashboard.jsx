import React from 'react';
import './WorkflowDashboard.css';

const AGENTS = [
    { id: 'error_detector', name: 'Error Detector', icon: '🔍' },
    { id: 'complexity_analyzer', name: 'Complexity Analyzer', icon: '📊' },
    { id: 'memory_profiler', name: 'Memory Profiler', icon: '💾' },
    { id: 'security_analyzer', name: 'Security Analyzer', icon: '🔒' },
    { id: 'quality_checker', name: 'Quality Checker', icon: '✨' },
    { id: 'algorithm_visualizer', name: 'Algorithm Visualizer', icon: '🎬' },
    { id: 'fix_suggester', name: 'Fix Suggester', icon: '🔧' }
];

const WorkflowDashboard = ({ statuses }) => {
    const getStatus = (agentId) => {
        return statuses[agentId] || 'pending';
    };

    const getStatusClass = (status) => {
        if (status === 'completed') return 'status-completed';
        if (status === 'running') return 'status-running';
        if (status === 'error') return 'status-error';
        return 'status-pending';
    };

    const getStatusIcon = (status) => {
        if (status === 'completed') return '✓';
        if (status === 'running') return '⏳';
        if (status === 'error') return '✗';
        return '○';
    };

    return (
        <div className="workflow-dashboard">
            <h3 className="workflow-title">
                <span className="icon">🤖</span>
                Agent Workflow
            </h3>

            <div className="agents-grid">
                {AGENTS.map((agent) => {
                    const status = getStatus(agent.id);
                    return (
                        <div
                            key={agent.id}
                            className={`agent-card ${getStatusClass(status)}`}
                        >
                            <div className="agent-icon">{agent.icon}</div>
                            <div className="agent-info">
                                <h4 className="agent-name">{agent.name}</h4>
                                <div className="agent-status">
                                    {getStatusIcon(status)} {status}
                                </div>
                            </div>
                            {status === 'running' && (
                                <div className="progress-bar">
                                    <div className="progress-fill"></div>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default WorkflowDashboard;
