import pytz
from flask import Flask, request
import urllib.parse
from flask import Response
import json
import smtplib
import codecs
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import constants

app = Flask(__name__)
from sqlalchemy.engine import create_engine

engine = create_engine(
    'postgres://%s:Amcompose2019@testamcompose.postgres.database.azure.com/postgres' % urllib.parse.quote(
        'newuser@testamcompose'))

jsonObject = [{
      "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
      "type": "AdaptiveCard",
      "version": "1.0",
      "body": [
        {
          "type": "TextBlock",
          "text": "This is some text",
          "size": "large"
        },
        {
          "type": "TextBlock",
          "text": "It doesn't wrap by default",
          "weight": "bolder"
        },
        {
          "type": "TextBlock",
          "text": "So set **wrap** to true if you plan on showing a paragraph of text",
          "wrap": true
        },
        {
          "type": "TextBlock",
          "text": "You can also use **maxLines** to prevent it from getting out of hand",
          "wrap": true,
          "maxLines": 2
        },
        {
          "type": "TextBlock",
          "text": "You can even draw attention to certain text with color",
          "wrap": true,
          "color": "attention"
        }
      ]
    }]

@app.route("/")
def hello():
    return "Hello World!"

def generatetext(sid, number):
    ques = engine.execute(constants.queryQuestionSurvey, sid)
    question = ques.fetchall()
    question = str(question[number])
    question = question[2:len(question) - 3]
    body = sid + str(number + 1)
    payload = constants.surveyTextPayload % (question, body,)
    return payload

@app.route("/postmessage", methods=['POST'])
def postmessage():
    postinteams()

