# Dashboard Module

A React-based engineering dashboard for ticket management with AI integration and PM feedback features.

## Overview

The Dashboard module provides a comprehensive interface for managing engineering tickets, integrating AI capabilities, and tracking PM feedback status. It includes:

- **Ticket Management**: Create, view, and manage engineering tickets
- **AI Integration**: Quick actions for bug reports and feature requests powered by AI
- **PM Feedback**: Real-time status indicators for project manager interactions

## Features

### Ticket Creation
- Enter ticket titles with priority selection
- Submit structured ticket data to the system
- Track ticket lifecycle from creation through completion

### AI Integration
- Generate bug reports automatically
- Create feature request proposals
- Analyze code patterns and suggest improvements

### PM Feedback
- Real-time status indicators (Available, Busy, etc.)
- Direct communication channels with project managers
- Priority tracking and escalation workflows

## Components

| Component | Description |
|-----------|-------------|
| `Dashboard` | Main dashboard container with navigation tabs |
| `TicketForm` | Form for creating new engineering tickets |
| `AIIntegration` | Quick action buttons for AI-powered features |
| `ChatBox` | Communication interface for PM feedback |

## Testing

Run tests using Jest:

```bash
npm test -- dashboard/
```

Test files are located in `dashboard/__tests__/`.

## Running the Dashboard

### Prerequisites

- Node.js (v18 or later)
- npm (v8 or later)

### Installation

1. Navigate to the dashboard folder:
   ```bash
   cd dashboard
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. If using a package manager like yarn:
   ```bash
   yarn install
   ```

### Running the Dashboard

To start the development server:

```bash
npm start
```

Or with yarn:
```bash
yarn start
```

The dashboard will be available at `http://localhost:3000` by default.

### Development Commands

| Command | Description |
|---------|-------------|
| `npm start` or `yarn start` | Start the development server |
| `npm run build` | Build for production |
| `npm test` | Run all tests |
| `npm run lint` | Run ESLint |

## License

MIT License