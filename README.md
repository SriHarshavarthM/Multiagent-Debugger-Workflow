# 🤖 AlgoSync - Multiagent Code Debugger

Advanced code analysis platform with intelligent multiagent workflow for debugging, profiling, and optimization across multiple programming languages.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 7 Specialized AI Agents

1. **🔍 Error Detector** - Identifies syntax, runtime, and logical errors
2. **📊 Complexity Analyzer** - Calculates Big O notation, cyclomatic complexity, and maintainability metrics
3. **💾 Memory Profiler** - Detects memory leaks and optimization opportunities
4. **🔒 Security Analyzer** - Scans for OWASP Top 10 vulnerabilities (SQL injection, XSS, etc.)
5. **✨ Code Quality Checker** - Identifies code smells and best practice violations
6. **🎬 Algorithm Visualizer** - Creates animated step-by-step algorithm visualizations
7. **🔧 Fix Suggester** - Generates intelligent fix recommendations

### Advanced Capabilities

- 🌐 **Multi-language Support**: Python, JavaScript, TypeScript, Java, C++, C, Go, Rust, Ruby, PHP
- 🎨 **Algorithm Visualization**: Watch sorting, searching, and graph algorithms execute in real-time
- ⚡ **Parallel Agent Execution**: Multiple agents analyze code simultaneously
- 📈 **Efficiency Metrics**: Track comparisons, swaps, and complexity in real-time
- 🎥 **Playback Controls**: Step through algorithm execution frame-by-frame
- 💎 **Premium Dark UI**: Glassmorphic design with smooth animations
- 🔄 **Real-time Updates**: WebSocket support for live analysis progress

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python app.py
```

Backend API will be available at `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend UI will be available at `http://localhost:5173`

## 📖 Usage

1. **Open the application** in your browser at `http://localhost:5173`
2. **Select a programming language** from the dropdown
3. **Write or paste your code** in the Monaco editor
4. **Click "Analyze Code"** to start the multiagent analysis
5. **Watch agents execute** in the workflow dashboard
6. **Review findings** in the results panel
7. **Explore visualizations** if algorithms are detected

### Sample Code

Try this bubble sort example:

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

data = [64, 34, 25, 12, 22, 11, 90]
sorted_data = bubble_sort(data)
```

## 🏗️ Architecture

### Backend (Python Flask)

```
backend/
├── app.py                      # Flask application entry
├── config.py                   # Configuration
├── agents/                     # Analysis agents
│   ├── error_detector.py
│   ├── complexity_analyzer.py
│   ├── memory_profiler.py
│   ├── security_analyzer.py
│   ├── quality_checker.py
│   ├── algorithm_visualizer.py
│   └── fix_suggester.py
├── orchestrator/               # Workflow management
│   └── workflow_manager.py
└── routes/                     # API endpoints
    ├── analysis.py
    └── websocket.py
```

### Frontend (React + Vite)

```
frontend/src/
├── App.jsx                     # Main application
├── components/
│   ├── CodeEditor.jsx          # Monaco editor
│   ├── WorkflowDashboard.jsx   # Agent status display
│   ├── ResultsPanel.jsx        # Analysis results
│   └── AlgorithmCanvas.jsx     # Visualization canvas
└── styles/                     # CSS files
```

## 🔌 API Reference

### POST /api/analyze

Analyze code with all agents.

**Request:**
```json
{
  "code": "def hello(): pass",
  "language": "python",
  "context": {}
}
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_findings": 15,
    "critical_issues": 2,
    "quality_score": 85
  },
  "agent_results": {...},
  "visualizations": [...]
}
```

### GET /api/languages

Get supported programming languages.

### GET /api/agents

Get information about all available agents.

## 🎨 Algorithm Visualizations

The system automatically detects and visualizes:

- **Sorting**: Bubble Sort, Merge Sort, Quick Sort, Heap Sort
- **Searching**: Binary Search, Linear Search
- **Graph Algorithms**: BFS, DFS, Dijkstra
- **Data Structures**: Arrays, Trees, Graphs, Stacks

Each visualization includes:
- Step-by-step animated execution
- Operation counters (comparisons, swaps)
- Time and space complexity metrics
- Playback controls with speed adjustment

## 🛡️ Security Features

- **Vulnerability Detection**: SQL injection, XSS, command injection
- **Hardcoded Secrets**: Detects passwords and API keys in code
- **Insecure Patterns**: Identifies unsafe random number generation
- **OWASP Compliance**: Checks against Top 10 vulnerabilities

## 📊 Code Quality Metrics

- Cyclomatic Complexity
- Maintainability Index
- Code Smells (long functions, deep nesting)
- Best Practices (naming conventions, documentation)
- Halstead Metrics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Monaco Editor for the code editor component
- Chart.js for data visualization
- D3.js for algorithm visualizations
- Radon for Python complexity metrics
- Bandit for security analysis

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using React, Flask, and AI**
