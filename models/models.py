from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column('id', db.Integer, primary_key=True)
    categoriesID = db.Column('categoriesID', db.Integer)
    questions = db.Column('questions', db.String(120))
    correctResponseID = db.Column('correctResponseID', db.Integer)

    def __init__(self, questions=None, correctresid=None):
        self.questions = questions
        self.correctResponseID = correctresid

    def __repr__(self):
        return '<Questions %r>' % (self.questions)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'categoriesID': self.categoriesID,
            # This is an example how to deal with Many2Many relations
            'questions': self.questions,
            'correctResponseID': self.correctResponseID
        }

class Responses(db.Model):
    __tablename__ = 'responses'
    id = db.Column('id', db.Integer, primary_key=True)
    commentaire = db.Column('commentaire', db.String(120))
    questionID = db.Column('questionID', db.Integer)

    def __init__(self, commentaire=None, questionid=None):
        self.commentaire = commentaire
        self.questionID = questionid


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'commentaire': self.commentaire,
            'questionID': self.questionID
        }