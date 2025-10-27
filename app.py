from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enable cross-origin requests for frontend

# In-memory storage for todos
todos = []
next_id = 1

@app.route('/')
def home():
    return "Flask To-Do API is running!"

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    global next_id
    data = request.get_json()
    title = data.get('title', '')
    if not title:
        return jsonify({"error": "Title is required"}), 400
    new_todo = {"id": next_id, "title": title, "done": False}
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = data.get('done', todo['done'])
            return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
