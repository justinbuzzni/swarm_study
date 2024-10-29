# agents/agents.py
from typing import Dict, List, TypedDict, Union, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from configs.prompts import (
    TRIAGE_SYSTEM_PROMPT,
    FLIGHT_MODIFICATION_PROMPT,
    FLIGHT_CANCEL_PROMPT,
    FLIGHT_CHANGE_PROMPT,
    LOST_BAGGAGE_PROMPT
)

# model = ChatAnthropic(model="claude-3-sonnet-20240229")


# LLM 초기화
model = ChatOpenAI(model="gpt-4o-mini")

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]
    current_agent: str
    context: Dict[str, Any]
    status: str

def create_triage_agent():
    def triage_agent(state: AgentState) -> AgentState:
        messages = state["messages"]
        last_message = messages[-1].content
        
        # Triage 로직
        prompt = ChatPromptTemplate.from_messages([
            ("system", TRIAGE_SYSTEM_PROMPT),
            ("human", last_message),
        ])
        
        try:
            response = model.invoke(prompt.format_messages(input=last_message))
            state["messages"].append(AIMessage(content=response.content))
            
            # 간단한 키워드 기반 라우팅
            if any(word in last_message.lower() for word in ["baggage", "luggage", "lost"]):
                state["current_agent"] = "lost_baggage"
            elif any(word in last_message.lower() for word in ["cancel", "change", "modify", "reschedule"]):
                state["current_agent"] = "flight_modification"
                
        except Exception as e:
            state["messages"].append(AIMessage(content="죄송합니다. 잠시 문제가 발생했습니다. 다시 한번 말씀해 주시겠어요?"))
            
        return state
    return triage_agent

def create_lost_baggage_agent():
    def lost_baggage_agent(state: AgentState) -> AgentState:
        messages = state["messages"]
        last_message = messages[-1].content
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", LOST_BAGGAGE_PROMPT),
            ("human", last_message),
        ])
        
        try:
            response = model.invoke(prompt.format_messages(input=last_message))
            state["messages"].append(AIMessage(content=response.content))
            state["status"] = "COMPLETED"
            
        except Exception as e:
            state["messages"].append(AIMessage(content="죄송합니다. 수화물 처리 중 문제가 발생했습니다. 다시 시도해 주시겠어요?"))
            
        return state
    return lost_baggage_agent

def create_flight_modification_agent():
    def flight_modification_agent(state: AgentState) -> AgentState:
        messages = state["messages"]
        last_message = messages[-1].content
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", FLIGHT_MODIFICATION_PROMPT),
            ("human", last_message),
        ])
        
        try:
            response = model.invoke(prompt.format_messages(input=last_message))
            state["messages"].append(AIMessage(content=response.content))
            
            if "cancel" in last_message.lower():
                state["current_agent"] = "flight_cancel"
            elif "change" in last_message.lower():
                state["current_agent"] = "flight_change"
                
        except Exception as e:
            state["messages"].append(AIMessage(content="죄송합니다. 항공편 변경 처리 중 문제가 발생했습니다. 다시 말씀해 주시겠어요?"))
            
        return state
    return flight_modification_agent

def create_flight_cancel_agent():
    def flight_cancel_agent(state: AgentState) -> AgentState:
        messages = state["messages"]
        last_message = messages[-1].content
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", FLIGHT_CANCEL_PROMPT),
            ("human", last_message),
        ])
        
        try:
            response = model.invoke(prompt.format_messages(input=last_message))
            state["messages"].append(AIMessage(content=response.content))
            state["status"] = "COMPLETED"
            
        except Exception as e:
            state["messages"].append(AIMessage(content="죄송합니다. 항공편 취소 처리 중 문제가 발생했습니다. 다시 시도해 주시겠어요?"))
            
        return state
    return flight_cancel_agent

def create_flight_change_agent():
    def flight_change_agent(state: AgentState) -> AgentState:
        messages = state["messages"]
        last_message = messages[-1].content
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", FLIGHT_CHANGE_PROMPT),
            ("human", last_message),
        ])
        
        try:
            response = model.invoke(prompt.format_messages(input=last_message))
            state["messages"].append(AIMessage(content=response.content))
            state["status"] = "COMPLETED"
            
        except Exception as e:
            state["messages"].append(AIMessage(content="죄송합니다. 항공편 변경 처리 중 문제가 발생했습니다. 다시 시도해 주시겠어요?"))
            
        return state
    return flight_change_agent