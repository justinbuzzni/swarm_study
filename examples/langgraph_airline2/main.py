# main.py
from typing import Dict, List, Annotated, Union
from langgraph.graph import StateGraph, END
from agents.agents import (
    AgentState,
    create_triage_agent,
    create_flight_modification_agent,
    create_flight_cancel_agent,
    create_flight_change_agent,
    create_lost_baggage_agent
)
from configs.config import DEFAULT_CONTEXT
from langchain_core.messages import HumanMessage, AIMessage

def should_end(state: AgentState) -> bool:
    """Determine if we should end the conversation"""
    return state["status"] == "COMPLETED"

def route_from_triage(state: AgentState) -> str:
    """Route from triage node"""
    if should_end(state):
        return "END"
    current_agent = state["current_agent"]
    if current_agent in ["flight_modification", "lost_baggage"]:
        return current_agent
    return "triage"

def route_from_flight_modification(state: AgentState) -> str:
    """Route from flight modification node"""
    if should_end(state):
        return "END"
    current_agent = state["current_agent"]
    if current_agent in ["flight_cancel", "flight_change"]:
        return current_agent
    return "flight_modification"

def route_to_triage(state: AgentState) -> str:
    """Route back to triage"""
    if should_end(state):
        return "END"
    return "triage"

def create_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("triage", create_triage_agent())
    workflow.add_node("flight_modification", create_flight_modification_agent())
    workflow.add_node("flight_cancel", create_flight_cancel_agent())
    workflow.add_node("flight_change", create_flight_change_agent())
    workflow.add_node("lost_baggage", create_lost_baggage_agent())
    
    # Add edges for triage
    workflow.add_conditional_edges(
        "triage",
        route_from_triage,
        {
            "flight_modification": "flight_modification",
            "lost_baggage": "lost_baggage",
            "triage": "triage",
            "END": END
        }
    )
    
    # Add edges for flight_modification
    workflow.add_conditional_edges(
        "flight_modification",
        route_from_flight_modification,
        {
            "flight_cancel": "flight_cancel",
            "flight_change": "flight_change",
            "flight_modification": "flight_modification",
            "END": END
        }
    )
    
    # Add edges for other nodes
    for node in ["flight_cancel", "flight_change", "lost_baggage"]:
        workflow.add_conditional_edges(
            node,
            route_to_triage,
            {
                "triage": "triage",
                "END": END
            }
        )
    
    # Set entry point
    workflow.set_entry_point("triage")
    
    return workflow.compile()

def main():
    # Initialize workflow
    workflow = create_workflow()
    
    # Initialize state
    initial_state: AgentState = {
        "messages": [],
        "current_agent": "triage",
        "context": DEFAULT_CONTEXT,
        "status": "ACTIVE"
    }
    
    print("Welcome to Flight Airlines Customer Service! How can I help you today?")
    
    # Main conversation loop
    while True:
        try:
            # 현재 상태 출력
            print(f"\n[Debug] Current State:")
            print(f"Current Agent: {initial_state['current_agent']}")
            print(f"Status: {initial_state['status']}")
            print(f"Message Count: {len(initial_state['messages'])}\n")
            
            user_input = input("User: ")
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Thank you for using Flight Airlines Customer Service. Goodbye!")
                break
            
            # Update state with user message
            initial_state["messages"].append(HumanMessage(content=user_input))
            
            # Process through workflow
            result = workflow.invoke(initial_state)
            
            # Update state
            initial_state = result
            
            # Print agent response
            if result["messages"]:
                last_message = result["messages"][-1]
                if isinstance(last_message, AIMessage):
                    print(f"Agent: {last_message.content}")
            
            # Check if conversation is complete
            if result.get("status") == "COMPLETED":
                print("Is there anything else I can help you with?")
                initial_state["status"] = "ACTIVE"
                initial_state["current_agent"] = "triage"
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            initial_state = {
                "messages": [],
                "current_agent": "triage",
                "context": DEFAULT_CONTEXT,
                "status": "ACTIVE"
            }
            print("Starting a new conversation. How can I help you?")

if __name__ == "__main__":
    main()