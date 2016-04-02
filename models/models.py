from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column('questionID', db.Integer, primary_key=True)
    question_txt = db.Column('Question text', db.String(120))
    k_type = db.Column('Question type ID', db.Integer)
    k_subtype = db.Column('Question subtype ID', db.Integer)
    k_language = db.Column('Question Language ID', db.Integer)

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
    responseID = db.Column('Response ID', db.Integer, primary_key=True)
    questionID = db.Column('Question ID', db.Integer)
    response_txt = db.Column('Text response', db.String(120))
    k_correct_ind = db.Column('Correct indicator', db.Integer)
    comments_txt = db.Column('Response comment', db.String(120))

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