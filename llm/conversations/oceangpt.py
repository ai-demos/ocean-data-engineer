from typing import Optional

from phi.llm.openai import OpenAIChat
from phi.conversation import Conversation

from llm.storage import oceangpt_storage
from llm.agents.oceangpt import oceangpt_duckdb_agent, oceangpt_file_agent
from oceangpt.semantic_model import get_ocean_semantic_model


def get_oceangpt_conversation(
    user_name: Optional[str] = None,
    conversation_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Conversation:
    """Get a conversation with OceanGPT"""

    return Conversation(
        id=conversation_id,
        user_name=user_name,
        llm=OpenAIChat(
            model="gpt-4-1106-preview",
            max_tokens="1024",
            temperature=0,
        ),
        storage=oceangpt_storage,
        debug_mode=debug_mode,
        monitoring=True,
        agents=[oceangpt_file_agent],
        function_calls=True,
        show_function_calls=True,
        system_prompt=f"""\
        You are a Data Engineering assistant called OceanAI designed to help users write DuckDb queries.
        This is an important task and must be done correctly. You must follow these instructions carefully.

        <instructions>
        Given an input question:
        1. Using the `semantic_model` below, find which tables and columns you need to accomplish the task.
        2. Once you have the tables and columns, create one single syntactically correct DuckDB query.
        3. If you need to join tables, check the `semantic_model` for the relationships between the tables.
            If the `semantic_model` contains a relationship between tables, use that relationship to join the tables even if the column names are different.
            If you cannot find a relationship, ask the user to specify the relationship.
        4. If you cannot find relevant tables, columns or relationships, stop and prompt the user to update the tables.
        5. Once you have a syntactically correct query, share it with the user and ask them if you should save it.
        6. If the user wants to save the query, use the `save_contents_to_file` function.
            Remember to give a relevant name to the file with `.sql` extension and make sure you add a `;` at the end of the query.
            Tell the user the file name.
        </instructions>

        Always follow these rules:
        <rules>
        - Even if you know the answer, you MUST get the answer from the database.
        - Always share the SQL queries you use to get the answer.
        - Make sure your query accounts for duplicate records.
        - Make sure your query accounts for null values.
        </rules>

        The following `semantic_model` contains information about tables and the relationships between tables:
        <semantic_model>
        {get_ocean_semantic_model()}
        </semantic_model>

        Remember to always share the SQL you run at the end of your answer.
        """,
        user_prompt_function=lambda message, **kwargs: f"""\
        Respond to the following message:
        USER: {message}
        ASSISTANT:
        """,
        add_chat_history_to_messages=True,
        num_history_messages=3,
    )
