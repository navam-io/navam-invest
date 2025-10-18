# Build a Basic Chatbot with LangGraph

## Prerequisites

- Access to an LLM with tool-calling features (OpenAI, Anthropic, Google Gemini)
- Python environment with LangGraph installed

## Installation

```bash
pip install -U langgraph langsmith
```

## Complete Tutorial Code

```python
from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Choose your LLM (example uses Anthropic)
llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
```

## Step-by-Step Breakdown

### Step 1: Define State

State is a TypedDict that manages message history:

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

**Key Points:**
- `messages`: List of conversation messages
- `add_messages`: Reducer that appends new messages to the list
- `Annotated`: Specifies how to update the messages field

### Step 2: Initialize StateGraph

Create the graph builder with the state schema:

```python
from langgraph.graph import StateGraph, START, END

graph_builder = StateGraph(State)
```

**Graph Components:**
- `StateGraph`: Main graph class
- `START`: Special node representing entry point
- `END`: Special node representing termination

### Step 3: Select Language Model

Choose an LLM provider:

```python
from langchain.chat_models import init_chat_model

# Anthropic
llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

# OpenAI
llm = init_chat_model("openai:gpt-4o")

# Google
llm = init_chat_model("google_genai:gemini-1.5-pro")
```

### Step 4: Create Chatbot Node

Define the chatbot function that processes messages:

```python
def chatbot(state: State):
    # Invoke LLM with current messages
    response = llm.invoke(state["messages"])
    # Return new message to be added to state
    return {"messages": [response]}
```

**Node Behavior:**
- Receives current state
- Invokes LLM with message history
- Returns updated state with new message

### Step 5: Add Graph Edges

Configure the graph structure:

```python
# Add chatbot node
graph_builder.add_node("chatbot", chatbot)

# Connect START to chatbot
graph_builder.add_edge(START, "chatbot")

# Connect chatbot to END
graph_builder.add_edge("chatbot", END)
```

**Graph Flow:**
```
START → chatbot → END
```

### Step 6: Compile Graph

Prepare the graph for execution:

```python
graph = graph_builder.compile()
```

## Running the Chatbot

### Basic Invocation

```python
# Single message
result = graph.invoke({
    "messages": [{"role": "user", "content": "Hello!"}]
})

print(result["messages"][-1].content)
```

### Streaming Updates

```python
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
```

### Interactive Loop

```python
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)

    except Exception as e:
        print(f"Error: {e}")
        break
```

## Advanced Features

### Adding System Prompt

```python
def chatbot(state: State):
    # Add system message
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ] + state["messages"]

    response = llm.invoke(messages)
    return {"messages": [response]}
```

### Message History Management

```python
def chatbot(state: State):
    # Limit message history
    messages = state["messages"][-10:]  # Keep last 10 messages

    response = llm.invoke(messages)
    return {"messages": [response]}
```

### Error Handling

```python
def chatbot(state: State):
    try:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}
    except Exception as e:
        error_message = {
            "role": "assistant",
            "content": f"I encountered an error: {str(e)}"
        }
        return {"messages": [error_message]}
```

## Understanding the Reducer

The `add_messages` reducer controls how messages are accumulated:

```python
from langgraph.graph.message import add_messages

# This reducer:
# 1. Takes existing messages list
# 2. Appends new messages
# 3. Returns combined list

messages: Annotated[list, add_messages]
```

### Custom Reducer Example

```python
def custom_message_reducer(existing: list, new: list) -> list:
    # Keep only last 5 messages
    combined = existing + new
    return combined[-5:]

class State(TypedDict):
    messages: Annotated[list, custom_message_reducer]
```

## Visualization

You can visualize the graph structure:

```python
from IPython.display import Image, display

# Generate graph visualization
display(Image(graph.get_graph().draw_mermaid_png()))
```

## Next Steps

After building a basic chatbot, continue learning with:

1. **Add Tools**: Integrate external tools (search, calculator, etc.)
2. **Add Memory**: Persist conversation across sessions
3. **Add Human-in-the-Loop**: Enable human oversight
4. **Customize State**: Add custom fields and logic
5. **Time Travel**: Navigate conversation history

## Key Concepts Learned

✅ **State Management**: Using TypedDict and reducers
✅ **Graph Structure**: Nodes, edges, START, END
✅ **Message Handling**: Accumulating conversation history
✅ **Node Functions**: Processing state and returning updates
✅ **Graph Compilation**: Preparing graph for execution

## Complete Working Example

```python
from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 1. Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Initialize graph
graph_builder = StateGraph(State)

# 3. Select LLM
llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

# 4. Create chatbot node
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 5. Add edges
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# 6. Compile
graph = graph_builder.compile()

# 7. Run
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

# Interactive loop
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        break
```

This basic chatbot forms the foundation for more complex agent workflows in LangGraph.