def postinteams():
    url = 'https://graph.microsoft.com/beta/teams/4fbdbd4b-09dc-4fd8-aaf2-e92b9beb23e3/channels/19:169c8d5ec0a945558634a21d1ff5fbf2@thread.skype/messages'
    auth_token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6InN2QVZ6V011S0VLajhOUmRSSlUzVGVBVndISDBwSXRYR2N1RFZhQVhldkUiLCJhbGciOiJSUzI1NiIsIng1dCI6InU0T2ZORlBId0VCb3NIanRyYXVPYlY4NExuWSIsImtpZCI6InU0T2ZORlBId0VCb3NIanRyYXVPYlY4NExuWSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRiNDcvIiwiaWF0IjoxNTYzODcxNTg0LCJuYmYiOjE1NjM4NzE1ODQsImV4cCI6MTU2Mzg3NTQ4NCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhNQUFBQXVhMUFZN3QwOFhEcGUyQUlFMGJZSTJpVnlWWmJ6aWFCbllRMTJHQ1dqUi9mcXRoQXRaNmhNSlVEZkw5Tm9Sd01rZ1JESkNjTXdqeitTdTFLMmJkYS9mSXFLVFRvajlZTitPOWY4bGljM1FNPSIsImFtciI6WyJwd2QiLCJ3aWEiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggZXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiS3VtYXIiLCJnaXZlbl9uYW1lIjoiU2h1YmhhbSIsImluX2NvcnAiOiJ0cnVlIiwiaXBhZGRyIjoiMTY3LjIyMC4yMzguOTMiLCJuYW1lIjoiU2h1YmhhbSBLdW1hciIsIm9pZCI6ImE1NDBkN2UzLTAxYjktNGRlOS1hMGNiLTMwZGYzMjIyYjcwOSIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0yMTQ2NzczMDg1LTkwMzM2MzI4NS03MTkzNDQ3MDctMjI3OTkxNiIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMDAwMEE0RDhGRTExIiwic2NwIjoiQ2FsZW5kYXJzLlJlYWRXcml0ZSBDb250YWN0cy5SZWFkV3JpdGUgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5Qcml2aWxlZ2VkT3BlcmF0aW9ucy5BbGwgRGV2aWNlTWFuYWdlbWVudE1hbmFnZWREZXZpY2VzLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRSQkFDLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRSQkFDLlJlYWRXcml0ZS5BbGwgRGV2aWNlTWFuYWdlbWVudFNlcnZpY2VDb25maWcuUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudFNlcnZpY2VDb25maWcuUmVhZFdyaXRlLkFsbCBEaXJlY3RvcnkuQWNjZXNzQXNVc2VyLkFsbCBEaXJlY3RvcnkuUmVhZFdyaXRlLkFsbCBGaWxlcy5SZWFkV3JpdGUuQWxsIEdyb3VwLlJlYWRXcml0ZS5BbGwgSWRlbnRpdHlSaXNrRXZlbnQuUmVhZC5BbGwgTWFpbC5SZWFkV3JpdGUgTWFpbGJveFNldHRpbmdzLlJlYWRXcml0ZSBOb3Rlcy5SZWFkV3JpdGUuQWxsIG9wZW5pZCBQZW9wbGUuUmVhZCBwcm9maWxlIFJlcG9ydHMuUmVhZC5BbGwgU2l0ZXMuUmVhZFdyaXRlLkFsbCBUYXNrcy5SZWFkV3JpdGUgVXNlci5SZWFkQmFzaWMuQWxsIFVzZXIuUmVhZFdyaXRlIFVzZXIuUmVhZFdyaXRlLkFsbCBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJpbmtub3dubnR3ayIsImttc2kiXSwic3ViIjoiMXllMk9iRE5oZ0kzb09NaFhLaVZCVnptNTJDb3BWeFhkTHZieWo1WXAxMCIsInRpZCI6IjcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0NyIsInVuaXF1ZV9uYW1lIjoic2h1a3VtYUBtaWNyb3NvZnQuY29tIiwidXBuIjoic2h1a3VtYUBtaWNyb3NvZnQuY29tIiwidXRpIjoiOF9UZl9hY3FRRUdHRl9BVGw2RUtBQSIsInZlciI6IjEuMCIsInhtc19zdCI6eyJzdWIiOiIwV1RMeUM4U0F4SWdlVktQdFRHV21DRkhyQ09uN1Yta0lHaGR5eVRhRWVnIn0sInhtc190Y2R0IjoxMjg5MjQxNTQ3fQ.Q3Tf_rAg21gPty38VzzyKkDepoIBgSTbNdS11_d_yDBsqR-TnhMyZUyzF4qjcFIbw8UPul-MmAbJlWNQsONFG7uckyZrjA4RfLMTaYbUb3yPQQ3a5iAy_euhaa0uWu4H76IXcjdGt4ulALMpzbAjsyDXvbIEB5qQNXmeNeMK9fLjHEfe45U2dVSlP27esobNicD8hrfiN1nfp9Re2a6Tt4LHlurqDZHTXh2Fj4f87jvxQ1jxlvG4btLXYievxOaRZbbqav45Ezynds_tuXJDnnEk-qb7VsY8esgwEguTApKfK16YFh7T7e0e3NnrH3-OTNAJ7lQmnudhMEw44oo68g'
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + auth_token}
    body = convertjsonobject(jsonObject)
    response = requests.post(url, json=body, headers=headers)
    print(response)

def convertjsonobject(jsonobject):
    body = '{"subject": null,"body": {"contentType": "html", "content": "<attachment id=\"74d20c7f34aa4a7fb74e2b30004247c5\"></attachment>"'
    attachments = {
        "attachments": [
            {
                "id": "74d20c7f34aa4a7fb74e2b30004247c5",
                "contentType": "application/vnd.microsoft.card.thumbnail",
                "contentUrl": null,
                "content": str(jsonObject[0]),
                "name": null,
                "thumbnailUrl": null
            }
        ]
    }
    reqbodyforteams = body + str(attachments) + '}'
    return reqbodyforteams

