import React, { useState } from 'react';

interface AIIntegrationProps {
  onTicketCreated: (ticket: any) => void;
}

const AIIntegration: React.FC<AIIntegrationProps> = ({ onTicketCreated }) => {
  const [aiMessage, setAiMessage] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  // AI prompt templates for ticket generation
  const aiPrompts = [
    'Generate a bug report ticket',
    'Create a feature request ticket',
    'Analyze code quality issues',
    'Suggest performance improvements',
    'Review pull request changes'
  ];

  // Handle AI message submission
  const handleAiSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!aiMessage.trim()) return;

    setIsProcessing(true);
    setAiResponse('');

    // Simulate AI processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    const response = generateAiResponse(aiMessage);
    setAiResponse(response);

    // Create ticket from AI analysis
    const aiTicket = {
      id: `T-${Date.now().toString().slice(-4)}`,
      title: response.ticketTitle || 'AI Generated Ticket',
      status: 'open',
      priority: response.priority,
      assignee: '',
    };

    onTicketCreated(aiTicket);
    setAiMessage('');
    setIsProcessing(false);
  };

  // Generate AI response based on prompt
  const generateAiResponse = (prompt: string) => {
    switch (true) {
      case prompt.includes('bug report'):
        return {
          ticketTitle: 'Critical bug detected in authentication module',
          priority: 'high',
          description: 'AI analysis indicates potential security vulnerability in login flow. Recommend immediate investigation.',
        };
      case prompt.includes('feature request'):
        return {
          ticketTitle: 'Implement new user dashboard feature',
          priority: 'medium',
          description: 'User feedback suggests need for enhanced dashboard functionality with improved data visualization.',
        };
      case prompt.includes('code quality'):
        return {
        ticketTitle: 'Code quality issues detected in main branch',
        priority: 'high',
        description: 'AI static analysis found 12 potential issues including unused imports and complex logic patterns.',
      };
      case prompt.includes('performance'):
        return {
        ticketTitle: 'Optimize database queries for user list endpoint',
        priority: 'medium',
        description: 'Performance profiling shows N+1 query issue causing slow response times under load.',
      };
      default:
        return {
          ticketTitle: 'AI Generated Ticket',
          priority: 'medium',
          description: `Based on your request: "${prompt}". AI has generated a preliminary ticket for review.`,
        };
    }
  };

  return (
    <div className="ai-integration">
      <h2>Engineering AI Integration</h2>
      
      {/* Quick Actions */}
      <div className="quick-actions">
        <button onClick={() => setAiMessage('Generate a bug report ticket')}>Bug Report</button>
        <button onClick={() => setAiMessage('Create a feature request ticket')}>Feature Request</button>
        <button onClick={() => setAiMessage('Analyze code quality issues')}>Code Quality Analysis</button>
        <button onClick={() => setAiMessage('Suggest performance improvements')}>Performance Review</button>
      </div>

      {/* AI Chat Interface */}
      <div className="ai-chat-interface">
        <div className="chat-messages">
          <div className="message ai-message">
            Hello! I'm your Engineering AI assistant. How can I help you today?
          </div>
        </div>

        <form onSubmit={handleAiSubmit} className="ai-input-form">
          <textarea
            value={aiMessage}
            onChange={(e) => setAiMessage(e.target.value)}
            placeholder="Describe what needs to be done..."
            rows={3}
          />
          <button type="submit" disabled={isProcessing}>
            {isProcessing ? 'Analyzing...' : 'Send'}
          </button>
        </form>

        {/* AI Response */}
        {aiResponse && (
          <div className="ai-response">
            <h3>AI Analysis Complete</h3>
            <p><strong>Ticket Title:</strong> {aiResponse.ticketTitle}</p>
            <p><strong>Priority:</strong> {aiResponse.priority}</p>
            <p><strong>Description:</strong> {aiResponse.description}</p>
            <button onClick={() => setAiMessage('Review and update ticket details')}>Update Ticket</button>
          </div>
        )}
      </div>

      {/* AI Insights */}
      <div className="ai-insights">
        <h3>AI Insights & Recommendations</h3>
        <ul>
          <li>Automated ticket generation from natural language descriptions</li>
          <li>Priority assessment based on historical data and impact analysis</li>
          <li>Smart suggestions for optimal assignee selection</li>
          <li>Trend analysis for recurring issues</li>
        </ul>
      </div>
    </div>
  );
};

export default AIIntegration;
