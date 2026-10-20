"""
Tests for PM Agent System
Tests the Product Manager agent's ticket management, prompt conversion, 
engineering AI interface, and review capabilities.
"""

import pytest
from datetime import datetime
from pm.main import (
    Ticket,
    TicketManager,
    PromptConverter,
    EngineeringAIInterface,
    ReviewAgent,
    PMAgent
)


class TestTicket:
    """Tests for the Ticket data class."""
    
    def test_ticket_creation(self):
        """Test basic ticket creation with default values."""
        ticket = Ticket(
            id="TICKET-001",
            title="Test Feature",
            description="Test description"
        )
        
        assert ticket.id == "TICKET-001"
        assert ticket.title == "Test Feature"
        assert ticket.description == "Test description"
        assert ticket.priority == "medium"
        assert ticket.status == "open"
    
    def test_ticket_with_custom_priority(self):
        """Test ticket creation with custom priority."""
        ticket = Ticket(
            id="TICKET-002",
            title="Critical Feature",
            description="Important feature",
            priority="critical"
        )
        
        assert ticket.priority == "critical"
    
    def test_ticket_with_custom_status(self):
        """Test ticket creation with custom status."""
        ticket = Ticket(
            id="TICKET-003",
            title="In Progress Task",
            description="Task in progress",
            status="in_progress"
        )
        
        assert ticket.status == "in_progress"


class TestTicketManager:
    """Tests for the TicketManager class."""
    
    def test_create_ticket(self):
        """Test creating a new ticket."""
        manager = TicketManager()
        ticket = manager.create_ticket(
            title="Add user management",
            description="Implement CRUD operations for users",
            priority="high"
        )
        
        assert ticket.id.startswith("TICKET-")
        assert ticket.title == "Add user management"
        assert ticket.description == "Implement CRUD operations for users"
        assert ticket.priority == "high"
    
    def test_get_ticket(self):
        """Test retrieving a ticket by ID."""
        manager = TicketManager()
        manager.create_ticket(
            title="Test Feature",
            description="Test description",
            priority="medium"
        )
        
        ticket = manager.get_ticket("TICKET-001")
        assert ticket is not None
        assert ticket.title == "Test Feature"
    
    def test_update_ticket_status(self):
        """Test updating ticket status."""
        manager = TicketManager()
        manager.create_ticket(
            title="Feature",
            description="Description",
            priority="medium"
        )
        
        initial_status = manager.get_ticket("TICKET-001").status
        
        result = manager.update_ticket_status("TICKET-001", "in_progress")
        
        assert result is True
        assert manager.get_ticket("TICKET-001").status == "in_progress"
    
    def test_update_ticket_status_invalid(self):
        """Test updating non-existent ticket status."""
        manager = TicketManager()
        
        result = manager.update_ticket_status("INVALID", "open")
        
        assert result is False


class TestPromptConverter:
    """Tests for the PromptConverter class."""
    
    def test_convert_simple_prompt(self):
        """Test converting a simple prompt to ticket."""
        converter = PromptConverter()
        prompt = "Add login functionality"
        
        ticket = converter.convert_prompt_to_ticket(prompt)
        
        assert ticket.title == "Add login functionality" or "Login" in ticket.title
        assert ticket.status == "open"
    
    def test_convert_priority_prompt(self):
        """Test converting a prompt with priority."""
        converter = PromptConverter()
        prompt = "Implement critical feature X - high priority"
        
        ticket = converter.convert_prompt_to_ticket(prompt)
        
        assert ticket.priority == "high"
    
    def test_convert_bug_fix_prompt(self):
        """Test converting a bug fix prompt."""
        converter = PromptConverter()
        prompt = "Fix the authentication issue where tokens expire too quickly"
        
        ticket = converter.convert_prompt_to_ticket(prompt)
        
        assert "fix" in ticket.title.lower() or "bug" in ticket.title.lower()


class TestEngineeringAIInterface:
    """Tests for the EngineeringAIInterface class."""
    
    def test_deliver_ticket(self):
        """Test delivering a ticket to engineering AI."""
        manager = TicketManager()
        manager.create_ticket(
            title="Test Feature",
            description="Test description",
            priority="medium"
        )
        
        interface = EngineeringAIInterface()
        response = interface.deliver_ticket(manager.get_ticket("TICKET-001"))
        
        assert response is not None
        assert "Engineering AI Response" in response or "Response" in response
    
    def test_get_response(self):
        """Test retrieving engineering AI response."""
        manager = TicketManager()
        manager.create_ticket(
            title="Feature",
            description="Description",
            priority="medium"
        )
        
        interface = EngineeringAIInterface()
        interface.deliver_ticket(manager.get_ticket("TICKET-001"))
        
        response = interface.get_response("TICKET-001")
        
        assert response is not None


