from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask import Flask

app = Flask(__name__)

db = SQLAlchemy(app)



class Todo(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), nullable=False)
    priority = db.Column(db.Integer)
    description = db.Column(db.Text)
    finished = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()