'use client';
import { ReactFlow, Controls, Background } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

export default function ProtocolEditor() {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <h1>Protocol Editor</h1>
      <div style={{ width: '100%', height: '600px', border: '1px solid #ccc' }}>
        <ReactFlow
          nodes={[{ id: '1', position: { x: 0, y: 0 }, data: { label: 'Start Protocol' } }]}
          edges={[]}
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
}
