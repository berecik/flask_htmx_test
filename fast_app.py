from fasthtml.common import *

# The line `app, rt, todos, Todo = fast_app(...)` is initializing the application and setting up the
app, rt, todos, Todo = fast_app(
    "todos.db",
    hdrs=[Style(":root { --pico-font-size: 100%; }")],
    id=int,
    title=str,
    done=bool,
    pk="id",
)

id_currunt = "current-todo"

# Helper function to get the id of a task
def todo_id(id):
    return f"todo-{id}"


# Define how each task is displayed
@patch
def __ft__(self: Todo):
    show = AX(self.title, f"/todos/{self.id}", id_currunt)
    edit = AX("edit", f"/edit/{self.id}", id_currunt)

    done = CheckboxX(
        checked=False
    )
    completed = " ✅" if self.done else done
    complete = AX(completed, hx_get=f"/done/{self.id}", target_id=todo_id(self.id), hx_swap="outerHTML")
    return Li(show, complete, " | ", edit, id=todo_id(self.id))


# Helper functions
def create_input_field(**kw):
    return Input(
        id="new-title",
        name="title",
        placeholder="Enter a new Todo",
        required=True,
        **kw,
    )


# Route to display the task list and add new tasks
@rt("/")
async def get():
    add_task = Form(
        Group(create_input_field(), Button("Add")),
        hx_post="/",
        target_id="todo-list",
        hx_swap="beforeend",
    )
    task_list = (
        Card(Ul(*todos(), id="todo-list"), header=add_task, footer=Div(id=id_currunt)),
    )
    title = "FastHTML To-Do List"
    
    # Display the source code
    with open(__file__) as f:
        source_txt = f.read()
    source_code = H2("Source Code"), Pre(source_txt, id="source", cls="container")
    
    # Display the Marysia Software Limited logo
    logo = (Img(src="https://marysia.app/resources/img/logo_small.png",
               class_="mt-3", style="width:30%", alt="logo"),
            H1(title))
    
    # Show main screen of the app
    return Title(title), Main(logo, task_list, source_code, cls="container")


# Route to delete a task
@rt("/todos/{id}")
async def delete(id: int):
    todos.delete(id)
    return clear(id_currunt)


# Route to add a new task
@rt("/")
async def post(todo: Todo):
    return todos.insert(todo), create_input_field(hx_swap_oob="true")


# Route to display the edit form for a task
@rt("/edit/{id}")
async def get(id: int):
    res = Form(
        Group(Input(id="title"), Button("Save")),
        Hidden(id="id"),
        CheckboxX(id="done", label="Done"),
        hx_put="/",
        target_id=todo_id(id),
        id="edit",
    )
    return fill_form(res, todos.get(id))

# Route to toggle a task state
@rt("/done/{id}")
async def get(id: int):
    todo = todos.get(id)
    todo.done = not todo.done
    return todos.upsert(todo), clear(id_currunt)

# Route to update a task
@rt("/")
async def put(todo: Todo):
    return todos.upsert(todo), clear(id_currunt)


@rt("/todos/{id}")
async def get(id: int):
    todo = todos.get(id)
    btn = Button(
        "delete",
        hx_delete=f"/todos/{todo.id}",
        target_id=todo_id(todo.id),
        hx_swap="outerHTML",
    )
    return Div(Div(todo.title), btn)

# Start the application server
serve()
