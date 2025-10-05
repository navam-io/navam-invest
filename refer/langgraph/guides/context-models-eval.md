# LangGraph Context, Models, and Evaluation

## Context Engineering

### Overview
Context engineering involves providing the right information and tools to AI applications through three approaches: static runtime context, dynamic runtime context (state), and cross-conversation context (store).

### 1. Static Runtime Context

Immutable data passed at startup via `context` parameter.

```python
from dataclasses import dataclass

@dataclass
class ContextSchema:
    user_name: str
    risk_tolerance: str
    api_keys: dict

def investment_node(state: State, *, context: ContextSchema):
    # Access immutable context
    user_name = context.user_name
    risk_level = context.risk_tolerance

    # Customize behavior
    prompt = f"Analyze for {user_name} with {risk_level} risk tolerance"
    return process(prompt, state)

# Pass context at runtime
graph.invoke(
    {"messages": [...]},
    context={
        "user_name": "John Smith",
        "risk_tolerance": "moderate",
        "api_keys": {...}
    }
)
```

**Use Cases**: User metadata, database connections, API keys, configuration

---

### 2. Dynamic Runtime Context (State)

Mutable data that evolves during execution via state management.

```python
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages

class CustomState(TypedDict):
    messages: Annotated[list, add_messages]
    user_name: str
    portfolio_value: float

def analyze_node(state: CustomState):
    # Access mutable state
    user = state["user_name"]
    value = state["portfolio_value"]

    # Update state
    analysis = perform_analysis(value)

    return {
        "messages": [{"role": "assistant", "content": analysis}],
        "portfolio_value": updated_value
    }
```

**Use Cases**: Conversation history, intermediate results, short-term memory

---

### 3. Cross-Conversation Context (Store)

Persistent data spanning multiple conversations via memory store.

```python
from langgraph.store.base import BaseStore

def preference_node(state: State, *, store: BaseStore):
    user_id = state["user_id"]

    # Load long-term preferences
    prefs = store.get(
        namespace=["users", user_id],
        key="preferences"
    )

    # Use preferences
    risk_tolerance = prefs.value["risk_tolerance"]

    # Update preferences based on behavior
    store.put(
        namespace=["users", user_id],
        key="preferences",
        value={**prefs.value, "last_updated": datetime.now()}
    )

    return state
```

**Use Cases**: User profiles, preferences, historical interactions, long-term memory

---

## Model Integration

### Supported Providers

- **Anthropic**: Claude models
- **OpenAI**: GPT models
- **Azure OpenAI**: Enterprise OpenAI
- **Google**: Gemini models
- **AWS Bedrock**: Multiple providers

### Using init_chat_model()

```python
from langchain.chat_models import init_chat_model

# Quick initialization with provider:model format
llm = init_chat_model("anthropic:claude-3-7-sonnet-latest")
llm = init_chat_model("openai:gpt-4o")
llm = init_chat_model("google:gemini-2.0-flash-exp")

# With configuration
llm = init_chat_model(
    "anthropic:claude-3-5-sonnet-latest",
    temperature=0,
    max_tokens=2048
)
```

### Direct Model Instantiation

```python
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# Anthropic
model = ChatAnthropic(
    model="claude-3-7-sonnet-latest",
    temperature=0,
    max_tokens=2048,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# OpenAI
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### Model Configuration

```python
# Disable streaming
model = init_chat_model("anthropic:claude-3-7-sonnet-latest", disable_streaming=True)

# Add fallback models
primary = init_chat_model("openai:gpt-4o")
fallback = init_chat_model("anthropic:claude-3-5-sonnet-latest")
model_with_fallback = primary.with_fallbacks([fallback])

# Rate limiting
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=10,
    max_bucket_size=100
)
model = init_chat_model("openai:gpt-4o", rate_limiter=rate_limiter)
```

### Dynamic Model Selection

```python
def select_model(state, runtime):
    """Choose model based on context."""
    if runtime.context.provider == "anthropic":
        return anthropic_model.bind_tools(tools)
    elif runtime.context.provider == "openai":
        return openai_model.bind_tools(tools)
    else:
        return default_model.bind_tools(tools)

