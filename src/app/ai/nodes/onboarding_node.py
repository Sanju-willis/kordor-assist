# src\app\ai\nodes\onboarding_node.py
from typing import Dict, Any, List, Sequence, cast
from pydantic import SecretStr
from langchain_core.messages import HumanMessage, AnyMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from app.types import CustomState
from app.ai.agents import build_onboarding_agent
from app.config.settings import settings

# Build once; type-correct api_key
ONBOARDING_AGENT = build_onboarding_agent(
    model=ChatOpenAI(
        model="gpt-4o",
        api_key=SecretStr(settings.OPENAI_API_KEY),
    ),
    checkpointer=None,
)

def onboarding_node(state: CustomState) -> Dict[str, Any]:
    msgs: Sequence[AnyMessage] = cast(Sequence[AnyMessage], state.get("messages", []) or [])
    
    # Always add fresh system message to force onboarding behavior
    system_msg = SystemMessage(content="""You are an onboarding specialist. Your job:
1) Explain available modules: 'company' and 'product'  
2) Ask user to choose ONE module
3) Use validate_choice tool when they respond
4) Tell them the next step after validation

Start by explaining the two modules and asking them to choose.""")
    
    if not msgs:
        user_msg = HumanMessage(content="Start onboarding")
        payload = {"messages": [system_msg, user_msg]}
    else:
        # Always include system message + last user message only
        last_user_msg = None
        for msg in reversed(msgs):
            if hasattr(msg, 'type') and msg.type == 'human':
                last_user_msg = msg
                break
        
        if last_user_msg:
            payload = {"messages": [system_msg, last_user_msg]}
        else:
            payload = {"messages": [system_msg, HumanMessage(content="Continue onboarding")]}

    config: RunnableConfig = cast(
        RunnableConfig,
        {"configurable": {"thread_id": f"onboarding_{state.get('thread_id', 'default')}"}},
    )

    result = ONBOARDING_AGENT.invoke(payload, config=config)
    new_msgs: List[AnyMessage] = cast(List[AnyMessage], result.get("messages", []))

    # Merge messages
    if len(new_msgs) >= len(msgs):
        out_msgs: List[AnyMessage] = list(msgs) + new_msgs[len(msgs):]
    else:
        out_msgs = list(msgs) + new_msgs

    # Determine next stage based on USER INPUT (not agent response)
    next_stage = "onboarding"  # default
    
    # Look for user's choice in the incoming message
    current_user_msg = None
    for msg in reversed(msgs):
        if hasattr(msg, 'type') and msg.type == 'human':
            current_user_msg = msg
            break
    
    if current_user_msg:
        user_content = str(current_user_msg.content).lower()
        print(f"DEBUG: User said: {user_content}")
        
        if "company" in user_content and "product" not in user_content:
            next_stage = "company_ready"
            print("DEBUG: User chose company")
        elif "product" in user_content and "company" not in user_content:
            next_stage = "product_ready" 
            print("DEBUG: User chose product")
        else:
            print("DEBUG: No clear choice detected, staying in onboarding")

    print(f"DEBUG: Onboarding stage changing to: {next_stage}")  # Debug log

    return {"messages": out_msgs, "stage": next_stage}