class TestReviewAgent:
    """Tests for the ReviewAgent class."""
    
    def test_review_ticket(self):
        """Test reviewing a ticket's engineering work."""
        manager = TicketManager()
        manager.create_ticket(
            title="Feature",
            description="Description",
            priority="medium"
        )
        
        manager.get_ticket("TICKET-001").engineering_response = "Implementation details..."
        
        agent = ReviewAgent()
        result = agent.review_ticket(manager.get_ticket("TICKET-001"))
        
        assert result is not None
    
    def test_rewrite_prompt(self):
        """Test rewriting a ticket's prompt."""
        manager = TicketManager()
        manager.create_ticket(
            title="Feature",
            description="Description",
            priority="medium"
        )
        
        agent = ReviewAgent()
        new_prompt = agent.rewrite_prompt(manager.get_ticket("TICKET-001"))
        
        assert new_prompt is not None


class TestPMAgent:
    """Tests for the main PMAgent class."""
    
    def test_create_ticket_from_prompt(self):
        """Test creating a ticket from user prompt."""
        pm = PMAgent()
        prompt = "Add user authentication with JWT tokens"
        
        ticket = pm.create_ticket_from_prompt(prompt)
        
        assert ticket is not None
        assert ticket.title == "Add user authentication with JWT tokens" or "Authentication" in ticket.title
    
    def test_deliver_to_engineering_ai(self):
        """Test delivering a ticket to engineering AI."""
        pm = PMAgent()
        prompt = "Implement feature X"
        
        ticket = pm.create_ticket_from_prompt(prompt)
        response = pm.deliver_to_engineering_ai(ticket)
        
        assert response is not None
    
    def test_review_work(self):
        """Test reviewing engineering AI's work."""
        pm = PMAgent()
        prompt = "Add feature"
        
        ticket = pm.create_ticket_from_prompt(prompt)
        pm.deliver_to_engineering_ai(ticket)
        
        review_result = pm.review_work(ticket.id)
        
        assert review_result is not None
    
    def test_rewrite_prompt(self):
        """Test rewriting a ticket's prompt."""
        pm = PMAgent()
        prompt = "Add feature"
        
        ticket = pm.create_ticket_from_prompt(prompt)
        pm.deliver_to_engineering_ai(ticket)
        
        new_prompt = pm.rewrite_prompt(ticket.id)
        
        assert new_prompt is not None
    
    def test_update_ticket(self):
        """Test updating a ticket."""
        pm = PMAgent()
        prompt = "Add feature"
        
        ticket = pm.create_ticket_from_prompt(prompt)
        
        result = pm.update_ticket(ticket.id, {"priority": "high"})
        
        assert result is True
        assert ticket.priority == "high"
    
    def test_get_all_tickets(self):
        """Test getting all tickets."""
        pm = PMAgent()
        prompt1 = "Feature 1"
        prompt2 = "Feature 2"
        
        ticket1 = pm.create_ticket_from_prompt(prompt1)
        ticket2 = pm.create_ticket_from_prompt(prompt2)
        
        tickets = pm.get_all_tickets()
        
        assert len(tickets) == 2


class TestIntegration:
    """Integration tests for the complete PM workflow."""
    
    def test_full_workflow(self):
        """Test the complete PM workflow from prompt to review."""
        pm = PMAgent()
        
        # Step 1: User provides prompt
        user_prompt = "Add JWT authentication with token refresh"
        
        # Step 2: Create ticket
        ticket = pm.create_ticket_from_prompt(user_prompt)
        
        assert ticket is not None
        assert ticket.status == "open"
        
        # Step 3: Deliver to engineering AI
        response = pm.deliver_to_engineering_ai(ticket)
        
        assert response is not None
        
        # Step 4: Review work
        review_result = pm.review_work(ticket.id)
        
        assert review_result is not None
        
        # Step 5: If needed, rewrite prompt
        if "REVIEW REQUIRED" in review_result:
            new_prompt = pm.rewrite_prompt(ticket.id)
            assert new_prompt is not None
            
            # Update ticket with new prompt
            pm.update_ticket(ticket.id, {"prompt_for_engineering_ai": new_prompt})


class TestTicketStorage:
    """Tests for ticket storage and persistence."""
    
    def test_ticket_persistence(self):
        """Test that tickets are persisted to file."""
        manager = TicketManager()
        manager.create_ticket(
            title="Persistent Feature",
            description="Description",
            priority="high"
        )
        
        # Reload from file
        manager2 = TicketManager("tickets.json")
        ticket = manager2.get_ticket("TICKET-001")
        
        assert ticket is not None
        assert ticket.title == "Persistent Feature"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
