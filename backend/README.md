# Multiagent Debugger Backend

Advanced code analysis backend with 7 specialized AI agents.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### POST /api/analyze
Analyze code with all agents.

**Request:**
```json
{
  "code": "def bubble_sort(arr): ...",
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
    "warnings": 5,
    "quality_score": 85
  },
  "agent_results": {...},
  "visualizations": [...]
}
```

### GET /api/languages
Get supported languages.

### GET /api/agents
Get information about all agents.

## WebSocket Events

Connect to `ws://localhost:5000` for real-time updates.

**Events:**
- `analyze` - Start analysis
- `status_update` - Receive progress updates
- `analysis_complete` - Receive final results

## Agents

1. **Error Detector** - Syntax, runtime, logical errors
2. **Complexity Analyzer** - Big O, cyclomatic complexity
3. **Memory Profiler** - Memory leaks, optimization
4. **Security Analyzer** - Vulnerabilities, OWASP
5. **Quality Checker** - Code smells, best practices
6. **Algorithm Visualizer** - Algorithm animations
7. **Fix Suggester** - Intelligent fixes
