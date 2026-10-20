import React from 'react';

interface AIIntegrationProps {
  onTicketCreated?: (ticket: any) => void;
}

const AIIntegration: React.FC<AIIntegrationProps> = ({ onTicketCreated }) => {
  return (
    <div className="ai-integration">
      <h2>AI Integration</h2>
      
      {/* Quick Action Buttons */}
      <div className="quick-actions">
        <button 
          onClick={() => alert('Generate Bug Report') || onTicketCreated?.({
            title: 'Bug Report',
            type: 'bug',
            priority: 'high'
          })}
        >
          Bug Report
        </button>
        <button 
          onClick={() => alert('Create Feature Request') || onTicketCreated?.({
            title: 'Feature Request',
            type: 'feature',
            priority: 'medium'
          })}
        >
          Feature Request
        </button>
        <button 
          onClick={() => alert('Analyze Code Patterns') || onTicketCreated?.({
            title: 'Code Analysis',
            type: 'analysis',
            priority: 'low'
          })}
        >
          Analyze Code
        </button>
      </div>

      {/* AI Suggestions */}
      <div className="ai-suggestions">
        <h3>AI Suggestions</h3>
        <ul>
          <li>Automated bug detection from code reviews</li>
          <li>Feature proposal generation based on trends</li>
          <li>Code quality analysis and improvement suggestions</li>
        </ul>
      </div>
    </div>
  );
};

export default AIIntegration;