@app.route("/getsurveyquestion", methods=['POST'])
def getsurveyquestion():
    sidn = request.data
    sidn = sidn.decode(constants.UTF8)
    number = sidn[len(sidn) - 1]
    sid = sidn[0:len(sidn) - 1]
    type = engine.execute(constants.queryTypeSurvey, sid)
    type = type.fetchall()
    if int(number) == len(type):
        payload = constants.endCardSurvey
        resp = Response(payload)
        resp.headers['CARD-UPDATE-IN-BODY'] = True
        resp.headers['Content-Type'] = 'application/json'
        return resp
    type = str(type[int(number)])
    type = type[2:len(type) - 3]
    payload = ""
    if type == constants.surveyTextCode:
        payload = generatetext(sid, int(number))
    if type == constants.surveyNumericCode:
        payload = generatenumeric(sid, int(number))
    if type == constants.surveyDateCode:
        payload = generatedate(sid, int(number))
    if type == constants.surveyChoiceCode:
        payload = generatechoice(sid, int(number))
    resp = Response(payload)
    resp.headers['CARD-UPDATE-IN-BODY'] = True
    resp.headers['Content-Type'] = 'application/json'
    return resp


def generatenumeric(sid, number):
    ques = engine.execute(constants.queryQuestionSurvey, sid)
    question = ques.fetchall()
    question = str(question[number])
    question = question[2:len(question) - 3]
    body = sid + str(number + 1)
    payload = constants.surveyNumericPayload % (question, body,)
    return payload


def generatedate(sid, number):
    ques = engine.execute(constants.queryQuestionSurvey, sid)
    question = ques.fetchall()
    question = str(question[number])
    question = question[2:len(question) - 3]
    body = sid + str(number + 1)
    payload = constants.surveyDatePayload % (question, body,)
    return payload


def generatechoice(sid, number):
    ques = engine.execute(constants.queryQuestionSurvey, sid)
    question = ques.fetchall()
    question = str(question[number])
    question = question[2:len(question) - 3]
    parts = question.split('","')
    options = ""
    for i in range(1, len(parts) - 1):
        options += constants.choiceOptionWithComma % (parts[i], parts[i],)
    options += constants.choiceOptionWithoutComma % (parts[len(parts) - 1], parts[len(parts) - 1],)
    body = sid + str(number + 1)
    payload = constants.surveyChoicePayload % (parts[0], options, body)
    return payload


def generateheaderquestion(expirytime):
    header = {constants.type: constants.Container, constants.style: constants.emphasis, constants.items: []}
    items = {constants.type: constants.ColumnSet, constants.columns: []}
    col1 = {constants.width: '32px', constants.type: constants.Column, constants.bleed: False, constants.items: []}
    col1item = {constants.type: constants.Image, constants.width: '26px', constants.horizontalAlignment: 'Center',
                'url': constants.Logo}
    col1[constants.items].append(col1item)
    items[constants.columns].append(col1)
    col2 = {constants.width: 'stretch', constants.type: constants.Column, constants.bleed: False, constants.items: []}
    col2item = {constants.type: constants.TextBlock, constants.text: 'Quick Poll', constants.size: 'Large',
                'height': 'stretch'}
    col2[constants.items].append(col2item)
    expiry = datetime.datetime.strptime(expirytime, '%Y-%m-%d %H:%M')
    expiry = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
    expirytime = expiry.strftime('%a') + ' ' + expiry.strftime('%d') + ' ' + expiry.strftime(
        '%b') + ', ' + expiry.strftime('%Y') + ', ' + expiry.strftime('%I') + ':' + expiry.strftime(
        '%M') + ' ' + expiry.strftime('%p')
    col2item2 = {constants.type: constants.TextBlock, constants.text: 'Due by ' + expirytime, 'size': 'small', }
    col2[constants.items].append(col2item2)
    items[constants.columns].append(col2)
    header[constants.items].append(items)
    return header


def generatebody(qid):
    body = {constants.type: constants.Container, 'padding': {'left': 'padding', 'right': 'padding'},
            constants.items: []}
    ques = engine.execute("SELECT ques FROM question WHERE qid = %s", qid)
    question = ques.fetchall()
    question = str(question[0])
    question = question[2:len(question) - 3]
    questionbody = {constants.text: '**' + question + '**', 'wrap': True, 'type': constants.TextBlock,
                    'separator': True}
    body[constants.items].append(questionbody)
    choice = {'id': 'Poll', 'type': 'Input.ChoiceSet', constants.style: 'expanded', 'isMultiSelect': False,
              'choices': []}
    queryChoice = engine.execute("SELECT choice FROM question WHERE qid = %s", qid)
    name = queryChoice.fetchall()
    choices = str(name[0]).split(',')
    choices[0] = choices[0][2:]
    choices[len(choices) - 2] = choices[len(choices) - 2][:len(choices[len(choices) - 2]) - 1]
    for i in range(len(choices) - 1):
        option = {'title': choices[i], 'value': choices[i]}
        choice['choices'].append(option)
    body[constants.items].append(choice)
    return body


