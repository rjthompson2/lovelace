import React from 'react';
import Dashboard from './components/Dashboard';

const App: React.FC = () => {
  const [tickets, setTickets] = React.useState([]);

  // Handle ticket creation
  const handleTicketCreated = (ticket) => {
    setTickets([...tickets, ticket]);
  };

  // Handle ticket update
  const handleTicketUpdated = (ticket) => {
    setTickets(tickets.map(t => t.id === ticket.id ? ticket : t));
  };

  return (
    <div className="app-root">
      <Dashboard
        onTicketCreated={handleTicketCreated}
        onTicketUpdated={handleTicketUpdated}
      />
    </div>
  );
};

export default App;
