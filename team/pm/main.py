"""
PM Agent System - Product Manager for Software Development

This system acts as a PM that:
1. Clarifies and communicates prompts into tickets
2. Delivers tickets to the engineering AI (in main.py)
3. Stores and observes tickets
4. Updates tickets based on feedback
5. Reviews engineering AI work and rewrites prompts if needed
"""

from dataclasses import dataclass, field
from team.engineering.main import main as agent_code
from typing import Optional
from datetime import datetime
import json
import os
import sys


@dataclass
class Ticket:
    """Represents a development ticket managed by the PM agent."""
    
    id: str
    title: str
    description: str
    priority: str = "medium"  # low, medium, high, critical
    status: str = "open"  # open, in_progress, review, closed
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Engineering AI specific fields
    prompt_for_engineering_ai: Optional[str] = None
    engineering_response: Optional[str] = None
    review_notes: Optional[str] = None
    
    # Review iteration tracking
    review_iteration: int = 1
    last_review_prompt: Optional[str] = None
    
    def __post_init__(self):
        if self.updated_at == datetime.now():
            self.updated_at = datetime.now()


class TicketManager:
    """Manages ticket storage, observation, and lifecycle."""
    
    def __init__(self, tickets_file: str = "tickets.json"):
        self.tickets_file = tickets_file
        self.tickets: dict[str, Ticket] = {}
        self._load_tickets()
    
    def _load_tickets(self):
        """Load tickets from storage."""
        if os.path.exists(self.tickets_file):
            with open(self.tickets_file, 'r') as f:
                data = json.load(f)
                for ticket_id, ticket_data in data.items():
                    self.tickets[ticket_id] = Ticket(**ticket_data)
    
    def _save_tickets(self):
        """Save tickets to storage."""
        data = {tid: {k: v for k, v in vars(ticket).items() 
                     if not k.startswith('_')} 
                 for tid, ticket in self.tickets.items()}
        with open(self.tickets_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def create_ticket(self, title: str, description: str, 
                     priority: str = "medium") -> Ticket:
        """Create a new ticket from a user prompt."""
        ticket = Ticket(
            id=f"TICKET-{len(self.tickets) + 1:04d}",
            title=title,
            description=description,
            priority=priority
        )
        self.tickets[ticket.id] = ticket
        self._save_tickets()
        return ticket
    
    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Retrieve a ticket by ID."""
        return self.tickets.get(ticket_id)
    
    def update_ticket_status(self, ticket_id: str, status: str) -> bool:
        """Update ticket status (open -> in_progress -> review -> closed)."""
        ticket = self.get_ticket(ticket_id)
        if ticket:
            ticket.status = status
            ticket.updated_at = datetime.now()
            self._save_tickets()
            return True
        return False
    
    def observe_ticket(self, ticket_id: str) -> Ticket:
        """Observe and log current state of a ticket."""
        ticket = self.get_ticket(ticket_id)
        if ticket:
            ticket.updated_at = datetime.now()
            self._save_tickets()
        return ticket


class PromptConverter:
    """Converts user prompts into structured tickets for engineering AI."""
    
    def __init__(self, ticket_manager):
        self.templating_patterns = {
            "feature": "Implement the following feature:\n\n{description}\n\nPriority: {priority}",
            "bug_fix": "Fix the following bug:\n\n{description}\n\nExpected behavior: {expected_behavior}\n\nActual behavior: {actual_behavior}",
            "refactor": "Refactor the following code:\n\n{description}\n\nGoal: {goal}",
        }
        self.ticket_manager = ticket_manager
    
    def convert_prompt_to_ticket(self, user_prompt: str) -> Ticket:
        """Convert a raw user prompt into a ticket."""
        # Extract key information from the prompt
        title = self._extract_title(user_prompt)
        description = self._extract_description(user_prompt)
        
        priority = self._extract_priority(user_prompt)
        
        ticket = self.ticket_manager.create_ticket(title, description, priority)
        
        # Set engineering AI prompt
        ticket.prompt_for_engineering_ai = self._format_engineering_prompt(ticket)
        
        return ticket
    
    def _extract_title(self, prompt: str) -> str:
        """Extract title from user prompt."""
        import re
        # Look for patterns like "Add feature X", "Fix bug Y"
        match = re.search(r'(?:add|implement|create|build|fix|resolve|refactor)(?:\s+\w+)?', prompt, re.IGNORECASE)
        if match:
            return match.group(0).title()
        # Default title extraction
        words = prompt.split()
        if len(words) > 3:
            return ' '.join(words[:2]).title()
        return prompt.title()
    
    def _extract_description(self, prompt: str) -> str:
        """Extract detailed description from user prompt."""
        # Remove title-like parts and keep the rest
        import re
        title_match = re.search(r'(?:add|implement|create|build|fix|resolve|refactor)(?:\s+\w+)?', prompt, re.IGNORECASE)
        if title_match:
            desc = prompt[title_match.end():]
            return desc.strip()
        return prompt
    
    def _extract_priority(self, prompt: str) -> str:
        """Extract priority from user prompt."""
        import re
        match = re.search(r'(?:low|medium|high|critical)(?:\s+)?', prompt, re.IGNORECASE)
        if match:
            return match.group(0).lower()
        return "medium"
    
    def _format_engineering_prompt(self, ticket: Ticket) -> str:
        """Format the prompt specifically for engineering AI."""
        # Add technical context and structure
        base = f"""# Engineering Task Ticket

## Summary
{ticket.title}

## Description
{ticket.description}

## Priority
{ticket.priority}

## Status
{ticket.status}

## Review Iteration
Iteration {ticket.review_iteration}

---

## Technical Requirements

Please implement the following based on the ticket details. Provide:
1. Code changes with explanations
2. Test cases if applicable
3. Any breaking changes or migration notes

"""
        return base


class EngineeringAIInterface:
    """Interface for delivering tickets to engineering AI and receiving responses."""
    
    def __init__(self):
        self.responses: dict[str, str] = {}
    
    def deliver_ticket(self, ticket: Ticket) -> str:
        """Deliver a ticket to engineering AI and return response."""
        prompt = ticket.prompt_for_engineering_ai
        
        # Engineering AI response
        response = agent_code(prompt)
        
        ticket.engineering_response = response
        ticket.updated_at = datetime.now()
        
        return response
    
    def get_response(self, ticket_id: str) -> Optional[str]:
        """Retrieve engineering AI's response for a ticket."""
        return self.responses.get(ticket_id)


class ReviewAgent:
    """Reviews engineering AI work and can rewrite prompts if needed."""
    
    def __init__(self):
        self.review_history: dict[str, list] = {}
    
    def review_ticket(self, ticket: Ticket) -> str:
        """Review engineering AI's work on a ticket."""
        response = ticket.engineering_response
        
        # Analyze the response against requirements
        issues = self._analyze_response(ticket, response)
        
        if issues:
            return f"REVIEW REQUIRED: Found {len(issues)} issue(s). Rewrite prompt.\n\n{issues}"
        else:
            return "REVIEW PASSED: Implementation meets requirements."
    
    def _analyze_response(self, ticket: Ticket, response: str) -> list:
        """Analyze engineering AI's response for issues."""
        issues = []
        
        # Check if response addresses the ticket description
        if not response.lower().contains(ticket.description.lower()):
            issues.append("Response does not address key requirements")
        
        # Check priority alignment
        if ticket.priority == "critical" and "minor" in response.lower():
            issues.append("Response tone doesn't match critical priority")
        
        return issues
    
    def rewrite_prompt(self, ticket: Ticket) -> str:
        """Rewrite the prompt for a ticket based on review feedback."""
        # Generate improved prompt
        new_prompt = self._generate_improved_prompt(ticket)
        
        ticket.last_review_prompt = new_prompt
        ticket.review_iteration += 1
        
        return new_prompt
    
    def _generate_improved_prompt(self, ticket: Ticket) -> str:
        """Generate an improved prompt based on review feedback."""
        # In production, this would use LLM to generate better prompts
        base = f"""# Engineering Task - Iteration {ticket.review_iteration}

## Summary
{ticket.title}

## Description
{ticket.description}

## Priority
{ticket.priority}

## Previous Issues (from review)
- {ticket.review_notes or "No specific issues noted"}

Please ensure your implementation:
1. Addresses all requirements from the description
2. Maintains code quality standards
3. Includes appropriate tests
4. Documents any breaking changes

"""
        return base


class PMAgent:
    """Main Product Manager Agent that orchestrates the workflow."""
    
    def __init__(self):
        self.ticket_manager = TicketManager()
        self.prompt_converter = PromptConverter(self.ticket_manager)
        self.engineering_ai = EngineeringAIInterface()
        self.review_agent = ReviewAgent()
    
    def create_ticket_from_prompt(self, user_input: str) -> Ticket:
        """Create a ticket from a raw user prompt."""
        ticket = self.prompt_converter.convert_prompt_to_ticket(user_input)
        return ticket
    
    def deliver_to_engineering_ai(self, ticket: Ticket) -> str:
        """Deliver a ticket to engineering AI and get response."""
        response = self.engineering_ai.deliver_ticket(ticket)
        return response
    
    def review_work(self, ticket_id: str) -> str:
        """Review engineering AI's work on a ticket."""
        ticket = self.ticket_manager.get_ticket(ticket_id)
        if not ticket:
            return "Ticket not found."
        
        review_result = self.review_agent.review_ticket(ticket)
        return review_result
    
    def rewrite_prompt(self, ticket_id: str) -> str:
        """Rewrite the prompt for a ticket based on review feedback."""
        ticket = self.ticket_manager.get_ticket(ticket_id)
        if not ticket:
            return "Ticket not found."
        
        new_prompt = self.review_agent.rewrite_prompt(ticket)
        return new_prompt
    
    def update_ticket(self, ticket_id: str, updates: dict) -> bool:
        """Update a ticket with new information."""
        ticket = self.ticket_manager.get_ticket(ticket_id)
        if not ticket:
            return False
        
        for key, value in updates.items():
            setattr(ticket, key, value)
        
        ticket.updated_at = datetime.now()
        self.ticket_manager._save_tickets()
        return True
    
    def get_all_tickets(self) -> list[Ticket]:
        """Get all tickets."""
        return list(self.ticket_manager.tickets.values())


def main():
    """Main entry point demonstrating PM agent workflow."""
    
    pm = PMAgent()
    
    # Example workflow
    print("=== PM Agent System Demo ===\n")
    
    # 1. User provides a prompt
    user_prompt = " ".join(sys.argv[1:])
    print(f"User: {user_prompt}")
    
    # 2. Create ticket from prompt
    ticket = pm.create_ticket_from_prompt(user_prompt)
    print(f"\nTicket created: {ticket.id} - {ticket.title}")
    print(f"Status: {ticket.status}, Priority: {ticket.priority}")
    
    # 3. Deliver to engineering AI
    print("\nDelivering to Engineering AI...")
    response = pm.deliver_to_engineering_ai(ticket)
    print(f"\nEngineering AI Response:\n{response[:200]}...")
    
    # 4. Review the work
    print("\nReviewing engineering AI's work...")
    review_result = pm.review_work(ticket.id)
    print(f"Review Result: {review_result}")
    
    if "REVIEW REQUIRED" in review_result:
        print("\nRewriting prompt for iteration 2...")
        new_prompt = pm.rewrite_prompt(ticket.id)
        print(f"New Prompt:\n{new_prompt[:150]}...")
        
        # Update ticket with new prompt
        pm.update_ticket(ticket.id, {"prompt_for_engineering_ai": new_prompt})
    
    # 5. Get all tickets
    print("\n=== All Tickets ===")
    for t in pm.get_all_tickets():
        print(f"{t.id}: {t.title} - Status: {t.status}, Iteration: {t.review_iteration}")


if __name__ == "__main__":
    main()