def generateaction(qid):
    body = {constants.type: constants.Container,
            'padding': {'left': 'padding', 'right': 'padding', 'bottom': 'padding'}, constants.items: []}
    actionbody = {constants.type: 'ActionSet', 'actions': []}
    actionbodys = {'method': 'POST', constants.body: '{{Poll.value}}#' + qid, 'title': 'Submit', 'isPrimary': True,
                   constants.type: 'Action.Http'}
    responsevisibility = engine.execute("SELECT responsevisibility FROM survey WHERE sid = %s", qid)
    responsevisibility = responsevisibility.fetchall()
    responsevisibility = str(responsevisibility[0])
    responsevisibility = responsevisibility[2:len(responsevisibility) - 3]
    if (responsevisibility == "1"):
        actionbodys['url'] = 'https://amcompose.azurewebsites.net/submitResponse'
    else:
        actionbodys['url'] = 'https://amcompose.azurewebsites.net/submitResponseVisible'
    actionbody['actions'].append(actionbodys)
    body[constants.items].append(actionbody)
    return body


def generatequestion(qid, expirytime):
    payload = {constants.type: 'AdaptiveCard', 'version': '1.0', 'padding': 'none',
               'originator': constants.Originator, constants.body: [],
               'autoInvokeAction': {'type': 'Action.Http', 'method': 'POST', 'hideCardOnInvoke': False, 'body': qid,
                                    'url': 'https://amcompose.azurewebsites.net/pollcard'}}

    header = generateheaderquestion(expirytime)
    bodyquestion = generatebody(qid)
    actionbody = generateaction(qid)
    payload[constants.body].append(header)
    payload[constants.body].append(bodyquestion)
    payload[constants.body].append(actionbody)
    payload = json.dumps(payload)
    payload = str(payload)
    return payload


@app.route("/pollcard", methods=['POST', 'GET'])
def pollcard():
    qid = request.data
    qid = qid.decode(constants.UTF8)
    x = datetime.datetime.now()
    date = x.strftime("%Y") + "-" + x.strftime("%m") + "-" + x.strftime("%d") + " " + x.strftime(
        "%H") + ":" + x.strftime("%M")
    expirytime = engine.execute("SELECT expirytime FROM survey WHERE sid = %s", qid)
    expirytime = expirytime.fetchall()
    expirytime = str(expirytime[0])
    expirytime = expirytime[2:len(expirytime) - 3]
    if expirytime >= date:
        payload = generatequestion(qid, expirytime)
    else:
        payload = constants.sorryPayload
    resp = Response(payload)
    resp.headers['CARD-UPDATE-IN-BODY'] = True
    resp.headers['Content-Type'] = 'application/json'
    return resp


def generateheader():
    header = {constants.type: constants.Container, constants.style: constants.emphasis, constants.items: []}
    items = {constants.type: constants.ColumnSet, constants.columns: []}
    col1 = {constants.width: '32px', 'type': constants.Column, constants.bleed: False, constants.items: []}
    col1item = {constants.type: constants.Image, constants.width: '26px', constants.horizontalAlignment: 'Center',
                'url': constants.Logo}
    col1[constants.items].append(col1item)
    items[constants.columns].append(col1)
    col2 = {constants.width: 'stretch', constants.type: constants.Column, constants.bleed: False, constants.items: []}
    col2item = {constants.type: constants.TextBlock, constants.text: 'Quick Poll', constants.size: 'Large',
                'height': 'stretch'}
    col2[constants.items].append(col2item)
    items[constants.columns].append(col2)
    col3 = {constants.width: 'auto', 'type': constants.Column, constants.bleed: False, constants.items: []}
    col3items = {constants.type: constants.TextBlock, constants.text: '[Refresh](action:inlineActionID)',
                 constants.size: 'Large', 'color': 'accent',
                 'height': 'stretch'}
    col3[constants.items].append(col3items)
    items[constants.columns].append(col3)
    header[constants.items].append(items)
    return header