# Use in graph
def call_model(state: State, *, context):
    model = select_model(state, context)
    response = model.invoke(state["messages"])
    return {"messages": [response]}
```

### Bring Your Own Model

```python
from langchain_core.language_models import BaseChatModel

class CustomChatModel(BaseChatModel):
    """Custom model implementation."""

    def _generate(self, messages, stop=None, **kwargs):
        # Custom generation logic
        response = your_model_api.generate(messages)
        return ChatGeneration(message=AIMessage(content=response))

    async def _agenerate(self, messages, stop=None, **kwargs):
        # Async generation
        response = await your_model_api.agenerate(messages)
        return ChatGeneration(message=AIMessage(content=response))

# Use custom model
custom_model = CustomChatModel()
agent = create_react_agent(custom_model, tools=tools)
```

---

## Evaluation

### Overview
Evaluate agent performance using LangSmith and AgentEvals library.

### Setup

```bash
pip install -U agentevals langsmith
```

### Evaluation Methods

#### 1. Trajectory Matching

Compare sequence of tool calls against reference trajectories.

```python
from agentevals.trajectory.match import create_trajectory_match_evaluator

# Create evaluator
evaluator = create_trajectory_match_evaluator(
    trajectory_match_mode="superset"  # or "strict", "unordered", "subset"
)
```

**Matching Modes**:
- `superset`: Agent calls all expected tools (and possibly more)
- `strict`: Exact match of tool sequence
- `unordered`: All tools called, order doesn't matter
- `subset`: Agent calls subset of expected tools

#### 2. LLM-as-a-Judge

Use LLM to evaluate agent performance against reference outputs.

```python
from agentevals.trajectory.llm_as_judge import create_trajectory_llm_as_judge

evaluator = create_trajectory_llm_as_judge(
    prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
    model="openai:o3-mini"  # Evaluation model
)
```

#### 3. Reference Output Comparison

Compare final outputs against expected results.

```python
from agentevals.output import create_output_evaluator

evaluator = create_output_evaluator(
    comparison_fn=semantic_similarity,
    threshold=0.8
)
```

### Creating Datasets

```python
from langsmith import Client

client = Client()

# Create dataset
dataset = client.create_dataset(
    dataset_name="investment_analysis_test",
    description="Test cases for investment analysis agent"
)

# Add examples
client.create_examples(
    dataset_id=dataset.id,
    examples=[
        {
            "inputs": {"messages": [{"role": "user", "content": "Analyze AAPL"}]},
            "outputs": {
                "messages": [{
                    "role": "assistant",
                    "content": "Expected analysis...",
                    "tool_calls": [{"name": "get_stock_data", "args": {"symbol": "AAPL"}}]
                }]
            }
        },
        # More examples...
    ]
)
```

### Running Evaluations

```python
from langsmith import Client
from langgraph.prebuilt import create_react_agent
from agentevals.trajectory.match import create_trajectory_match_evaluator

# Initialize
client = Client()
agent = create_react_agent(model=llm, tools=tools)
evaluator = create_trajectory_match_evaluator(trajectory_match_mode="superset")

# Run evaluation
experiment_results = client.evaluate(
    lambda inputs: agent.invoke(inputs),
    data="investment_analysis_test",  # Dataset name
    evaluators=[evaluator],
    experiment_prefix="agent_v1"
)

# View results
print(f"Results: {experiment_results}")
```

### Custom Evaluators

```python
def custom_accuracy_evaluator(run, example):
    """Custom evaluation logic."""
    predicted = run.outputs["messages"][-1]["content"]
    expected = example.outputs["messages"][-1]["content"]

    # Custom scoring
    score = calculate_similarity(predicted, expected)

    return {
        "key": "accuracy",
        "score": score,
        "comment": f"Similarity: {score}"
    }

