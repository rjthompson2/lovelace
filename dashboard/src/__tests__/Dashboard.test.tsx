import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Dashboard from '../components/Dashboard';

describe('Dashboard', () => {
  const mockOnTicketCreated = jest.fn();
  const mockOnTicketUpdated = jest.fn();

  beforeEach(() => {
    render(<Dashboard onTicketCreated={mockOnTicketCreated} onTicketUpdated={mockOnTicketUpdated} />);
  });

  test('renders dashboard header with tabs', () => {
    expect(screen.getByText(/Tickets/i)).toBeInTheDocument();
    expect(screen.getByText(/AI Integration/i)).toBeInTheDocument();
    expect(screen.getByText(/PM Feedback/i)).toBeInTheDocument();
  });

  test('switches between tabs correctly', async () => {
    const ticketsTab = screen.getByText(/Tickets/i);
    fireEvent.click(ticketsTab);
    
    await waitFor(() => {
      expect(document.querySelector('.dashboard-main')).toHaveTextContent(/Create New Ticket/);
    });
  });

  test('displays ticket creation form', () => {
    const titleInput = screen.getByPlaceholderText(/Enter ticket title/i);
    expect(titleInput).toBeInTheDocument();
    
    const prioritySelect = screen.getByLabelText(/Priority/i);
    expect(prioritySelect).toBeInTheDocument();
  });

  test('creates new ticket when form is submitted', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Enter ticket title/i), { target: { value: 'Test Ticket' } });
    
    const prioritySelect = screen.getByLabelText(/Priority/i);
    fireEvent.change(prioritySelect, { target: { value: 'high' } });
    
    fireEvent.click(screen.getByText(/Create Ticket/i));
    
    await waitFor(() => {
      expect(mockOnTicketCreated).toHaveBeenCalledWith(
        expect.objectContaining({
          id: expect.stringMatching(/^T-\d+$/),
          title: 'Test Ticket',
          status: 'open',
          priority: 'high'
        })
      );
    });
  });

  test('updates ticket when form is submitted', async () => {
    const ticket = { id: 'T-1234', title: 'Old Title', status: 'open' };
    
    fireEvent.change(screen.getByPlaceholderText(/Enter ticket title/i), { target: { value: 'New Title' } });
    
    const prioritySelect = screen.getByLabelText(/Priority/i);
    fireEvent.change(prioritySelect, { target: { value: 'medium' } });
    
    fireEvent.click(screen.getByText(/Create Ticket/i));
    
    await waitFor(() => {
      expect(mockOnTicketUpdated).toHaveBeenCalledWith(
        expect.objectContaining({
          id: ticket.id,
          title: 'New Title',
          priority: 'medium'
        })
      );
    });
  });

  test('displays notifications for actions', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Enter ticket title/i), { target: { value: 'Test Ticket' } });
    
    const prioritySelect = screen.getByLabelText(/Priority/i);
    fireEvent.change(prioritySelect, { target: { value: 'high' } });
    
    fireEvent.click(screen.getByText(/Create Ticket/i));
    
    await waitFor(() => {
      expect(screen.getByText(/Ticket T-\d+ created successfully/i)).toBeInTheDocument();
    });
  });

  test('filters tickets by status', async () => {
    const filterSelect = screen.getByLabelText(/Status Filter/i);
    fireEvent.change(filterSelect, { target: { value: 'open' } });
    
    await waitFor(() => {
      expect(screen.queryByText(/No tickets found/i)).not.toBeInTheDocument();
    });
  });

  test('displays empty state when no tickets match filter', async () => {
    const filterSelect = screen.getByLabelText(/Status Filter/i);
    fireEvent.change(filterSelect, { target: { value: 'closed' } });
    
    await waitFor(() => {
      expect(screen.getByText(/No tickets found/i)).toBeInTheDocument();
    });
  });
});

