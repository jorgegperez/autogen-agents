from fastapi import APIRouter
import os
from autogen import (
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager,
)
from app.resources.agents import (
    mongo_agent as MongoAgent,
    user_proxy as UserProxy,
    coder as CoderAgent,
)

router = APIRouter()


@router.get("/")
async def get_mongo_query(query: str = None):
    config_list = [
        {
            "model": "gpt-4",
            "api_key": os.environ.get("OPENAI_API_KEY"),
        }
    ]

    llm_config = {"model": "gpt-4", "config_list": config_list, "seed": 42}

    user_proxy_agent = UserProxy.user_proxy

    mongo_assistant = MongoAgent.mongo_agent

    coder_assistant = CoderAgent.coder_agent

    groupchat = GroupChat(
        agents=[user_proxy_agent, mongo_assistant, coder_assistant],
        messages=[],
        max_round=50,
    )

    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
        system_message="""Chat Manager. You will ALWAYS follow the next steps:
    1. The MongoAgent will determine the endpoints needed in the query and its corresponding interfaces.
    2. With that info the Coder creates a Python script to query the endpoint and calculate whatever its needed.
    3. With the result of that script, you will answer the user's query. """,
    )

    user_proxy_agent.initiate_chat(manager, message=query)

    return {"message": user_proxy_agent.last_message()}
