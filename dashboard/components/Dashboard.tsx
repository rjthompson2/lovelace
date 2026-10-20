import React, { useState } from 'react';
import AIIntegration from './AIIntegration';
import ChatBox from './ChatBox';

interface DashboardProps {
  onTicketCreated: (ticket: any) => void;
  onTicketUpdated: (ticket: any) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onTicketCreated, onTicketUpdated }) => {
  const [activeTab, setActiveTab] = useState('tickets');
  const [ticketTitle, setTicketTitle] = useState('');
  const [priority, setPriority] = useState('medium');

  // Handle ticket creation
  const handleTicketCreate = () => {
    if (ticketTitle.trim()) {
      const newTicket = {
        id: Date.now(),
        title: ticketTitle,
        priority,
        status: 'open',
        createdAt: new Date().toISOString()
      };
      onTicketCreated(newTicket);
      setTicketTitle('');
      setPriority('medium');
    }
  };

  // Handle ticket update
  const handleTicketUpdate = (updatedTicket) => {
    onTicketUpdated(updatedTicket);
  };

  return (
    <div className="dashboard">
      {/* Header with tabs */}
      <header className="dashboard-header">
        <h1>Engineering Dashboard</h1>
        <nav className="tabs">
          <button 
            className={`tab ${activeTab === 'tickets' ? 'active' : ''}`}
            onClick={() => setActiveTab('tickets')}
          >
            Tickets
          </button>
          <button 
            className={`tab ${activeTab === 'ai-integration' ? 'active' : ''}`}
            onClick={() => setActiveTab('ai-integration')}
          >
            AI Integration
          </button>
          <button 
            className={`tab ${activeTab === 'pm-feedback' ? 'active' : ''}`}
            onClick={() => setActiveTab('pm-feedback')}
          >
            PM Feedback
          </button>
        </nav>
      </header>

      {/* Ticket Creation Form */}
      <section className="ticket-form">
        <h2>Create New Ticket</h2>
        <form onSubmit={handleTicketCreate}>
          <input
            type="text"
            placeholder="Enter ticket title"
            value={ticketTitle}
            onChange={(e) => setTicketTitle(e.target.value)}
          />
          <select 
            value={priority} 
            onChange={(e) => setPriority(e.target.value)}
          >
            <option value="low">Low Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="high">High Priority</option>
            <option value="critical">Critical Priority</option>
          </select>
          <button type="submit">Create Ticket</button>
        </form>
      </section>

      {/* AI Integration Section */}
      <section className="ai-integration">
        <h2>AI Integration</h2>
        <div className="quick-actions">
          <button onClick={() => alert('Generate Bug Report')}>Bug Report</button>
          <button onClick={() => alert('Create Feature Request')}>Feature Request</button>
          <button onClick={() => alert('Analyze Code Patterns')}>Analyze Code</button>
        </div>
      </section>

      {/* PM Feedback Section */}
      <section className="pm-feedback">
        <h2>PM Feedback</h2>
        <ChatBox />
      </section>
    </div>
  );
};

export default Dashboard;
