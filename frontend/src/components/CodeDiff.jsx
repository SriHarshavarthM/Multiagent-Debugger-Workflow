import React, { useMemo } from 'react';
import { parseDiff, Diff, Hunk } from 'react-diff-view';
import { createTwoFilesPatch } from 'diff';
import 'react-diff-view/style/index.css';
import './CodeDiff.css';

const CodeDiff = ({ oldCode, newCode, language = 'python' }) => {
    const diff = useMemo(() => {
        if (!oldCode || !newCode) return null;

        // Generate unified diff
        // createTwoFilesPatch(fileName1, fileName2, oldStr, newStr, oldHeader, newHeader)
        const diffText = createTwoFilesPatch(
            'Original',
            'Use Verification',
            oldCode,
            newCode,
            'Original Code',
            'Suggested Fix'
        );

        const files = parseDiff(diffText);
        return files[0];
    }, [oldCode, newCode]);

    if (!diff) return null;

    return (
        <div className="code-diff-container">
            <div className="diff-header">
                <span className="diff-title">Suggested Changes</span>
            </div>
            <div className="diff-content-wrapper">
                <Diff
                    viewType="split"
                    diffType={diff.type}
                    hunks={diff.hunks}
                    optimizeSelection={true}
                >
                    {hunks => hunks.map(hunk => (
                        <Hunk key={hunk.content} hunk={hunk} />
                    ))}
                </Diff>
            </div>
        </div>
    );
};

export default CodeDiff;
