/**
 * Engineering Dashboard Module Entry Point
 * 
 * This file serves as the main entry point for the dashboard module,
 * exporting all components for use in other parts of the application.
 */

// Export all dashboard components
export { default as Dashboard } from './components/Dashboard';
export { default as AIIntegration } from './components/AIIntegration';
export { default as ChatBox } from './components/ChatBox';

// Re-export types and interfaces for convenience
export * from './types';
