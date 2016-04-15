from flask import Flask, jsonify, abort, make_response, request
from models.models import Questions, Responses, db, Ref_type
from random import randint
from flask.ext.cors import CORS
import xlwt, time, math, smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
CORS(app)
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

@app.route('/api/1/result', methods=['POST'])
def retrieveResults():
    results =request.get_json();
    createExcelSheet(results);
    return jsonify(result="success")

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
    for i in range(0, questionToPick):b.append({'question':questionbyID(tableIDQuestCat[i]), 'responses' : responsesbyID(tableIDQuestCat[i])})
    return b


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def createExcelSheet(resultsToParse):
    book = xlwt.Workbook()
    filename = "results_" + time.strftime("%d%m%Y_%H%M") + "_" + resultsToParse["matricule"] + ".xls"
    sh = book.add_sheet("results")
    sh.write(0,0,time.strftime("%d/%m/%Y %H:%M"))
    sh.write(1,0,resultsToParse["name"])
    sh.write(2,0,resultsToParse["matricule"])
    sh.write(3,0,resultsToParse["mail"])
    sh.write(0,2,"Questions")
    sh.write(0,3,"Response given")
    sh.write(0,4,"Correct?")
    questionNb=1
    goodQuestion=0
    for myquestion in resultsToParse["questions"]:
        sh.write(questionNb,2,myquestion["question"])
        sh.write(questionNb,3,myquestion["response"])
        sh.write(questionNb,4,myquestion["correct"])
        if myquestion["correct"] == 'yes':
            goodQuestion+=1
        questionNb+=1
    sh.write(questionNb,4,math.ceil(goodQuestion/(questionNb-1)*100))
    book.save(filename)
    toaddr = "";
    sendMailTo(toaddr, filename, resultsToParse["name"], resultsToParse["matricule"])
    os.remove(filename)

def sendMailTo(toaddr, filename, name, matricule):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    fromaddr = ""

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Results of " + name + "_" + matricule

    body = "In attachement, the result of " + name + "_" + matricule

    msg.attach(MIMEText(body, 'plain'))

    attachment = open("D:\GitHub\yannQuestionnaire\yannQuestionnaire\\" + filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(fromaddr, "password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()




if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
