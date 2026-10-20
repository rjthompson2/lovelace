import React, { useState, useEffect } from 'react';

interface ChatMessage {
  id: number;
  sender: 'me' | 'pm';
  text: string;
  timestamp: Date;
  type?: 'text' | 'file' | 'ticket-link';
}

interface ChatBoxProps {
  onTicketCreated?: (ticket: any) => void;
  onTicketUpdated?: (ticket: any) => void;
}

const ChatBox: React.FC<ChatBoxProps> = ({ onTicketCreated, onTicketUpdated }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [pmStatus, setPmStatus] = useState<'available' | 'busy' | 'offline'>('available');

  // Initial greeting
  useEffect(() => {
    addSystemMessage('Welcome! I\'m your PM assistant. How can I help you today?');
  }, []);

  // Simulate typing effect
  useEffect(() => {
    if (isTyping) {
      const timer = setTimeout(() => setIsTyping(false), 1500);
      return () => clearTimeout(timer);
    }
  }, [isTyping]);

  // Handle message submission
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now(),
      sender: 'me',
      text: inputMessage,
      timestamp: new Date(),
    };

    setMessages([...messages, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate PM response
    await new Promise(resolve => setTimeout(resolve, 2000));

    const pmResponseText = generatePmResponse(inputMessage);
    
    const pmMessage: ChatMessage = {
      id: Date.now() + 1,
      sender: 'pm',
      text: pmResponseText,
      timestamp: new Date(),
      type: inputMessage.includes('ticket') ? 'ticket-link' : undefined,
    };

    setMessages(prev => [...prev, pmMessage]);
    setIsTyping(false);
  };

  // Generate PM response based on user message
  const generatePmResponse = (message: string) => {
    if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
      return 'Hello! How can I assist you today? Feel free to ask about tickets, features, or anything else.';
    }
    if (message.toLowerCase().includes('ticket') || message.toLowerCase().includes('issue')) {
      return 'I can help with that. What ticket are you referring to? Would you like me to create a new one or review an existing one?';
    }
    if (message.toLowerCase().includes('feature') || message.toLowerCase().includes('idea')) {
      return 'That sounds interesting! I\'ll add it to the product roadmap for consideration. What specific feature are you thinking about?';
    }
    if (message.toLowerCase().includes('urgent') || message.toLowerCase().includes('critical')) {
      return 'I understand this is urgent. Let me prioritize this and ensure it gets addressed in our next sprint.';
    }
    return 'Thanks for the message! How can I help you today?';
  };

  // Quick action buttons
  const quickActions = [
    { label: 'Create Ticket', action: () => setInputMessage('Please create a new ticket for this discussion') },
    { label: 'Request Feature', action: () => setInputMessage('I would like to request a new feature') },
    { label: 'Report Bug', action: () => setInputMessage('This is a bug that needs immediate attention') },
    { label: 'Schedule Call', action: () => setInputMessage('Let\'s schedule a call to discuss this topic') },
  ];

  // Handle quick action
  const handleQuickAction = (action) => {
    action.action();
  };

  return (
    <div className="chat-box">
      {/* PM Status Indicator */}
      <div className="pm-status-bar">
        <div className={`status-indicator ${pmStatus}`}>
          <span className="dot"></span>
          <span>{pmStatus === 'available' ? 'Available' : pmStatus === 'busy' ? 'Busy' : 'Offline'}</span>
        </div>
        <button onClick={() => setPmStatus(pmStatus === 'available' ? 'busy' : 'available')}>
          {pmStatus === 'available' ? 'Mark as Busy' : 'Mark as Available'}
        </button>
      </div>

      {/* Messages Area */}
      <div className="messages-container">
        {messages.map(message => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className="message-bubble">
              {message.text}
            </div>
            <div className="message-meta">
              <span>{message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
              {message.type === 'ticket-link' && (
                <a href="#" onClick={(e) => e.preventDefault()}>View Ticket</a>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="quick-actions-bar">
        {quickActions.map((action, index) => (
          <button key={index} onClick={() => handleQuickAction(action)}>
            {action.label}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSendMessage} className="message-input-form">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message to PM..."
          autoComplete="off"
        />
        <button type="submit">Send</button>
      </form>

      {/* Quick Suggestions */}
      <div className="suggestions-bar">
        <span>Suggestions:</span>
        <button onClick={() => setInputMessage('Can you help me understand the current status of our tickets?')}>
          Check ticket status
        </button>
        <button onClick={() => setInputMessage('What features are planned for the next sprint?')}>
          Ask about roadmap
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
