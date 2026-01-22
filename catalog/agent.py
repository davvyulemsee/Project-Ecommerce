import asyncio

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from typing import TypedDict, List, Union, Annotated, Sequence, Optional
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
import chainlit as cl
from pydantic import Field
import requests
from pathlib import Path

# load_dotenv()

# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


# load_dotenv(r"C:\Users\Santan\PycharmProjects\PythonProject\project1\.env")
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
#
#
# groq_api_key = os.getenv("GROQ_API_KEY")
#
#
# model = ChatGroq(model="openai/gpt-oss-20b", temperature = 0, api_key=groq_api_key)

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'
if not env_path.is_file():
    env_path = BASE_DIR.parent / '.env'

load_dotenv(env_path)

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("No GROQ_API_KEY! Check .env path.")

model = ChatGroq(model="openai/gpt-oss-20b", temperature=0, api_key=groq_api_key)

API_BASE = "http://localhost:8000/catalog"

@tool
def search_products(
        query: str = Field(..., description = "Main search keywords(name, description, category)"),
        category: Optional[str] = Field(None, description="Optional category"),
        limit: int = Field(5, description = "Number of results to show."),
) -> str:
    """Search tool for searching products in store"""
    params = {"q":query, "limit": min(limit, 10)}

    if category:
        params["category"] = category

    try:
        resp = requests.get(f"{API_BASE}/api/search/", params = params, timeout = 5)
        data = resp.json()
        if not data.get("content"):
            return " No products found. Try another product."

        return str(data)
        # return f"Status: {resp.status_code}\nContent-Type: {resp.headers.get('Content-Type')}\nRaw body: {resp.text}"
    except Exception as e:
        return f"Error: {e}"



tools_list = [search_products]


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly and concise e-commerce customer support assistant.
You help users find products, answer questions about orders, shipping, returns, etc.

Rules:
- Be helpful, polite and short unless more detail is needed
- Always search products when user is looking for items
- If you're not sure → ask clarifying questions
- Never hallucinate product information — always use tools
- If user asks something you cannot help with, say so politely
"""),
    MessagesPlaceholder("messages"),
])

llm = prompt | model.bind_tools(tools_list)


def safe_invoke(messages):
    """
    Force-rebuild every message to make sure we never pass legacy-style HumanMessage/AIMessage
    """
    fixed = []
    for msg in messages:
        if isinstance(msg, BaseMessage):
            # Re-create from scratch to avoid legacy constructor issues
            if msg.type == "human":
                fixed.append(HumanMessage(content=msg.content, additional_kwargs=msg.additional_kwargs))
            elif msg.type == "ai":
                fixed.append(AIMessage(content=msg.content, additional_kwargs=msg.additional_kwargs))
            elif msg.type == "system":
                fixed.append(SystemMessage(content=msg.content, additional_kwargs=msg.additional_kwargs))
            elif msg.type == "tool":
                fixed.append(ToolMessage(content=msg.content, tool_call_id=msg.tool_call_id))
            else:
                # fallback
                fixed.append(HumanMessage(content=str(msg.content)))
        elif isinstance(msg, tuple) and len(msg) == 2:
            role, content = msg
            if role in ("user", "human"):
                fixed.append(HumanMessage(content=content))
            elif role in ("assistant", "ai"):
                fixed.append(AIMessage(content=content))
            else:
                fixed.append(HumanMessage(content=str(content)))
        elif isinstance(msg, str):
            fixed.append(HumanMessage(content=msg))
        else:
            fixed.append(HumanMessage(content=str(msg)))

    # Now invoke with the cleaned list
    return llm.invoke(fixed)


def agent(state: AgentState):
    response = safe_invoke(state['messages'])
    return {"messages": [response]}

graph = StateGraph(AgentState)

graph.add_node("agent_node", agent)

tools = ToolNode(tools_list)

graph.add_node("tools", tools)

graph.add_edge(START, "agent_node")

graph.add_conditional_edges("agent_node", tools_condition)

graph.add_edge("tools", "agent_node")


memory = MemorySaver()

# app = graph.compile(checkpointer=memory)
app = graph.compile()


# config = {"configurable": {"thread_id": "david-test-001"}}
#
# inputs = {"messages": [("user", "I'm looking for wireless earbuds under 100 dollars")]}
# for chunk in app.stream(inputs, config, stream_mode="values"):
#     chunk["messages"][-1].pretty_print()




















