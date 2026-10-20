/**
 * Type definitions for the Engineering Dashboard Module
 */

// Ticket-related types
export interface Ticket {
  id: number;
  title: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'in-progress' | 'closed';
  createdAt: string;
}

// Dashboard props
export interface DashboardProps {
  onTicketCreated?: (ticket: Ticket) => void;
  onTicketUpdated?: (ticket: Ticket) => void;
}

// AI Integration props
export interface AIIntegrationProps {
  onTicketCreated?: (ticket: Ticket) => void;
}

// ChatBox types
export type Sender = 'user' | 'pm';

export interface ChatMessage {
  id: number;
  sender: Sender;
  text: string;
  timestamp: Date;
}

export type PMStatus = 'Available' | 'Busy' | 'Away' | 'Offline';

export interface ChatBoxProps {
  pmStatus?: PMStatus;
  onQuickAction?: (action: string) => void;
}
