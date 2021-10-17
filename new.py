from flask import Flask, redirect, request, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from  flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
api=Api(app)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///lite.db"
db=SQLAlchemy(app)


class NEW(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200))
    summary=db.Column(db.String(500))


resourse_field = {
    'id':fields.Integer,
    'task':fields.String,
    'summary':fields.String,
}


todo_post = reqparse.RequestParser()
todo_post.add_argument("task", type=str, help='Task is required', required=True)
todo_post.add_argument('summary', type=str, help='summary is equired', required=True)

todo_update=reqparse.RequestParser()
todo_update.add_argument('task',type=str)
todo_update.add_argument('summary',type=str)



class hello(Resource):
    
    def get(self):
        task=NEW.query.all()

        todos={}

        for i in task:
            todos[i.id]={"task":i.task,"summary":i.summary}
        return todos


class hi(Resource):
    @marshal_with(resourse_field)
    def get(self,todo_id):
        task=NEW.query.filter_by(id=todo_id).first()
        if not task:
            abort(401,'not find the task')
        return task


    @marshal_with(resourse_field)
    def post(self,todo_id):
        args = todo_post.parse_args()
        task=NEW.query.filter_by(id=todo_id).first()
        if task:
            abort(409, 'task id already taken')
        a=NEW(id=todo_id,task=args['task'],summary=args['summary'])
        db.session.add(a)
        db.session.commit()
        return a, 201


    
    def put(self,todo_id):
        args = todo_update.parse_args()
        task=NEW.query.filter_by(id=todo_id).first()
        if todo_id in task:
            abort(409,'already exist')
        if args['task']:
            task.task=args['task']
        if args['summary']:
            task.summary=args['summary']
        db.session.commit()
        return task
    def delete(self,todo_id):
        task=NEW.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        return 'dleted',204








api.add_resource(hi,'/todo/<int:todo_id>')
api.add_resource(hello,'/todo')

if __name__=="__main__":
    app.run(debug=True)