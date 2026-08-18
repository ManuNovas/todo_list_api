from aws_cdk import Stack
from constructs import Construct
from infra.nested_stacks.provider_nested_stack import ProviderNestedStack
from infra.nested_stacks.repository_nested_stack import RepositoryNestedStack


class TodoListStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, **kwargs):
        super().__init__(scope, stack_id, **kwargs)
        RepositoryNestedStack(self, "Repository", **kwargs)
        ProviderNestedStack(self, "Provider", **kwargs)
