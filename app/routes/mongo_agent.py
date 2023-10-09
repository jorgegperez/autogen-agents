from fastapi import APIRouter
import os
from autogen import (
    config_list_from_json,
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager,
)
from urllib.parse import urlencode


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

    user_proxy = UserProxyAgent(
        name="Admin",
        system_message="A human admin. Plan execution needs to be approved by this admin.",
        code_execution_config=False,
        llm_config=llm_config,
    )

    engineer = AssistantAgent(
        name="Engineer",
        llm_config=llm_config,
        system_message=f"""Engineer. You write python/shell code to solve tasks.
        You can call the following endpoint (http://localhost:3333/api/tags) to get a list of tags with the following properties:
        "_id": string,
        "isDeleted": boolean,
        "deleteDate": null | Date,
        "name": string,
        "academy": string,
        "__v": number,
        "isDemo": boolean,
        "updatedAt": Date
        If you use this endpoint, you will need to use the following Bearer Token: "{os.environ.get("BEARER_TOKEN")}".
        Wrap the code in a code block that specifies the script type.
        The user can't modify your code. So do not suggest incomplete code which requires others to modify.
        Don't use a code block if it's not intended to be executed by the executor.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result.
        Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again.
        Suggest the full code instead of partial code or code changes.
        If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        """,
    )

    executor = UserProxyAgent(
        name="Executor",
        system_message="Executor. Execute the code written by the engineer and report the result.",
        human_input_mode="NEVER",
        code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
        # function_map=
    )

    groupchat = GroupChat(
        agents=[user_proxy, engineer, executor],
        messages=[],
        max_round=50,
    )

    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy.initiate_chat(manager, message=query)

    return {"message": engineer}