describe('TicketList', () => {
  const mockOnCreate = jest.fn();
  const mockOnUpdate = jest.fn();

  beforeEach(() => {
    render(<TicketList tickets={[]} onCreate={mockOnCreate} onUpdate={mockOnUpdate} />);
  });

  test('renders ticket creation form', () => {
    expect(screen.getByPlaceholderText(/Enter ticket title/i)).toBeInTheDocument();
  });

  test('displays priority options', () => {
    const select = screen.getByLabelText(/Priority/i);
    expect(select).toHaveValue('medium');
  });
});

describe('AIIntegration', () => {
  const mockOnTicketCreated = jest.fn();

  beforeEach(() => {
    render(<AIIntegration onTicketCreated={mockOnTicketCreated} />);
  });

  test('displays quick action buttons', () => {
    expect(screen.getByText(/Bug Report/i)).toBeInTheDocument();
    expect(screen.getByText(/Feature Request/i)).toBeInTheDocument();
  });

  test('generates AI response for bug report prompt', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Describe what needs to be done\.\.\./), { target: { value: 'Generate a bug report ticket' } });
    
    await waitFor(() => {
      expect(screen.getByText(/Critical bug detected in authentication module/i)).toBeInTheDocument();
    });
  });

  test('creates ticket from AI analysis', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Describe what needs to be done\.\.\./), { target: { value: 'Generate a bug report ticket' } });
    
    await waitFor(() => {
      expect(mockOnTicketCreated).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'Critical bug detected in authentication module',
          priority: 'high'
        })
      );
    });
  });
});

describe('PMFeedback', () => {
  const mockOnTicketUpdated = jest.fn();

  beforeEach(() => {
    render(<PMFeedback onTicketUpdated={mockOnTicketUpdated} />);
  });

  test('displays feedback form', () => {
    expect(screen.getByPlaceholderText(/Describe your feedback or request\.\.\./)).toBeInTheDocument();
  });

  test('displays PM response after submission', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Describe your feedback or request\.\.\./), { target: { value: 'Test message' } });
    
    await waitFor(() => {
      expect(screen.getByText(/I see this is a high priority item/i)).toBeInTheDocument();
    });
  });

  test('acknowledges PM response and creates ticket', async () => {
    fireEvent.click(screen.getByText(/Acknowledge & Create Ticket/i));
    
    await waitFor(() => {
      expect(mockOnTicketUpdated).toHaveBeenCalledWith(
        expect.objectContaining({
          status: 'in-progress'
        })
      );
    });
  });

  test('displays feedback history', () => {
    expect(screen.getByText(/Recent Feedback Exchange/i)).toBeInTheDocument();
  });
});

describe('ChatBox', () => {
  beforeEach(() => {
    render(<ChatBox />);
  });

  test('displays PM status indicator', () => {
    expect(screen.getByText(/Available/i)).toBeInTheDocument();
  });

  test('displays initial greeting message', async () => {
    await waitFor(() => {
      expect(screen.getByText(/Welcome! I.*m your PM assistant/i)).toBeInTheDocument();
    });
  });

  test('displays quick action buttons', () => {
    expect(screen.getByText(/Create Ticket/i)).toBeInTheDocument();
    expect(screen.getByText(/Request Feature/i)).toBeInTheDocument();
  });

  test('generates response for hello message', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Type your message to PM\.\.\./), { target: { value: 'Hello' } });
    
    await waitFor(() => {
      expect(screen.getByText(/Hello! How can I assist you today/i)).toBeInTheDocument();
    });
  });

  test('generates response for ticket-related message', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Type your message to PM\.\.\./), { target: { value: 'What is the status of our tickets?' } });
    
    await waitFor(() => {
      expect(screen.getByText(/I can help with that/i)).toBeInTheDocument();
    });
  });

  test('displays typing indicator when sending message', async () => {
    fireEvent.change(screen.getByPlaceholderText(/Type your message to PM\.\.\./), { target: { value: 'Test' } });
    
    await waitFor(() => {
      expect(document.querySelector('.typing-indicator')).toBeInTheDocument();
    });
  });
});
