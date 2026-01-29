import { useState, useEffect } from 'react';
import CodeEditor from './components/CodeEditor';
import WorkflowDashboard from './components/WorkflowDashboard';
import ResultsPanel from './components/ResultsPanel';
import AlgorithmCanvas from './components/AlgorithmCanvas';
import CodeDiff from './components/CodeDiff';
import './App.css';

const SAMPLE_CODE = `def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # Comparing arr[j] and arr[j + 1]
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                # Swap occurred
        if not swapped:
            break
    return arr

# Example usage
data = [64, 34, 25, 12, 22, 11, 90]
sorted_data = bubble_sort(data)
print(sorted_data)
`;

function App() {
  const [code, setCode] = useState(SAMPLE_CODE);
  const [language, setLanguage] = useState('python');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [agentStatuses, setAgentStatuses] = useState({});

  const handleAnalyze = async () => {
    setAnalyzing(true);
    setResults(null);
    setAgentStatuses({});

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          language,
          context: {}
        })
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Analysis failed:', error);
      setResults({
        status: 'error',
        message: error.message
      });
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="logo">
            <span className="logo-icon">🤖</span>
            <span className="logo-text">AlgoSync</span>
            <span className="logo-subtitle">Multiagent Code Debugger</span>
          </h1>
          <div className="header-actions">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="language-select"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="typescript">TypeScript</option>
              <option value="java">Java</option>
              <option value="cpp">C++</option>
            </select>
            <button
              onClick={handleAnalyze}
              className="analyze-btn"
              disabled={analyzing}
            >
              {analyzing ? '⏳ Analyzing...' : '🚀 Analyze Code'}
            </button>
          </div>
        </div>
      </header>

      <div className="main-content">
        <div className="left-panel">
          <CodeEditor
            code={code}
            onChange={setCode}
            language={language}
          />
        </div>

        <div className="right-panel">
          {analyzing && (
            <WorkflowDashboard
              statuses={agentStatuses}
            />
          )}

          {results && !analyzing && (
            <>
              <ResultsPanel results={results} />

              {results.visualizations && results.visualizations.length > 0 && (
                <div className="visualization-section">
                  <h3 className="section-title">
                    <span className="icon">🎨</span>
                    Algorithm Visualization
                  </h3>
                  <AlgorithmCanvas
                    visualization={results.visualizations[0]}
                  />
                </div>
              )}

              {results.agent_results?.fix_suggester?.findings?.[0]?.code_example && (
                <div className="visualization-section">
                  <h3 className="section-title">
                    <span className="icon">🔧</span>
                    Proposed Fix
                  </h3>
                  <CodeDiff
                    oldCode={code}
                    newCode={results.agent_results.fix_suggester.findings[0].code_example}
                    language={language}
                  />
                </div>
              )}
            </>
          )}

          {!analyzing && !results && (
            <div className="welcome-panel">
              <div className="welcome-content">
                <div className="welcome-icon">🎯</div>
                <h2>Welcome to AlgoSync</h2>
                <p>Your intelligent multiagent code analysis platform</p>
                <div className="features-grid">
                  <div className="feature-card">
                    <span className="feature-icon">🔍</span>
                    <h4>Error Detection</h4>
                    <p>Syntax, runtime & logical errors</p>
                  </div>
                  <div className="feature-card">
                    <span className="feature-icon">📊</span>
                    <h4>Complexity Analysis</h4>
                    <p>Big O, cyclomatic metrics</p>
                  </div>
                  <div className="feature-card">
                    <span className="feature-icon">💾</span>
                    <h4>Memory Profiling</h4>
                    <p>Leak detection & optimization</p>
                  </div>
                  <div className="feature-card">
                    <span className="feature-icon">🔒</span>
                    <h4>Security Scan</h4>
                    <p>OWASP vulnerabilities</p>
                  </div>
                  <div className="feature-card">
                    <span className="feature-icon">✨</span>
                    <h4>Code Quality</h4>
                    <p>Best practices & smells</p>
                  </div>
                  <div className="feature-card">
                    <span className="feature-icon">🎬</span>
                    <h4>Algorithm Viz</h4>
                    <p>Animated execution flow</p>
                  </div>
                </div>
                <button onClick={handleAnalyze} className="cta-button">
                  ✨ Try Sample Code
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
