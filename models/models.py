from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Questions(db.Model):
    __tablename__ = 'questions'
    questionID = db.Column('questionID', db.Integer, primary_key=True)
    questions = db.Column('question_txt', db.String(120))
    k_type = db.Column('k_type', db.Integer)
    k_subtype = db.Column('k_subtype', db.Integer)
    k_language = db.Column('k_language', db.Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.questionID,
            'questions': self.questions,
            'k_type': self.k_type,
            'k_subtype': self.k_subtype,
            'k_language': self.k_language
        }

class Responses(db.Model):
    __tablename__ = 'responses'
    responseID = db.Column('responseID', db.Integer, primary_key=True)
    response_txt = db.Column('response_txt', db.String(120))
    questionID = db.Column('questionID', db.Integer)
    k_correct_ind = db.Column('k_correct_ind', db.Integer)
    comments_txt = db.Column('comments_txt', db.String(120))


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.responseID,
            'response_txt': self.response_txt,
            'questionID': self.questionID,
            'k_correct_ind': self.k_correct_ind,
            'comments_txt': self.comments_txt
        }

class Ref_type(db.Model):
    __tablename__ = 'ref_type'
    k_type = db.Column('k_type', db.Integer, primary_key=True)
    type_txt = db.Column('type_txt', db.String(120))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'k_type': self.k_type,
            'type_txt': self.type_txt
        }