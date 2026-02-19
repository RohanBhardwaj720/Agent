from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import AzureChatOpenAI
import operator
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage
from langchain_core.messages import HumanMessage, AIMessage


load_dotenv()


class chatbot(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]



llm = AzureChatOpenAI(
    azure_deployment="o4-mini",
    api_version="2024-12-01-preview"
)

def LLM(state: chatbot) -> chatbot:
    response = llm.invoke(state["messages"])
    return {"messages": [AIMessage(response.content)]}

graph = StateGraph(chatbot)
graph.add_node("LLM", LLM)
graph.add_edge(START, "LLM")
graph.add_edge("LLM", END)

checkpointer = InMemorySaver()
g = graph.compile(checkpointer= checkpointer)
config = {"configurable": {"thread_id": "1"}}

print(g.invoke({"messages" :[HumanMessage("hi")]}, config=config))

print(g.invoke({"messages" :[HumanMessage("what is my name")]}, config=config))