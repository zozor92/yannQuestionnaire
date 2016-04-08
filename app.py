from flask import Flask, jsonify, abort, make_response, request
from models.models import Questions, Responses, db
from random import randint

app = Flask(__name__)
db.init_app(app)

mathCatId = 1
statsCatId = 2
EcoCatId = 3


@app.route('/api/1/questions', methods=['GET'])
def get_questions():
    return jsonify(questions=[i.serialize for i in Questions.query.all()])


@app.route('/api/1/responses', methods=['GET'])
def get_responses():
    return jsonify(responses=[i.serialize for i in Responses.query.all()])


@app.route('/api/1/oneQuestion', methods=['GET'])
def get_onequestion():
    test = Questions.query.all()
    idQuestions = []
    for i in test:
        idQuestions.append(i.id)
    toPick = randint(1, len(idQuestions))
    return jsonify(questions=questionbyID(toPick), responses=responsesbyID(toPick))



@app.route('/api/1/questions', methods=['GET'])
def get_questionMath():
    cat = request.args.get('category', '')
    if cat.isdigit() :
        c = questionrepbyCat(cat)
        return jsonify(questions=c)


# @app.route('/api/1/users', methods=['POST'])
# def create_users():
#    if not request.json or not '' in request.json:
#        abort(400)
#    user = Questions(request.json['name'])
#    db.session.add(user)
#    db.session.commit()
#    return jsonify(users=[i.serialize for i in Questions.query.all()])

def questionbyID(id):
    return Questions.query.filter_by(id=id).first().serialize

def responsesbyID(id):
    return [i.serialize for i in Responses.query.filter_by(questionID=id)]

def questionrepbyCat(cat):
    tableIDQuestMath= []
    myQuestiosnWithCat = Questions.query.filter_by(categoriesID=mathCatId)
    for i in myQuestiosnWithCat:
        tableIDQuestMath.append(i.id)
    questionToPick = min(len(tableIDQuestMath), 5)
    b = []
    for i in range(0, questionToPick):
        b.append({'question':questionbyID(tableIDQuestMath[i]), 'responses' : responsesbyID(tableIDQuestMath[0])})
    return b


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
