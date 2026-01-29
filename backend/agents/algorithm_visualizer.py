import ast
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent

class AlgorithmVisualizerAgent(BaseAgent):
    """
    Detects algorithms and data structures in code, then generates
    visualization data for animated step-by-step execution.
    
    Supports: sorting, searching, graph algorithms, dynamic programming, trees
    """
    
    ALGORITHM_PATTERNS = {
        'bubble_sort': r'for.*in.*range.*:\s*for.*in.*range.*:.*if.*>.*:',
        'binary_search': r'while.*<=.*:.*mid.*=.*//',
        'merge_sort': r'def.*merge.*:.*def.*merge_sort.*:',
        'quick_sort': r'def.*partition.*:.*def.*quick_sort.*:',
        'bfs': r'queue.*=.*\[.*\].*while.*queue.*:',
        'dfs': r'def.*dfs.*:.*visited',
        'dijkstra': r'distance.*=.*infinity.*priority.*queue',
        'fibonacci': r'def.*fib.*:.*if.*<=.*1.*:.*return.*fib',
        'dynamic_programming': r'dp.*=.*\[.*\].*for.*in.*range'
    }
    
    def analyze(self, code: str, language: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Detect algorithms and generate visualization data."""
        
        supported_languages = ['python', 'javascript', 'java', 'cpp', 'c']
        
        if language not in supported_languages:
            return {
                "agent": self.name,
                "status": "partial",
                "findings": [],
                "visualizations": [],
                "metadata": {
                    "message": f"Algorithm visualization has limited support for {language}. Full support: {', '.join(supported_languages)}"
                }
            }
        
        # Detect algorithms
        detected_algorithms = self._detect_algorithms(code, language)
        
        # Generate visualization data
        visualizations = []
        for algo in detected_algorithms:
            viz_data = self._generate_visualization_data(code, algo, language)
            if viz_data:
                # Add memory efficiency metrics
                viz_data['memory_analysis'] = self._analyze_memory_efficiency(algo, code)
                visualizations.append(viz_data)
        
        return {
            "agent": self.name,
            "status": "success",
            "findings": detected_algorithms,
            "visualizations": visualizations,
            "metadata": {
                "algorithms_detected": len(detected_algorithms),
                "visualizations_generated": len(visualizations),
                "language": language,
                "supported_languages": supported_languages
            }
        }
    
    def _detect_algorithms(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect known algorithms in code."""
        detected = []
        
        for algo_name, pattern in self.ALGORITHM_PATTERNS.items():
            if re.search(pattern, code, re.DOTALL):
                detected.append({
                    'algorithm': algo_name,
                    'category': self._categorize_algorithm(algo_name),
                    'confidence': 0.8,
                    'message': f'Detected {algo_name.replace("_", " ").title()}'
                })
        
        # Detect data structures
        detected.extend(self._detect_data_structures(code))
        
        return detected
    
    def _detect_data_structures(self, code: str) -> List[Dict[str, Any]]:
        """Detect data structures in code."""
        structures = []
        
        # Check for arrays/lists
        if re.search(r'(list|array|\[\])', code, re.IGNORECASE):
            structures.append({
                'data_structure': 'array',
                'category': 'data_structure',
                'message': 'Array/List operations detected'
            })
        
        # Check for trees
        if re.search(r'(class.*Node|left.*right|root)', code):
            structures.append({
                'data_structure': 'tree',
                'category': 'data_structure',
                'message': 'Tree structure detected'
            })
        
        # Check for graphs
        if re.search(r'(graph|adjacency|edges|vertices)', code, re.IGNORECASE):
            structures.append({
                'data_structure': 'graph',
                'category': 'data_structure',
                'message': 'Graph structure detected'
            })
        
        # Check for stacks/queues
        if re.search(r'(stack|queue|deque|push|pop)', code, re.IGNORECASE):
            structures.append({
                'data_structure': 'stack_queue',
                'category': 'data_structure',
                'message': 'Stack/Queue operations detected'
            })
        
        return structures
    
    def _categorize_algorithm(self, algo_name: str) -> str:
        """Categorize algorithm type."""
        if 'sort' in algo_name:
            return 'sorting'
        elif 'search' in algo_name:
            return 'searching'
        elif algo_name in ['bfs', 'dfs', 'dijkstra']:
            return 'graph'
        elif algo_name in ['fibonacci', 'dynamic_programming']:
            return 'dynamic_programming'
        else:
            return 'other'
    
    def _generate_visualization_data(self, code: str, algo: Dict, language: str) -> Dict[str, Any]:
        """Generate visualization data for detected algorithm."""
        
        algo_name = algo.get('algorithm', algo.get('data_structure', ''))
        category = algo.get('category', '')
        
        # Generate sample execution trace
        if category == 'sorting':
            return self._generate_sorting_viz(algo_name)
        elif category == 'searching':
            return self._generate_searching_viz(algo_name)
        elif category == 'graph':
            return self._generate_graph_viz(algo_name)
        elif algo.get('data_structure') == 'tree':
            return self._generate_tree_viz()
        elif algo.get('data_structure') == 'array':
            return self._generate_array_viz()
        
        return None
    
    def _generate_sorting_viz(self, algo_name: str) -> Dict[str, Any]:
        """Generate sorting algorithm visualization data."""
        # Sample data for bubble sort visualization
        sample_array = [64, 34, 25, 12, 22, 11, 90]
        frames = []
        
        # Simulate bubble sort steps
        arr = sample_array.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Comparing frame
                frames.append({
                    'step': len(frames),
                    'array': arr.copy(),
                    'comparing': [j, j + 1],
                    'sorted': list(range(n - i, n)),
                    'operation': 'compare',
                    'message': f'Comparing {arr[j]} and {arr[j+1]}'
                })
                
                if arr[j] > arr[j + 1]:
                    # Swapping frame
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    frames.append({
                        'step': len(frames),
                        'array': arr.copy(),
                        'swapping': [j, j + 1],
                        'sorted': list(range(n - i, n)),
                        'operation': 'swap',
                        'message': f'Swapped {arr[j+1]} and {arr[j]}'
                    })
        
        return {
            'algorithm': algo_name,
            'type': 'sorting',
            'sample_data': sample_array,
            'frames': frames[:50],  # Limit frames
            'metrics': {
                'comparisons': sum(1 for f in frames if f['operation'] == 'compare'),
                'swaps': sum(1 for f in frames if f['operation'] == 'swap'),
                'time_complexity': 'O(n²)',
                'space_complexity': 'O(1)'
            }
        }
    
    def _generate_searching_viz(self, algo_name: str) -> Dict[str, Any]:
        """Generate searching algorithm visualization."""
        sample_array = [11, 12, 22, 25, 34, 64, 90]
        target = 25
        frames = []
        
        # Binary search simulation
        left, right = 0, len(sample_array) - 1
        
        while left <= right:
            mid = (left + right) // 2
            frames.append({
                'step': len(frames),
                'array': sample_array,
                'left': left,
                'right': right,
                'mid': mid,
                'target': target,
                'message': f'Checking middle element: {sample_array[mid]}'
            })
            
            if sample_array[mid] == target:
                frames.append({
                    'step': len(frames),
                    'array': sample_array,
                    'found': mid,
                    'message': f'Found target {target} at index {mid}'
                })
                break
            elif sample_array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return {
            'algorithm': algo_name,
            'type': 'searching',
            'sample_data': sample_array,
            'target': target,
            'frames': frames,
            'metrics': {
                'comparisons': len(frames),
                'time_complexity': 'O(log n)',
                'space_complexity': 'O(1)'
            }
        }
    
    def _generate_graph_viz(self, algo_name: str) -> Dict[str, Any]:
        """Generate graph algorithm visualization."""
        # Sample graph: adjacency list
        graph = {
            0: [1, 2],
            1: [0, 3, 4],
            2: [0, 5],
            3: [1],
            4: [1, 5],
            5: [2, 4]
        }
        
        frames = []
        visited = set()
        queue = [0]
        
        # BFS simulation
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                frames.append({
                    'step': len(frames),
                    'current_node': node,
                    'visited': list(visited),
                    'queue': queue.copy(),
                    'message': f'Visiting node {node}'
                })
                
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return {
            'algorithm': algo_name,
            'type': 'graph',
            'graph_data': {
                'nodes': list(graph.keys()),
                'edges': [(k, v) for k, neighbors in graph.items() for v in neighbors]
            },
            'frames': frames,
            'metrics': {
                'nodes_visited': len(visited),
                'time_complexity': 'O(V + E)',
                'space_complexity': 'O(V)'
            }
        }
    
    def _generate_tree_viz(self) -> Dict[str, Any]:
        """Generate tree visualization data."""
        return {
            'data_structure': 'tree',
            'type': 'tree',
            'sample_data': {
                'root': 50,
                'nodes': [
                    {'value': 50, 'left': 30, 'right': 70},
                    {'value': 30, 'left': 20, 'right': 40},
                    {'value': 70, 'left': 60, 'right': 80}
                ]
            },
            'message': 'Binary tree structure detected'
        }
    
    def _generate_array_viz(self) -> Dict[str, Any]:
        """Generate array visualization data."""
        return {
            'data_structure': 'array',
            'type': 'array',
            'sample_data': [10, 20, 30, 40, 50],
            'message': 'Array structure detected'
        }
    
    def _analyze_memory_efficiency(self, algo: Dict, code: str) -> Dict[str, Any]:
        """Analyze memory efficiency of the detected algorithm/data structure."""
        
        algo_name = algo.get('algorithm', algo.get('data_structure', 'unknown'))
        category = algo.get('category', '')
        
        # Memory characteristics by algorithm/structure type
        memory_profiles = {
            'bubble_sort': {
                'space_complexity': 'O(1)',
                'in_place': True,
                'auxiliary_space': '~8 bytes (swap variable)',
                'memory_efficient': True,
                'cache_friendly': True,
                'recommendation': 'Memory efficient but slow. Consider for small datasets.'
            },
            'merge_sort': {
                'space_complexity': 'O(n)',
                'in_place': False,
                'auxiliary_space': 'n * element_size bytes',
                'memory_efficient': False,
                'cache_friendly': False,
                'recommendation': 'Uses extra memory for merging. Use in-place merge sort for memory-constrained environments.'
            },
            'quick_sort': {
                'space_complexity': 'O(log n)',
                'in_place': True,
                'auxiliary_space': 'Stack frames for recursion',
                'memory_efficient': True,
                'cache_friendly': True,
                'recommendation': 'Good balance of speed and memory. Preferred for large datasets.'
            },
            'binary_search': {
                'space_complexity': 'O(1)',
                'in_place': True,
                'auxiliary_space': '~24 bytes (left, right, mid)',
                'memory_efficient': True,
                'cache_friendly': True,
                'recommendation': 'Extremely memory efficient. Ideal for sorted data lookup.'
            },
            'bfs': {
                'space_complexity': 'O(V)',
                'in_place': False,
                'auxiliary_space': 'Queue + Visited set',
                'memory_efficient': False,
                'cache_friendly': False,
                'recommendation': 'Memory scales with graph width. Use DFS for deep narrow graphs.'
            },
            'dfs': {
                'space_complexity': 'O(V)',
                'in_place': False,
                'auxiliary_space': 'Stack (recursion/explicit)',
                'memory_efficient': True,
                'cache_friendly': True,
                'recommendation': 'Better memory for deep graphs. Watch for stack overflow on deep recursion.'
            },
            'array': {
                'space_complexity': 'O(n)',
                'in_place': True,
                'auxiliary_space': 'Contiguous block',
                'memory_efficient': True,
                'cache_friendly': True,
                'recommendation': 'Most cache-friendly. Pre-allocate size if known.'
            },
            'tree': {
                'space_complexity': 'O(n)',
                'in_place': False,
                'auxiliary_space': 'Pointer overhead per node',
                'memory_efficient': False,
                'cache_friendly': False,
                'recommendation': 'Each node has ~16 bytes pointer overhead. Consider array-based trees for performance.'
            },
            'graph': {
                'space_complexity': 'O(V + E)',
                'in_place': False,
                'auxiliary_space': 'Adjacency list/matrix',
                'memory_efficient': False,
                'cache_friendly': False,
                'recommendation': 'Adjacency list saves memory for sparse graphs. Matrix better for dense graphs.'
            },
            'stack_queue': {
                'space_complexity': 'O(n)',
                'in_place': False,
                'auxiliary_space': 'Dynamic allocation',
                'memory_efficient': True,
                'cache_friendly': True,
                'recommendation': 'Use array-based implementation for better cache performance.'
            }
        }
        
        profile = memory_profiles.get(algo_name, {
            'space_complexity': 'Unknown',
            'in_place': None,
            'auxiliary_space': 'Unknown',
            'memory_efficient': None,
            'cache_friendly': None,
            'recommendation': 'Analyze manually for memory characteristics.'
        })
        
        # Estimate memory usage based on code patterns
        estimated_bytes = self._estimate_memory_usage(code, algo_name)
        
        return {
            **profile,
            'estimated_memory_bytes': estimated_bytes,
            'algorithm': algo_name
        }
    
    def _estimate_memory_usage(self, code: str, algo_name: str) -> int:
        """Estimate memory usage in bytes based on code patterns."""
        
        # Count array literals to estimate data size
        array_matches = re.findall(r'\[([^\]]+)\]', code)
        total_elements = 0
        for match in array_matches:
            elements = match.split(',')
            total_elements += len(elements)
        
        # Base estimation: 8 bytes per number (Python float), 50 bytes per string
        estimated = total_elements * 8
        
        # Add overhead based on data structure type
        if algo_name in ['tree', 'graph']:
            estimated += total_elements * 16  # Pointer overhead
        elif algo_name in ['bfs', 'dfs']:
            estimated += total_elements * 8  # Queue/stack overhead
        
        return max(estimated, 64)  # Minimum 64 bytes for any structure