# Use in evaluation
experiment_results = client.evaluate(
    agent.invoke,
    data="investment_analysis_test",
    evaluators=[custom_accuracy_evaluator]
)
```

### A/B Testing

```python
# Create two agent versions
agent_v1 = create_react_agent(model_v1, tools=tools)
agent_v2 = create_react_agent(model_v2, tools=tools)

# Evaluate both
results_v1 = client.evaluate(
    agent_v1.invoke,
    data="test_dataset",
    evaluators=[evaluator],
    experiment_prefix="v1"
)

results_v2 = client.evaluate(
    agent_v2.invoke,
    data="test_dataset",
    evaluators=[evaluator],
    experiment_prefix="v2"
)

# Compare results
print(f"V1 accuracy: {results_v1['accuracy']}")
print(f"V2 accuracy: {results_v2['accuracy']}")
```

### Best Practices

#### 1. Comprehensive Test Coverage
```python
# Test different scenarios
examples = [
    {"category": "simple_query", "input": "What is AAPL price?"},
    {"category": "complex_analysis", "input": "Full analysis of tech sector"},
    {"category": "error_handling", "input": "Analyze invalid symbol XYZ123"},
    {"category": "multi_step", "input": "Compare AAPL vs GOOGL"},
]
```

#### 2. Multiple Evaluation Metrics
```python
evaluators = [
    create_trajectory_match_evaluator(),  # Tool usage correctness
    create_trajectory_llm_as_judge(),     # Output quality
    custom_latency_evaluator,             # Performance
    custom_cost_evaluator                 # Efficiency
]
```

#### 3. Regression Testing
```python
# Track performance over time
for version in ["v1.0", "v1.1", "v1.2"]:
    results = client.evaluate(
        agent.invoke,
        data="regression_tests",
        experiment_prefix=version
    )
    store_results(version, results)
```

#### 4. Real-World Data
```python
# Use production data for evaluation (anonymized)
real_queries = load_production_queries(anonymize=True)
test_dataset = create_dataset_from_queries(real_queries)
```

## Complete Example

```python
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langsmith import Client
from agentevals.trajectory.match import create_trajectory_match_evaluator

# Define tools
@tool
def get_stock_price(symbol: str) -> float:
    """Get current stock price."""
    return 150.00  # Simplified

# Create agent with context and store
llm = init_chat_model("anthropic:claude-3-7-sonnet-latest")
agent = create_react_agent(llm, tools=[get_stock_price])
store = InMemoryStore()

# Store user preferences
store.put(
    namespace=["users", "123"],
    key="preferences",
    value={"risk_tolerance": "moderate"}
)

# Create evaluation dataset
client = Client()
dataset = client.create_dataset("stock_agent_test")
client.create_examples(
    dataset_id=dataset.id,
    examples=[{
        "inputs": {"messages": [{"role": "user", "content": "What's AAPL price?"}]},
        "outputs": {
            "messages": [{
                "role": "assistant",
                "tool_calls": [{"name": "get_stock_price", "args": {"symbol": "AAPL"}}]
            }]
        }
    }]
)

# Evaluate
evaluator = create_trajectory_match_evaluator()
results = client.evaluate(
    lambda inputs: agent.invoke(inputs),
    data="stock_agent_test",
    evaluators=[evaluator]
)

print(f"Evaluation results: {results}")
```

## Reference

### Context
- **Static**: Immutable runtime configuration via `context` parameter
- **Dynamic**: Mutable state during execution
- **Persistent**: Cross-conversation store for long-term memory

### Models
- **init_chat_model()**: Quick model initialization
- **Provider formats**: `"provider:model-name"`
- **Configuration**: temperature, max_tokens, streaming, rate limiting
- **Fallbacks**: `.with_fallbacks([model1, model2])`

### Evaluation
- **AgentEvals**: `trajectory_match`, `llm_as_judge`, custom evaluators
- **LangSmith**: Dataset creation, experiment tracking
- **Metrics**: Accuracy, tool usage, latency, cost
- **A/B Testing**: Compare agent versions

---

**Note**: Combine context management, appropriate models, and comprehensive evaluation for production-ready agents.
