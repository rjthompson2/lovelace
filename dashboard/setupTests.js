// Jest setup file
import '@testing-library/jest-dom';

// Configure mock data for testing
global.window = {
  location: {
    href: 'http://localhost:3000/',
    origin: 'http://localhost:3000'
  },
  localStorage: {
    getItem: jest.fn(),
    setItem: jest.fn()
  }
};

// Mock react-router-dom if needed
jest.mock('react-router-dom', () => ({
  useNavigate: jest.fn(() => (nav) => nav),
  useLocation: jest.fn(() => ({ pathname: '/' }))
}));
