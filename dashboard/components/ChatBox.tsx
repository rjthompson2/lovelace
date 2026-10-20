import React, { useState } from 'react';

interface ChatMessage {
  id: number;
  sender: 'user' | 'pm';
  text: string;
  timestamp: Date;
}

interface ChatBoxProps {
  pmStatus?: 'Available' | 'Busy' | 'Away' | 'Offline';
  onQuickAction?: (action: string) => void;
}

const ChatBox: React.FC<ChatBoxProps> = ({ pmStatus = 'Available', onQuickAction }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      sender: 'pm',
      text: 'Hello! I am available to help with your tickets.',
      timestamp: new Date()
    }
  ]);

  // Quick actions for PM feedback
  const handleQuickAction = (action: string) => {
    onQuickAction?.(action);
    setMessages(prev => [
      ...prev,
      {
        id: Date.now(),
        sender: 'user',
        text: action,
        timestamp: new Date()
      }
    ]);
  };

  return (
    <div className="chat-box">
      {/* PM Status Indicator */}
      <div className="pm-status-indicator">
        <span className={`status ${pmStatus.toLowerCase()}`}>
          {pmStatus}
        </span>
      </div>

      {/* Messages Area */}
      <div className="messages">
        {messages.map(message => (
          <div key={message.id} className={`message ${message.sender === 'user' ? 'user-message' : 'pm-message'}`}>
            <p>{message.text}</p>
            <small>{message.timestamp.toLocaleTimeString()}</small>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <button onClick={() => handleQuickAction('Create Ticket')}>Create Ticket</button>
        <button onClick={() => handleQuickAction('Request Feature')}>Request Feature</button>
        <button onClick={() => handleQuickAction('Escalate Issue')}>Escalate Issue</button>
      </div>

      {/* Message Input */}
      <div className="message-input">
        <input 
          type="text" 
          placeholder="Type your message..." 
          className="message-input-field"
        />
        <button className="send-button">Send</button>
      </div>
    </div>
  );
};

export default ChatBox;
