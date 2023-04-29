from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .models import StudentData


resultsdata = Blueprint('resultsdata', __name__)


@resultsdata.route("/resultsdata", methods=["POST","GET"])
@login_required
def results():

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient import errors
    from googleapiclient.discovery import build

    from google.oauth2 import service_account

    import pandas as pd

    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None

    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    print(creds.scopes)

    DATA_SHEET_ID = '1SKbP017fzVOXeL6_uoeoQIwl13O5Jn3_7UUrl0yIXx4'

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = DATA_SHEET_ID, range = "'ACE Data'!A1:AP170").execute()


    return render_template("resultsdata.html", students=result)



@resultsdata.route("/resultsdata/add", methods=["POST","GET"])
@login_required
def addresults():
    if request.method == 'POST':
        results = json.loads(request.data)

        xsearch = results['x-axis']
        ysearch = results['y-axis']
        
        college=results['college']
        major_gen=results['major_gen']

        arguments = {}

        if ((college=="any") & (major_gen=="null")):
            targetStudents = StudentData.query.all();
        else:
            if (college!="any"):
                college="'"+college+"'"
                arguments[eval(college)] = "TRUE" 
            if (major_gen!="null"):
                major_gen="'"+major_gen+"'"
                arguments["major_gen"] = eval(major_gen)            
            targetStudents = StudentData.query.filter_by(**arguments)
        

        data = []

        for x in targetStudents:
            if (eval('x.'+xsearch)!=0) & (eval('x.'+ysearch)!=0):
                data.append([eval('x.'+xsearch), eval('x.'+ysearch)])
        return data
    else:
        return render_template("resultsdata.html")


@resultsdata.route("/resultsdata/load", methods=["POST","GET"])
@login_required
def loadresults():

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient import errors
    from googleapiclient.discovery import build

    from google.oauth2 import service_account

    import pandas as pd

    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None

    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    print(creds.scopes)

    DATA_SHEET_ID = '1SKbP017fzVOXeL6_uoeoQIwl13O5Jn3_7UUrl0yIXx4'

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = DATA_SHEET_ID, range = "'ACE Data'!A1:AP170").execute()

    values = result.get('values', [])

    index = 0

    for x in values[0]:    
        print(x)
        if x=='gpa_uw':
            gpa_uwCol = index
        if x=='gpa_w':
            gpa_wCol = index
        if x=='num_ap':
            num_apCol = index
        if x=='num_hon':
            num_honCol = index
        if x=='num_ib':
            num_ibCol = index
        if x=='num_weighted':
            num_weightedCol = index
        if x=='highest_test':
            highest_testCol = index
        if x=='num_ap_exams':
            num_ap_examsCol = index
        if x =='avg_ap_score':
            avg_ap_scoreCol = index
        if x =='high_school':
            high_schoolCol = index
        if x =='major':
            majorCol = index
        if x =='major_gen':
            major_genCol = index

        if x=='berkeley':
            berkeleyCol = index
        if x=='davis':
            davisCol = index
        if x=='irvine':
            irvineCol = index
        if x=='los_angeles':
            los_angelesCol = index
        if x=='merced':
            mercedCol = index
        if x=='riverside':
            riversideCol = index
        if x=='san_diego':
            san_diegoCol = index
        if x=='santa_barbara':
            santa_barbaraCol = index
        if x=='santa_cruz':                                                           
            santa_cruzCol = index
        index = index+1

    print('-------------------------')

    for x in values:
        student = StudentData.query.filter_by(student_id=x[0]).first()

        if not student:
            new_student = StudentData(student_id=x[0], last_name=x[1], first_name=x[2], high_school=x[high_schoolCol], major_gen=x[major_genCol], major=x[majorCol], gpa_uw=x[gpa_uwCol], gpa_w=x[gpa_wCol], 
                                        num_ap = x[num_apCol], num_ib=x[num_ibCol], num_hon=x[num_honCol], num_weighted=x[num_weightedCol], highest_test=x[highest_testCol],
                                        num_ap_exams=x[num_ap_examsCol], avg_ap_score=x[avg_ap_scoreCol], berkeley=x[berkeleyCol], davis=x[davisCol], irvine=x[irvineCol],
                                        los_angeles=x[los_angelesCol], merced=x[mercedCol], riverside=x[riversideCol], san_diego=x[san_diegoCol], santa_barbara=x[santa_barbaraCol],
                                        santa_cruz=x[santa_cruzCol])
            db.session.add(new_student)
            db.session.commit()
    return render_template("resultsdata.html")