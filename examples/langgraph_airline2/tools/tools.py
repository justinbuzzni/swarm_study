# tools/tools.py
from langchain.tools import Tool
from typing import Optional

def escalate_to_agent(reason: Optional[str] = None) -> str:
    return f"Escalating to agent: {reason}" if reason else "Escalating to agent"

def valid_to_change_flight() -> str:
    return "Customer is eligible to change flight"

def change_flight() -> str:
    return "Flight was successfully changed!"

def initiate_refund() -> str:
    return "Refund initiated"

def initiate_flight_credits() -> str:
    return "Successfully initiated flight credits"

def initiate_baggage_search() -> str:
    return "Baggage was found!"

def create_tools():
    return [
        Tool(
            name="escalate_to_agent",
            func=escalate_to_agent,
            description="Escalate the conversation to a human agent"
        ),
        Tool(
            name="valid_to_change_flight",
            func=valid_to_change_flight,
            description="Check if customer is eligible for flight change"
        ),
        Tool(
            name="change_flight",
            func=change_flight,
            description="Process flight change"
        ),
        Tool(
            name="initiate_refund",
            func=initiate_refund,
            description="Process refund"
        ),
        Tool(
            name="initiate_flight_credits",
            func=initiate_flight_credits,
            description="Issue flight credits"
        ),
        Tool(
            name="initiate_baggage_search",
            func=initiate_baggage_search,
            description="Start baggage search process"
        )
    ]