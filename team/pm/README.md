# PM Agent System - Product Manager for Software Development

This system acts as an autonomous Product Manager (PM) agent that manages the entire software development workflow from user prompts to engineering deliverables.

## Features

### 1. Prompt-to-Ticket Conversion
- Converts raw user prompts into structured tickets
- Extracts title, description, and priority automatically
- Formats prompts specifically for engineering AI consumption

### 2. Ticket Storage & Observation
- Persists tickets to `tickets.json` for durability
- Tracks ticket lifecycle (open → in_progress → review → closed)
- Observes and logs current state of all tickets

### 3. Engineering AI Interface
- Delivers structured tickets to engineering AI
- Receives and stores engineering responses
- Manages response tracking per ticket

### 4. Review & Iteration System
- Reviews engineering AI's work against ticket requirements
- Tracks review iterations for iterative improvement
- Generates improved prompts based on feedback

### 5. Ticket Updates
- Update any ticket field (priority, status, description, etc.)
- Maintain audit trail of all changes

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   User       │      │ PromptConverter  │      │ Engineering AI  │
│   Prompt     │────▶│ (Converts to     │────▶│ (Delivers &      │
│               │     │  Tickets)        │     │  Receives)      │
└───────────────┘     └──────────────────┘     └──────────────────┘
       │                        │                        │
       │                        ▼                        │
       │                 ┌──────────────────┐           │
       │                  │ TicketManager    │           │
       │                  │ (Storage &       │           │
       │                  │  Lifecycle)      │           │
       │                  └──────────────────┘           │
       │                        │                        │
       │                        ▼                        │
       │                 ┌──────────────────┐           │
       │                  │ ReviewAgent      │           │
       │                  │ (Review &        │           │
       │                  │  Rewrite)        │           │
       │                  └──────────────────┘           │
       │                        │                        │
       │                        ▼                        │
       │                 ┌──────────────────┐           │
       │                  │ PMAgent         │           │
       │                  │ (Orchestrator)  │           │
       │                  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Creating a Ticket from User Prompt

```python
from main import PMAgent

pm = PMAgent()

# User provides raw prompt
user_prompt = "Add JWT authentication with token refresh"

# PM converts to structured ticket
ticket = pm.create_ticket_from_prompt(user_prompt)
print(f"Ticket: {ticket.id} - {ticket.title}")
print(f"Priority: {ticket.priority}, Status: {ticket.status}")
```

### Delivering to Engineering AI

```python
# Deliver ticket to engineering AI
response = pm.deliver_to_engineering_ai(ticket)
print(response)  # Engineering AI's response
```

### Reviewing Work

```python
# Review engineering AI's implementation
review_result = pm.review_work(ticket.id)
print(review_result)  # "REVIEW PASSED" or "REVIEW REQUIRED: ..."
```

### Rewriting Prompt (if review fails)

```python
# Rewrite prompt for iteration 2
new_prompt = pm.rewrite_prompt(ticket.id)
print(new_prompt)

# Update ticket with new prompt
pm.update_ticket(ticket.id, {"prompt_for_engineering_ai": new_prompt})
```

### Updating Ticket Status

```python
pm.update_ticket_status("TICKET-001", "in_progress")
pm.update_ticket_status("TICKET-001", "review")
pm.update_ticket_status("TICKET-001", "closed")
```

## Workflow Steps

1. **User provides prompt**: Raw natural language description of desired work
2. **PM creates ticket**: Prompt is converted to structured ticket with title, description, priority
3. **Engineering AI receives ticket**: Ticket is delivered with formatted engineering prompt
4. **Engineering AI responds**: Returns implementation details or code changes
5. **PM reviews work**: Reviews response against requirements
6. **Iterate if needed**: If review fails, PM rewrites prompt and resubmits
7. **Close ticket**: When review passes, ticket status moves to closed

## Ticket Lifecycle

```
open → in_progress → review → closed
  │         │           │
  │         │           └─► Done!
  │         └─► Review failed, rewrite prompt
  └─► Engineering AI working on task
```

## Files

- `main.py`: Core PM agent implementation
- `tickets.json`: Persistent ticket storage
- `test_pm_agent.py`: Comprehensive test suite
- `README.md`: This documentation

## Testing

Run the test suite:

```bash
python -m pytest test_pm_agent.py -v
```

## Configuration

No external configuration required. The system uses:
- `tickets.json` for ticket persistence
- Built-in simulation for engineering AI responses (replace with actual API calls in production)
