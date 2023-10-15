from autogen import AssistantAgent
import os
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

llm_config = {"model": "gpt-4", "config_list": config_list, "seed": 42}

coder_agent = AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
    system_message=f"""Coder. You write and execute python/shell code to solve tasks.
        You will get a list of endpoints and its corresponding interface and call that endpoint to perform queries.
        If you use any endpoint, you will need to use the following Bearer Token: "{os.environ.get("BEARER_TOKEN")}".
        Wrap the code in a code block that specifies the script type.
        The user can't modify your code. So do not suggest incomplete code which requires others to modify.
        Don't use a code block if it's not intended to be executed by the executor.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result.
        Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again.
        Suggest the full code instead of partial code or code changes.
        If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption,\
            collect additional info you need, and think of a different approach to try.
        """,
)
