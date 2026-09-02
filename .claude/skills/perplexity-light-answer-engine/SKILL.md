---
name: perplexity-light-answer-engine
description: Build a Perplexity-style AI answer engine ("Perplexity Light") — a web search + LLM synthesis app — using LangGraph, the Tavily search API, GPT-4, and FastAPI. Use when Tyler wants to build a search-and-answer chatbot, an "ask anything" research tool, a RAG-over-the-web app, or a Perplexity/SearchGPT clone, or asks how to wire Tavily + LangGraph agents + FastAPI together. Covers the agent-as-a-graph pattern (nodes/edges/conditional edges) instead of the legacy AgentExecutor loop.
---

# Perplexity Light — Web Answer Engine

Build an app that takes a user question, searches the live web, and returns a synthesized, source-cited answer — the core of Perplexity / SearchGPT.

**Stack:** LangGraph (agent orchestration as a graph) · Tavily (LLM-native web search API) · GPT-4 (`gpt-4-1106-preview`) · FastAPI + Bootstrap 5.3 frontend.

> Source: "AI Anytime" — *Build a Perplexity-style app with LangGraph + Tavily* (https://www.youtube.com/watch?v=O0fpDUwxUEg). "Tavily" is the search API the video calls "Tavi/tivoly."

-----

## Why LangGraph (not AgentExecutor)

The old LangChain way ran agents in a hidden `while` loop via `AgentExecutor`. **LangGraph** instead models the agent as an explicit **graph of nodes and edges**, giving you:

- Explicit, inspectable control flow (you decide when to call a tool vs. finish).
- Custom **cyclical** behavior (search → reason → search again → answer).
- Easier debugging — you can trace every intermediate step.

The loop here is just two nodes — `agent` and `tools` — wired so the agent keeps calling the search tool until it decides it has enough to answer.

-----

## Prerequisites

```bash
pip install langgraph langchain langchain-openai langchain-community langchainhub tavily-python
```

Two API keys (store as env vars / secrets, never hardcode):

- `OPENAI_API_KEY`
- `TAVILY_API_KEY` — free tier gives **1,000 requests**, plenty for an MVP. Sign up at tavily.com.

```python
import os
# e.g. from Colab: from google.colab import userdata; os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]  = "..."
os.environ["TAVILY_API_KEY"]  = "..."
```

-----

## Step 1 — Tool, prompt, LLM, runnable agent

```python
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent

tools  = [TavilySearchResults(max_results=1)]          # bump max_results for more sources
prompt = hub.pull("hwchase17/openai-functions-agent")  # Harrison Chase's stock functions-agent prompt
llm    = ChatOpenAI(model="gpt-4-1106-preview")

agent_runnable = create_openai_functions_agent(llm, tools, prompt)
```

> Gotcha from the video: the import is `langchain_community.tools.tavily_search` and the class is `TavilySearchResults` (plural "Results", "functions" plural in `create_openai_functions_agent`). Make sure `langchain-community` is actually installed or these imports fail confusingly.

-----

## Step 2 — Agent node + state plumbing

The graph state is a dict carrying `input`, `agent_outcome`, and `intermediate_steps`.

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.agents import AgentFinish

# agent node: run the LLM, store its decision under `agent_outcome`
agent = RunnablePassthrough.assign(agent_outcome = agent_runnable)
```

-----

## Step 3 — Tool-execution node

```python
def execute_tools(data):
    agent_action = data.pop("agent_outcome")
    tools_to_use = {t.name: t for t in tools}[agent_action.tool]
    observation  = tools_to_use.invoke(agent_action.tool_input)
    data["intermediate_steps"].append((agent_action, observation))
    return data
```

-----

## Step 4 — Conditional router

```python
def should_continue(data):
    if isinstance(data["agent_outcome"], AgentFinish):
        return "exit"      # agent is done -> END
    return "continue"      # agent wants a tool -> tools node
```

-----

## Step 5 — Build, wire, and compile the graph

```python
from langgraph.graph import Graph, END

workflow = Graph()
workflow.add_node("agent", agent)
workflow.add_node("tools", execute_tools)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",                          # start node
    should_continue,                  # router fn
    {"continue": "tools", "exit": END}
)
workflow.add_edge("tools", "agent")   # after a tool runs, loop back to the agent

chain = workflow.compile()            # MUST compile before invoke
```

-----

## Step 6 — Run it

```python
result = chain.invoke({
    "input": "Tell me five startups working in drug discovery",
    "intermediate_steps": []          # start empty; gets appended to each loop
})
print(result["agent_outcome"])        # synthesized answer
# result["intermediate_steps"] holds the raw trace: tool queries + Tavily JSON + source URLs
```

Flow: question → Tavily web search → raw results fed as context → GPT-4 synthesizes a human-readable answer **with source URLs**.

-----

## Step 7 — Wrap in FastAPI

```python
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/process_query")
def process_query(query: str = Form(...)):
    result = chain.invoke({"input": query, "intermediate_steps": []})
    return {"answer": result["agent_outcome"], "trace": result["intermediate_steps"]}
```

**Frontend:** Bootstrap 5.3 (CDN) single page — a search box posting to `/process_query` via vanilla JS `fetch`, an answer card, and a collapsible accordion showing the raw trace (intermediate steps + source links). Swap in React/Flask/Node if preferred.

-----

## Customization knobs

- `TavilySearchResults(max_results=N)` — more sources per query.
- LLM `max_tokens` — raise it so long web context fits and answers aren't truncated.
- Add memory + `ChatOpenAI` conversation state to make it a multi-turn chatbot.
- Optional: LangSmith for full tracing (set `LANGCHAIN_API_KEY`).
- Always surface the **source URLs** Tavily returns — that's what makes it Perplexity-like and lets the user verify.

-----

## Common pitfalls (hit live in the tutorial)

- **Forgot `workflow.compile()`** → `NameError: chain is not defined`. Compile before invoking.
- **State key typos** (`agent_outcome`) silently break the router — keep keys consistent across all nodes.
- **`langchain-community` not installed** → Tavily import errors that look like wrong module paths. Install it explicitly.
- Re-run *all* cells and recompile after editing any node function — the graph captures the functions at compile time.