def generatecount(qid, results):
    countresult = {constants.type: constants.Container, 'separator': 'true', 'spacing': 'none',
                   'padding': {'right': 'padding', 'left': 'padding', 'bottom': 'padding', 'top': 'padding'},
                   constants.items: []}
    item = {constants.type: constants.TextBlock, constants.size: 'Large', 'wrap': True}
    count = 0
    for i in range(len(results)):
        count = count + results[i]
    queryCount = engine.execute("SELECT count FROM receipients WHERE qid = %s", qid)
    tcount = queryCount.fetchall()

    tcount = str(tcount[0])[1:len(tcount[0]) - 3]
    total = int(tcount)
    item[constants.text] = str(count) + ' out of ' + str(total) + ' people have responded'
    countresult[constants.items].append(item)
    return countresult


def generatestatistics(qid, question, Options, results):
    question = question[2:len(question) - 3]
    question = "**" + question + "**"
    stats = {constants.type: constants.Container, 'separator': 'true', 'spacing': 'none',
             'padding': {'right': 'padding', 'left': 'padding', 'bottom': 'padding', 'top': 'padding'},
             constants.items: []}
    items1 = {constants.type: constants.TextBlock, constants.text: question, constants.size: 'Large', 'wrap': True}
    stats[constants.items].append(items1)
    sizes = []
    queryCount = engine.execute("SELECT count FROM receipients WHERE qid = %s", qid)
    tcount = queryCount.fetchall()
    count = str(tcount[0])[1:len(tcount[0]) - 3]
    total = int(count)
    for i in range(len(results)):
        size = (300 * results[i]) / total
        size = int(size)
        sizes.append(size)
    for i in range(len(Options) - 1):
        items = {constants.type: constants.TextBlock,
                 constants.text: Options[i] + ' - ' + str(results[i]) + '/' + str(total), constants.size: 'Large',
                 'wrap': True}
        stats[constants.items].append(items)
        titems = {constants.type: constants.Image, 'spacing': 'none', 'padding': 'none', 'padding': 'none',
                  'height': '10px',
                  'url': constants.bar,
                  constants.width: str(sizes[i]) + 'px'}
        if sizes[i] == 0:
            titems['isVisible'] = False
        stats['items'].append(titems)
    return stats


def generateRefreshButton(qid):
    button = {constants.type: 'ActionSet', 'actions': []}
    buttonaction = {constants.type: 'Action.Http', constants.method: 'POST',
                    'url': 'https://amcompose.azurewebsites.net/fetchLatestResponses', constants.body: qid,
                    'title': 'Get Latest Responses', 'isPrimary': True}
    button['actions'].append(buttonaction)
    return button


def generatePayloadStatistics(qid, question, Options, results):
    payload = {constants.type: 'AdaptiveCard', constants.version: '1.0', 'padding': 'none',
               constants.textOriginator: constants.Originator, constants.body: []}
    payload[constants.body].append(generateheader())
    payload[constants.body].append(generatecount(qid, results))
    payload[constants.body].append(generatestatistics(qid, question, Options, results))
    payload['autoInvokeAction'] = {constants.type: 'Action.Http', constants.method: 'POST', 'hideCardOnInvoke': False,
                                   'url': 'https://amcompose.azurewebsites.net/fetchLatestResponses',
                                   constants.body: qid}
    payload[constants.resources] = {constants.actions: []}
    resourceactions = {'id': 'inlineActionID', constants.type: 'Action.Http', constants.method: 'POST',
                       'title': 'Refresh',
                       'url': 'https://amcompose.azurewebsites.net/fetchLatestResponses', constants.body: qid}
    payload[constants.resources][constants.actions].append(resourceactions)
    return payload


