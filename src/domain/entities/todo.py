TODO_SK = "TODO#"

class Todo:
    pk: str
    sk: str
    title: str
    description: str
    created_at: str
    updated_at: str | None

    def __init__(self, user_pk: str, todo_sk: str, title: str, description: str, created_at: str, updated_at: str | None = None):
        self.pk = user_pk
        self.sk = TODO_SK + todo_sk
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
