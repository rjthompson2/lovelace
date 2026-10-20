const { render, screen } = require('@testing-library/react');
const Dashboard = require('../components/Dashboard').default;

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

  test('displays ticket creation form', () => {
    expect(screen.getByPlaceholderText(/Enter ticket title/i)).toBeInTheDocument();
  });

  test('displays quick action buttons in AI integration', () => {
    render(<AIIntegration onTicketCreated={jest.fn()} />);
    expect(screen.getByText(/Bug Report/i)).toBeInTheDocument();
  });

  test('displays PM status indicator', () => {
    render(<ChatBox />);
    expect(screen.getByText(/Available/i)).toBeInTheDocument();
  });
});
