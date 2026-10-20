import React, { useState } from 'react';

interface Ticket {
  id: string;
  title: string;
  status: 'open' | 'in-progress' | 'closed';
  priority: 'high' | 'medium' | 'low';
  assignee: string;
}

interface TicketListProps {
  tickets: Ticket[];
  onCreate: (ticket: any) => void;
  onUpdate: (ticket: any) => void;
}

const TicketList: React.FC<TicketListProps> = ({ tickets, onCreate, onUpdate }) => {
  const [newTicketTitle, setNewTicketTitle] = useState('');
  const [newTicketPriority, setNewTicketPriority] = useState('medium');
  const [filterStatus, setFilterStatus] = useState<string>('all');

  // Filter tickets by status
  const filteredTickets = filterStatus === 'all' 
    ? tickets 
    : tickets.filter(t => t.status === filterStatus);

  // Handle ticket creation
  const handleCreateTicket = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTicketTitle.trim()) return;

    const newTicket: Ticket = {
      id: `T-${Date.now().toString().slice(-4)}`,
      title: newTicketTitle,
      status: 'open',
      priority: newTicketPriority as any,
      assignee: '',
    };

    onCreate(newTicket);
    setNewTicketTitle('');
    setNewTicketPriority('medium');
  };

  // Handle ticket update
  const handleUpdateTicket = (ticketId: string, field: keyof Ticket, value: any) => {
    onUpdate({ ...tickets.find(t => t.id === ticketId), [field]: value });
  };

  return (
    <div className="ticket-list">
      {/* Create New Ticket Form */}
      <form onSubmit={handleCreateTicket} className="create-ticket-form">
        <h2>Create New Ticket</h2>
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            value={newTicketTitle}
            onChange={(e) => setNewTicketTitle(e.target.value)}
            placeholder="Enter ticket title"
          />
        </div>
        <div className="form-group">
          <label>Priority</label>
          <select
            value={newTicketPriority}
            onChange={(e) => setNewTicketPriority(e.target.value)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        <button type="submit">Create Ticket</button>
      </form>

      {/* Filter Options */}
      <div className="filter-options">
        <label>Status Filter:</label>
        <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
          <option value="all">All Tickets</option>
          <option value="open">Open</option>
          <option value="in-progress">In Progress</option>
          <option value="closed">Closed</option>
        </select>
      </div>

      {/* Ticket Cards */}
      <div className="tickets-grid">
        {filteredTickets.map(ticket => (
          <div key={ticket.id} className={`ticket-card ${ticket.status} ${ticket.priority}`}>
            <div className="ticket-header">
              <span className="ticket-id">{ticket.id}</span>
              <span className={`priority-badge ${ticket.priority}`}>{ticket.priority}</span>
            </div>
            <h3>{ticket.title}</h3>
            <div className="ticket-meta">
              <span>Status: {ticket.status.replace('-', ' ')}</span>
              <span>Assignee: {ticket.assignee || 'Unassigned'}</span>
            </div>
            <div className="ticket-actions">
              <button onClick={() => handleUpdateTicket(ticket.id, 'status', 'open')}>Open</button>
              <button onClick={() => handleUpdateTicket(ticket.id, 'status', 'in-progress')}>In Progress</button>
              <button onClick={() => handleUpdateTicket(ticket.id, 'status', 'closed')}>Close</button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredTickets.length === 0 && (
        <p className="empty-state">No tickets found. Create a new ticket!</p>
      )}
    </div>
  );
};

export default TicketList;
