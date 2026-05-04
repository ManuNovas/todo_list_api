from os import getenv

from src.adapters.input.user_input_adapter import UserInputAdapter
from src.adapters.output.user_output_adapter import UserOutputAdapter
from src.application.use_cases.user_use_cases import UserUseCases

table_name = getenv("USERS_TABLE_NAME", "todo_users_dev")
user_repository = UserOutputAdapter(table_name)
use_cases = UserUseCases(user_repository)
input_adapter = UserInputAdapter(use_cases)


def register(event, context):
    return input_adapter.register(event)

def login(event, context):
    return input_adapter.login(event)
