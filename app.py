from flask import Flask, jsonify, abort, make_response, request
from models.models import Questions, Responses, db, Ref_type
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
        idQuestions.append(i.questionID)
    toPick = randint(1, len(idQuestions))
    return jsonify(questions=questionbyID(toPick), responses=responsesbyID(toPick))



@app.route('/api/1/questionsbyCat', methods=['GET'])
def get_questionMath():
    cat = request.args.get('category', '')
    if cat.isdigit() :
        c = questionrepbyCat(cat)
        return jsonify(questions=c)
    return jsonify(error="No valid category received")

@app.route('/api/1/quiz', methods=['GET'])
def get_quiz():
    myCategories = Ref_type.query.all()
    questionList = []
    for i in myCategories:
        x = questionrepbyCat(i.serialize['k_type'])
        questionList.append(x)
    return jsonify(questions=questionList)

# @app.route('/api/1/users', methods=['POST'])
# def create_users():
#    if not request.json or not '' in request.json:
#        abort(400)
#    user = Questions(request.json['name'])
#    db.session.add(user)
#    db.session.commit()
#    return jsonify(users=[i.serialize for i in Questions.query.all()])

def questionbyID(id):
    return Questions.query.filter_by(questionID=id).first().serialize

def responsesbyID(id):
    return [i.serialize for i in Responses.query.filter_by(questionID=id)]

def questionrepbyCat(cat):
    tableIDQuestCat= []
    myQuestiosnWithCat = Questions.query.filter_by(k_type=cat)
    for i in myQuestiosnWithCat:
        tableIDQuestCat.append(i.questionID)
    questionToPick = min(len(tableIDQuestCat), 5)
    b = []
    for i in range(0, questionToPick):        b.append({'question':questionbyID(tableIDQuestCat[i]), 'responses' : responsesbyID(tableIDQuestCat[i])})
    return b


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
