import os
from autogen import UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

user_proxy_llm_config = {"model": "gpt-4", "config_list": config_list, "seed": 42}

user_proxy = UserProxyAgent(
    name="Admin",
    human_input_mode="TERMINATE",
    code_execution_config=False,
    llm_config=user_proxy_llm_config,
)