@app.route("/submitResponseVisible", methods=['POST'])
def submitResponseVisible():
    temp = request.data
    temp = temp.decode(constants.UTF8)
    lt = temp.split('#')
    response = lt[0]
    qid = lt[1]
    engine.execute("INSERT INTO responses (qid,response) VALUES (%s,%s)", (qid, response))
    r = []
    queryChoice = engine.execute("SELECT choice FROM question WHERE qid = %s", qid)
    name = queryChoice.fetchall()
    choices = str(name[0]).split(',')
    choices[0] = choices[0][2:]
    choices[len(choices) - 2] = choices[len(choices) - 2][:len(choices[len(choices) - 2]) - 1]
    queryChoice = engine.execute("SELECT ques FROM question WHERE qid = %s", qid)
    name = queryChoice.fetchall()
    question = str(name[0])
    for i in range(len(choices) - 1):
        result = engine.execute("SELECT * FROM responses WHERE qid = %s and response= %s", (qid, choices[i]))
        r.append(result.rowcount)
    payload = generatePayloadStatistics(qid, question, choices, r)
    payload = json.dumps(payload)
    payload = str(payload)
    resp = Response(payload)
    resp.headers['CARD-UPDATE-IN-BODY'] = True
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route("/submitResponse", methods=['POST'])
def submitResponse():
    temp = request.data
    temp = temp.decode(constants.UTF8)
    lt = temp.split('#')
    response = lt[0]
    qid = lt[1]
    engine.execute("INSERT INTO responses (qid,response) VALUES (%s,%s)", (qid, response))
    ques = engine.execute("SELECT ques FROM question WHERE qid = %s", qid)
    question = ques.fetchall()
    question = str(question[0])
    question = question[2:len(question) - 3]
    payload = constants.responsepayload % (question, response,)
    resp = Response(payload)
    resp.headers['CARD-UPDATE-IN-BODY'] = True
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route("/getResponses", methods=['POST'])
def getResponses():
    qid = request.data
    qid = qid.decode(constants.UTF8)
    r = ""
    queryChoice = engine.execute("SELECT choice FROM question WHERE qid = %s", qid)
    name = queryChoice.fetchall()
    choices = str(name[0]).split(',')
    choices[0] = choices[0][2:]
    choices[len(choices) - 2] = choices[len(choices) - 2][:len(choices[len(choices) - 2]) - 1]
    for i in range(len(choices) - 1):
        result = engine.execute("SELECT * FROM responses WHERE qid = %s and response= %s", (qid, choices[i]))
        r = r + choices[i] + "= " + str(result.rowcount)
        r = r + "\n"
    return r


@app.route("/fetchLatestResponses", methods=['POST', 'GET'])
def fetchLatestResponses():
    qid = request.data
    qid = qid.decode(constants.UTF8)
    r = []
    queryChoice = engine.execute("SELECT choice FROM question WHERE qid = %s", qid)
    name = queryChoice.fetchall()
    choices = str(name[0]).split(',')
    choices[0] = choices[0][2:]
    choices[len(choices) - 2] = choices[len(choices) - 2][:len(choices[len(choices) - 2]) - 1]
    queryChoice = engine.execute("SELECT ques FROM question WHERE qid = %s", qid)
    name = queryChoice.fetchall()
    question = str(name[0])
    for i in range(len(choices) - 1):
        result = engine.execute("SELECT * FROM responses WHERE qid = %s and response= %s", (qid, choices[i]))
        r.append(result.rowcount)
    payload = generatePayloadStatistics(qid, question, choices, r)
    payload = json.dumps(payload)
    payload = str(payload)
    resp = Response(payload)
    resp.headers['CARD-UPDATE-IN-BODY'] = True
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route("/sendEmail", methods=['POST'])
def sendEmail():
    qid = request.data
    qid = qid.decode(constants.UTF8)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = constants.emailSubject
    msg['From'] = "{}".format(constants.emailid)
    msg['To'] = "{}".format(constants.emailid)
    html = constants.emailhtml % (qid,)
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    mail = smtplib.SMTP(constants.emailServer, constants.emailPort)
    mail.ehlo()
    mail.starttls()
    mail.login(constants.emailid, constants.passwd)
    mail.sendmail(constants.emailid, constants.emailid, msg.as_string())
    mail.quit()
    return "HELL0"


@app.route("/getHtmlTemplate", methods=['GET'])
def getHtml():
    f = codecs.open("template.html", 'r')
    return f.read()


