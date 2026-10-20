import React, { useState, useEffect } from 'react';
import TicketList from './TicketList';
import AIIntegration from './AIIntegration';
import PMFeedback from './PMFeedback';
import ChatBox from './ChatBox';

interface DashboardProps {
  onTicketCreated: (ticket: any) => void;
  onTicketUpdated: (ticket: any) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onTicketCreated, onTicketUpdated }) => {
  const [activeTab, setActiveTab] = useState<'tickets' | 'ai' | 'pm'>('tickets');
  const [notifications, setNotifications] = useState([]);

  // Simulate ticket data
  const [tickets, setTickets] = useState([
    { id: 'T-1001', title: 'Fix login bug', status: 'open', priority: 'high', assignee: 'dev1' },
    { id: 'T-1002', title: 'Add new feature', status: 'in-progress', priority: 'medium', assignee: 'dev2' },
    { id: 'T-1003', title: 'Performance optimization', status: 'closed', priority: 'low', assignee: 'dev3' },
  ]);

  // Handle ticket creation
  const handleTicketCreated = (ticket) => {
    setTickets([...tickets, ticket]);
    onTicketCreated(ticket);
    addNotification(`Ticket ${ticket.id} created successfully`);
  };

  // Handle ticket update
  const handleTicketUpdated = (ticket) => {
    setTickets(tickets.map(t => t.id === ticket.id ? ticket : t));
    onTicketUpdated(ticket);
    addNotification(`Ticket ${ticket.id} updated`);
  };

  // Notification system
  const addNotification = (message: string) => {
    const newNotification = { id: Date.now(), message, type: 'info' };
    setNotifications([...notifications, newNotification]);
    setTimeout(() => {
      setNotifications(notifications.filter(n => n.id !== newNotification.id));
    }, 5000);
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
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
            className={`tab ${activeTab === 'ai' ? 'active' : ''}`}
            onClick={() => setActiveTab('ai')}
          >
            AI Integration
          </button>
          <button
            className={`tab ${activeTab === 'pm' ? 'active' : ''}`}
            onClick={() => setActiveTab('pm')}
          >
            PM Feedback
          </button>
        </nav>
      </header>

      {/* Main Content Area */}
      <main className="dashboard-main">
        {activeTab === 'tickets' && (
          <TicketList
            tickets={tickets}
            onCreate={handleTicketCreated}
            onUpdate={handleTicketUpdated}
          />
        )}

        {activeTab === 'ai' && (
          <AIIntegration onTicketCreated={handleTicketCreated} />
        )}

        {activeTab === 'pm' && (
          <PMFeedback onTicketUpdated={handleTicketUpdated} />
        )}
      </main>

      {/* Chat Box - Always visible at bottom */}
      <ChatBox />

      {/* Notifications */}
      {notifications.length > 0 && (
        <div className="notifications">
          {notifications.map(notif => (
            <div key={notif.id} className={`notification ${notif.type}`}>
              {notif.message}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
