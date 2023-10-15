from autogen import AssistantAgent
from enum import Enum
import os
from typing import Dict, Optional, Union, Callable
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

mongo_llm_config = {
    "model": "gpt-4",
    "config_list": config_list,
    "seed": 42,
    "functions": [
        {
            "name": "get_collection_endpoints",
            "description": "it takes a collection name as an input and returns a list of API endpoints associated with that collection \
                and a sample interface for that collection",
            "parameters": {
                "type": "object",
                "properties": {
                    "collection": {
                        "type": "string",
                        "description": "Valid collection name",
                    }
                },
                "required": ["collection"],
            },
        }
    ],
}


class Collections(Enum):
    TAGS = "TAGS"
    USERS = "USERS"


class MongoAgent(AssistantAgent):
    def __init__(
        self,
        name: str,
        system_message: str,
        llm_config: Optional[Union[Dict, bool]] = None,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "NEVER",
        code_execution_config: Optional[Union[Dict, bool]] = False,
        **kwargs,
    ):
        super().__init__(
            name,
            system_message,
            llm_config,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            code_execution_config,
            **kwargs,
        )
        self.register_functions()
        self.COLLECTION_MAP = {
            "TAGS": [{"enpoint": "http://localhost:3333/api/tags"}],
            "USERS": [{"endpoint": "http://localhost:3333/api/users"}],
        }

    def get_collection_endpoints(self, collection: Collections):
        return self.COLLECTION_MAP[collection]

    def register_functions(self):
        self.register_function(
            function_map={"get_collection_endpoints": self.get_collection_endpoints}
        )


mongo_agent = MongoAgent(
    name="MongoAgent",
    llm_config=mongo_llm_config,
    system_message=f"""Mongo Endpoint Agent. You can only use the function you are provided with.
        Based on the user query, you need to guess which mongo db collections he will need in his query.
        After it, should use the "get_collection_endpoints" function to get the endpoints associated with that collection,
        and pass that info to the coder.
        The function you are provided with takes as an input one of the COLLECTIONS list item \
            and return the endpoints and interfaces associated with that collection.
        COLLECTIONS: {list(Collections)}""",
)
