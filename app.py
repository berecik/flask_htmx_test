from crypt import methods

from flask import Flask
app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
    <head>
        <title>Flask HTMX App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="utf-8">
        <script src="https://unpkg.com/htmx.org/dist/htmx.js"></script>
    </head>
    <body>
        <h1>Flask HTMX App</h1>
        <p>Current count: <span id="count"<{{ counter }}</span></p>
        <button hx-post="/count" hx-target="#count" hx-swap="innerHTML">Increment</button>
    </body>
</html>
"""

state = {
    'counter': 0
}
@app.route('/')
def hello_world():  # put application's code here
    return template

@app.route('/count', methods=['POST', 'GET'])
def count():
    global state
    state['counter'] += 1
    return str(state['counter'])

if __name__ == '__main__':
    app.run()
