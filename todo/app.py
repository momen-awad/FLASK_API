from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from models import db, Todo


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)


class TodoRUD(Resource):


    def get(self, **kwargs):
        todo_id = kwargs.get('todo_id')
        print("id ->", todo_id)
        task = Todo.query.get(todo_id)
        if not task:
            abort(404, message='Not Found')

        data = {
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
            'description': task.description,
            'finished': task.finished
        }

        return data, 200


    def delete(self, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        print("id ->", todo_id)
        todo_obj = Todo.query.get(todo_id)

        print('todo obj -> ', todo_obj)

        db.session.delete(todo_obj)
        db.session.commit()

        return {'message': 'Deleted Successfully'}, 200

    def patch(self, **kwargs):
        todo_id = kwargs.get('todo_id')
        todo_obj = Todo.query.get(todo_id)
        db.session.add(todo_obj)  
        db.session.commit()
        return {'message': 'Todo Updated Successfully'}, 200






class TodoLC(Resource):

    
    def post(self):
        try:
            data = {
                'name': request.form.get('name'),
                'priority': request.form.get('priority'),
                'description': request.form.get('description'),
                'finished': False
            }

            todo_obj = Todo(**data) 
            db.session.add(todo_obj) 
            db.session.commit()

            return {'message': 'Task Created Successfully'}, 201
        except Exception as e:
            abort(500, message='Internal Server Error')

    def get(self):
        try:
            todo_objects = Todo.query.filter().all()
            print("TD OBJS -> ", todo_objects)

            limit = request.args.get('limit')

            my_new_list = []

            for task in todo_objects:
                data = {
                    'id': task.id,
                    'name': task.name,
                    'priority': task.priority,
                    'description': task.description,
                    'finished': task.finished
                }

                my_new_list.append(data)

            if limit:
                print(type(limit))
                my_new_list = my_new_list[:int(limit)]

            return my_new_list

        except Exception as e:
            abort(500, message="Internal Server Error {}".format(e))



        












'''@app.before_first_request
def initiate_date_base_tables():
    db.create_all()




app.run(debug=True)'''




app.add_resource(TodoLC, '/api/v1/todo')


app.add_resource(TodoRUD, '/api/v1/todo/<int:todo_id>')


db.init_app(app)


@app.before_first_request
def initiate_data_base_tables():
    db.create_all()



app.run(port=5080, debug=True)
