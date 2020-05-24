from collections import OrderedDict

from flask import Flask
from flask.ext.restful import Api, Resource, fields, marshal_with

app = Flask(__name__)
module_todo = Api(app)

resource_fields = {
    'task':   fields.String,
    'uri':    fields.Url('todo_ep'),
    'todo_id': fields.String,
    'no_this_attr': fields.String  # null
}

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

@module_todo.resource('/todos', endpoint='todo_ep')
class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')


# module_todo.add_resource(Todo, '/todos', endpoint='todo_ep')

if __name__ == '__main__':
    app.run(debug=True)
