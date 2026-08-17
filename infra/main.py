from aws_cdk import App

from stacks.todo_list_stack import TodoListStack

app = App()
TodoListStack(app, "TodoList")
app.synth()
