import React from 'react';
import Editor from '@monaco-editor/react';
import './CodeEditor.css';

const CodeEditor = ({ code, onChange, language }) => {
    const handleEditorChange = (value) => {
        onChange(value || '');
    };

    const getLanguageMode = (lang) => {
        const langMap = {
            'python': 'python',
            'javascript': 'javascript',
            'typescript': 'typescript',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'go': 'go',
            'rust': 'rust',
            'ruby': 'ruby',
            'php': 'php'
        };
        return langMap[lang] || 'python';
    };

    return (
        <div className="code-editor-container">
            <div className="editor-header">
                <span className="editor-title">
                    <span className="icon">📝</span>
                    Code Editor
                </span>
                <span className="editor-lang">{language.toUpperCase()}</span>
            </div>
            <Editor
                height="calc(100% - 50px)"
                language={getLanguageMode(language)}
                value={code}
                onChange={handleEditorChange}
                theme="vs-dark"
                options={{
                    minimap: { enabled: true },
                    fontSize: 14,
                    lineNumbers: 'on',
                    roundedSelection: true,
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    tabSize: 4,
                    wordWrap: 'on',
                    padding: { top: 16, bottom: 16 },
                    suggestOnTriggerCharacters: true,
                    quickSuggestions: true,
                    fontFamily: "'Fira Code', 'Consolas', monospace",
                    fontLigatures: true,
                    cursorBlinking: 'smooth',
                    cursorSmoothCaretAnimation: 'on',
                    smoothScrolling: true,
                }}
            />
        </div>
    );
};

export default CodeEditor;
