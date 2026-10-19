import React, { useState } from 'react';

interface PMFeedbackProps {
  onTicketUpdated: (ticket: any) => void;
}

const PMFeedback: React.FC<PMFeedbackProps> = ({ onTicketUpdated }) => {
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const [pmResponse, setPmResponse] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [feedbackHistory, setFeedbackHistory] = useState([]);

  // PM responses based on feedback type
  const pmResponses = {
    highPriority: 'I see this is a high priority item. Let me prioritize it in our sprint planning.',
    featureRequest: 'That sounds like a great idea! I\'ll add it to the backlog for review.',
    bugReport: 'Thanks for flagging this. Can you provide more details about the steps to reproduce?',
    general: 'Understood. Please keep me updated on progress.'
  };

  // Handle feedback submission
  const handleFeedbackSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedbackMessage.trim()) return;

    setIsSending(true);

    // Simulate PM response delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    const responseText = pmResponses.general;
    setPmResponse(responseText);
    
    const newHistoryItem = {
      id: Date.now(),
      message: feedbackMessage,
      response: responseText,
      timestamp: new Date().toISOString(),
    };

    setFeedbackHistory([...feedbackHistory, newHistoryItem]);
    setFeedbackMessage('');
    setIsSending(false);
  };

  // Handle PM response click
  const handlePmResponseClick = () => {
    onTicketUpdated({
      id: `T-${Date.now().toString().slice(-4)}`,
      title: 'PM Feedback Response',
      status: 'in-progress',
      priority: 'medium',
      assignee: 'pm-team',
    });
  };

  return (
    <div className="pm-feedback">
      <h2>PM Feedback & Communication</h2>

      {/* Feedback Form */}
      <form onSubmit={handleFeedbackSubmit} className="feedback-form">
        <h3>Send Feedback to Product Manager</h3>
        
        <div className="form-group">
          <label>Type of Feedback</label>
          <select value="" onChange={(e) => {}}>
            <option value="">Select type...</option>
            <option value="high-priority">High Priority Issue</option>
            <option value="feature-request">Feature Request</option>
            <option value="bug-report">Bug Report</option>
            <option value="general">General Feedback</option>
          </select>
        </div>

        <div className="form-group">
          <label>Message</label>
          <textarea
            value={feedbackMessage}
            onChange={(e) => setFeedbackMessage(e.target.value)}
            placeholder="Describe your feedback or request..."
            rows={4}
          />
        </div>

        <button type="submit" disabled={isSending}>
          {isSending ? 'Sending...' : 'Send to PM'}
        </button>
      </form>

      {/* PM Response Display */}
      {pmResponse && (
        <div className="pm-response-card">
          <div className="response-header">
            <span className="avatar">👨‍💼</span>
            <h4>PM Response</h4>
          </div>
          <p>{pmResponse}</p>
          <button onClick={handlePmResponseClick}>Acknowledge & Create Ticket</button>
        </div>
      )}

      {/* Feedback History */}
      <div className="feedback-history">
        <h3>Recent Feedback Exchange</h3>
        {feedbackHistory.length === 0 ? (
          <p>No feedback exchanges yet.</p>
        ) : (
          feedbackHistory.map(item => (
            <div key={item.id} className="history-item">
              <div className="history-header">
                <span>You:</span>
                <span>{item.message}</span>
              </div>
              <div className="history-response">
                <span>PM:</span>
                <span>{item.response}</span>
              </div>
              <div className="history-meta">
                <time>{new Date(item.timestamp).toLocaleString()}</time>
              </div>
            </div>
          ))
        )}
      </div>

      {/* PM Status */}
      <div className="pm-status">
        <h3>PM Availability</h3>
        <div className="status-indicator active">
          <span className="dot"></span>
          <span>Available for communication</span>
        </div>
        <p>Next available: {new Date().toLocaleTimeString()}</p>
      </div>
    </div>
  );
};

export default PMFeedback;
