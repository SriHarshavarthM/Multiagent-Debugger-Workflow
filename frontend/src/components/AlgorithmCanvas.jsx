import React, { useState, useEffect } from 'react';
import './AlgorithmCanvas.css';

const AlgorithmCanvas = ({ visualization }) => {
    const [currentFrame, setCurrentFrame] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [speed, setSpeed] = useState(1);

    const frames = visualization?.frames || [];
    const metrics = visualization?.metrics || {};
    const type = visualization?.type || '';
    const memoryAnalysis = visualization?.memory_analysis || {};

    useEffect(() => {
        if (isPlaying && frames.length > 0) {
            const interval = setInterval(() => {
                setCurrentFrame(prev => {
                    if (prev >= frames.length - 1) {
                        setIsPlaying(false);
                        return prev;
                    }
                    return prev + 1;
                });
            }, 1000 / speed);

            return () => clearInterval(interval);
        }
    }, [isPlaying, speed, frames.length]);

    const handlePlayPause = () => {
        if (currentFrame >= frames.length - 1) {
            setCurrentFrame(0);
        }
        setIsPlaying(!isPlaying);
    };

    const handleStepForward = () => {
        if (currentFrame < frames.length - 1) {
            setCurrentFrame(currentFrame + 1);
        }
    };

    const handleStepBack = () => {
        if (currentFrame > 0) {
            setCurrentFrame(currentFrame - 1);
        }
    };

    const handleReset = () => {
        setCurrentFrame(0);
        setIsPlaying(false);
    };

    // Handle data structures without animation frames (tree, array, graph)
    if (!visualization) {
        return (
            <div className="algorithm-canvas">
                <p className="no-viz">No visualization data available</p>
            </div>
        );
    }

    // For data structures without frames, show static visualization
    const hasFrames = frames && frames.length > 0;
    const frame = hasFrames ? frames[currentFrame] : null;

    const renderSortingVisualization = () => {
        const arr = frame.array || [];
        const maxValue = Math.max(...arr);

        return (
            <div className="sorting-viz">
                <div className="array-bars">
                    {arr.map((value, idx) => {
                        const height = (value / maxValue) * 100;
                        let className = 'bar';

                        if (frame.comparing?.includes(idx)) className += ' comparing';
                        if (frame.swapping?.includes(idx)) className += ' swapping';
                        if (frame.sorted?.includes(idx)) className += ' sorted';

                        return (
                            <div key={idx} className="bar-container">
                                <div
                                    className={className}
                                    style={{ height: `${height}%` }}
                                >
                                    <span className="bar-value">{value}</span>
                                </div>
                                <span className="bar-index">{idx}</span>
                            </div>
                        );
                    })}
                </div>
                <p className="operation-message">{frame.message}</p>
            </div>
        );
    };

    const renderSearchingVisualization = () => {
        const arr = frame.array || [];

        return (
            <div className="searching-viz">
                <div className="array-cells">
                    {arr.map((value, idx) => {
                        let className = 'cell';
                        if (idx === frame.mid) className += ' mid';
                        if (idx === frame.left) className += ' left';
                        if (idx === frame.right) className += ' right';
                        if (frame.found === idx) className += ' found';

                        return (
                            <div key={idx} className={className}>
                                <span className="cell-value">{value}</span>
                                <span className="cell-index">{idx}</span>
                            </div>
                        );
                    })}
                </div>
                <p className="operation-message">{frame.message}</p>
                <p className="target-indicator">Target: {frame.target}</p>
            </div>
        );
    };

    const renderGraphVisualization = () => {
        return (
            <div className="graph-viz">
                <div className="graph-info">
                    <p className="operation-message">{frame.message}</p>
                    <p>Current Node: <strong>{frame.current_node}</strong></p>
                    <p>Visited: [{frame.visited?.join(', ')}]</p>
                    <p>Queue: [{frame.queue?.join(', ')}]</p>
                </div>
            </div>
        );
    };

    const renderTreeVisualization = () => {
        const treeData = visualization.sample_data || {};
        const nodes = treeData.nodes || [];

        return (
            <div className="tree-viz">
                <div className="tree-container">
                    <div className="tree-root">
                        <div className="tree-node root-node">
                            <span className="node-value">{treeData.root || 'Root'}</span>
                        </div>
                        <div className="tree-children">
                            {nodes.slice(1, 3).map((node, idx) => (
                                <div key={idx} className="tree-branch">
                                    <div className="tree-node">
                                        <span className="node-value">{node.value}</span>
                                    </div>
                                    <div className="tree-sub-children">
                                        {node.left && (
                                            <div className="tree-node leaf">
                                                <span className="node-value">{node.left}</span>
                                            </div>
                                        )}
                                        {node.right && (
                                            <div className="tree-node leaf">
                                                <span className="node-value">{node.right}</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
                <p className="operation-message">{visualization.message || 'Tree structure detected'}</p>
            </div>
        );
    };

    const renderArrayVisualization = () => {
        const arr = visualization.sample_data || [];

        return (
            <div className="array-viz">
                <div className="array-display">
                    {arr.map((value, idx) => (
                        <div key={idx} className="array-cell">
                            <span className="cell-value">{value}</span>
                            <span className="cell-index">[{idx}]</span>
                        </div>
                    ))}
                </div>
                <p className="operation-message">{visualization.message || 'Array structure detected'}</p>
            </div>
        );
    };

    const renderMemoryAnalysis = () => {
        if (!memoryAnalysis || !memoryAnalysis.space_complexity) return null;

        return (
            <div className="memory-analysis">
                <h5 className="memory-title">💾 Memory Analysis</h5>
                <div className="memory-grid">
                    <div className="memory-item">
                        <span className="memory-label">Space Complexity</span>
                        <span className="memory-value">{memoryAnalysis.space_complexity}</span>
                    </div>
                    <div className="memory-item">
                        <span className="memory-label">In-Place</span>
                        <span className="memory-value">{memoryAnalysis.in_place ? '✅ Yes' : '❌ No'}</span>
                    </div>
                    <div className="memory-item">
                        <span className="memory-label">Cache Friendly</span>
                        <span className="memory-value">{memoryAnalysis.cache_friendly ? '✅ Yes' : '❌ No'}</span>
                    </div>
                    <div className="memory-item full-width">
                        <span className="memory-label">Recommendation</span>
                        <span className="memory-value recommendation">{memoryAnalysis.recommendation}</span>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="algorithm-canvas">
            <div className="canvas-header">
                <h4 className="canvas-title">
                    {visualization.algorithm || visualization.data_structure} Visualization
                </h4>
                <span className="canvas-type">{type.toUpperCase()}</span>
            </div>

            <div className="visualization-area">
                {type === 'sorting' && hasFrames && renderSortingVisualization()}
                {type === 'searching' && hasFrames && renderSearchingVisualization()}
                {type === 'graph' && hasFrames && renderGraphVisualization()}
                {type === 'tree' && renderTreeVisualization()}
                {type === 'array' && renderArrayVisualization()}
                {!hasFrames && type !== 'tree' && type !== 'array' && (
                    <div className="static-viz-message">
                        <p className="operation-message">{visualization.message || 'Data structure detected'}</p>
                    </div>
                )}
            </div>

            {renderMemoryAnalysis()}

            {/* Efficiency Metrics */}
            <div className="efficiency-metrics">
                <div className="metric-card">
                    <span className="metric-icon">🔄</span>
                    <div className="metric-info">
                        <span className="metric-label">Comparisons</span>
                        <span className="metric-value">{metrics.comparisons || 0}</span>
                    </div>
                </div>
                {metrics.swaps !== undefined && (
                    <div className="metric-card">
                        <span className="metric-icon">🔃</span>
                        <div className="metric-info">
                            <span className="metric-label">Swaps</span>
                            <span className="metric-value">{metrics.swaps || 0}</span>
                        </div>
                    </div>
                )}
                <div className="metric-card">
                    <span className="metric-icon">⚡</span>
                    <div className="metric-info">
                        <span className="metric-label">Time Complexity</span>
                        <span className="metric-value">{metrics.time_complexity || 'N/A'}</span>
                    </div>
                </div>
                <div className="metric-card">
                    <span className="metric-icon">💾</span>
                    <div className="metric-info">
                        <span className="metric-label">Space Complexity</span>
                        <span className="metric-value">{metrics.space_complexity || 'N/A'}</span>
                    </div>
                </div>
            </div>

            {/* Playback Controls */}
            <div className="playback-controls">
                <div className="control-buttons">
                    <button
                        className="control-btn"
                        onClick={handleReset}
                        title="Reset"
                    >
                        ⏮
                    </button>
                    <button
                        className="control-btn"
                        onClick={handleStepBack}
                        disabled={currentFrame === 0}
                        title="Step Back"
                    >
                        ⏪
                    </button>
                    <button
                        className="control-btn play-btn"
                        onClick={handlePlayPause}
                        title={isPlaying ? 'Pause' : 'Play'}
                    >
                        {isPlaying ? '⏸' : '▶'}
                    </button>
                    <button
                        className="control-btn"
                        onClick={handleStepForward}
                        disabled={currentFrame >= frames.length - 1}
                        title="Step Forward"
                    >
                        ⏩
                    </button>
                </div>

                <div className="speed-control">
                    <span className="speed-label">Speed:</span>
                    <button
                        className={`speed-btn ${speed === 0.5 ? 'active' : ''}`}
                        onClick={() => setSpeed(0.5)}
                    >
                        0.5x
                    </button>
                    <button
                        className={`speed-btn ${speed === 1 ? 'active' : ''}`}
                        onClick={() => setSpeed(1)}
                    >
                        1x
                    </button>
                    <button
                        className={`speed-btn ${speed === 2 ? 'active' : ''}`}
                        onClick={() => setSpeed(2)}
                    >
                        2x
                    </button>
                </div>

                <div className="progress-info">
                    <span className="frame-counter">
                        Step {currentFrame + 1} / {frames.length}
                    </span>
                    <input
                        type="range"
                        min="0"
                        max={frames.length - 1}
                        value={currentFrame}
                        onChange={(e) => setCurrentFrame(parseInt(e.target.value))}
                        className="progress-slider"
                    />
                </div>
            </div>
        </div>
    );
};

export default AlgorithmCanvas;
