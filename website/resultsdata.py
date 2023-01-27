from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, CA_Activity
from . import db
import json
from .models import StudentData


resultsdata = Blueprint('resultsdata', __name__)


@resultsdata.route("/resultsdata", methods=["POST","GET"])
@login_required
def results():

    #from __future__ import print_function

    import os.path

    
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
    result = sheet.values().get(spreadsheetId = DATA_SHEET_ID, range = "'ACE Data'!A1:AO170").execute()

    values = result.get('values', [])

    index = 0

    for x in values[0]:    
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


    index=0
    tot_gpa_uw = 0
    tot_gpa_w = 0
    tot_weighted = 0
    tot_avg_ap = 0

    for x in values:
        if (x[los_angelesCol] == 'TRUE'):
            index = index+1        
            tot_gpa_uw = tot_gpa_uw + float(x[gpa_uwCol])
            tot_gpa_w = tot_gpa_w+ float(x[gpa_wCol])
            tot_weighted = tot_weighted+float(x[num_weightedCol])
            tot_avg_ap = tot_avg_ap + float(x[avg_ap_scoreCol])
            print(x)

    for x in values:
        student = StudentData.query.filter_by(student_id=x[0])


        if not student:
            new_student = StudentData(student_id=x[0], last_name=x[1], first_name=x[2], high_school=x[3], major=x[4], gpa_uw=x[gpa_uwCol], gpa_w=x[gpa_wCol], 
                                        num_ap = x[num_apCol], num_ib=x[num_ibCol], num_hon=x[num_honCol], num_weighted=x[num_weightedCol], highest_test=x[highest_testCol],
                                        num_ap_exams=x[num_ap_examsCol], avg_ap_score=x[avg_ap_scoreCol], berkeley=x[berkeleyCol], davis=x[davisCol], irvine=x[irvineCol],
                                        los_angeles=x[los_angelesCol], merced=x[mercedCol], riverside=x[riversideCol], san_diego=x[san_diegoCol], santa_barbara=x[santa_barbaraCol],
                                        santa_cruz=x[santa_cruzCol])
            db.session.add(new_student)
            db.session.commit()


    berkeleyAdmits = StudentData.query.filter_by(berkeley="TRUE", los_angeles="TRUE")

    studentCount=0
    for x in berkeleyAdmits:
        print(x.first_name)
        studentCount=studentCount+1;
    print(studentCount)

    print(index)
    print ('Average Unweighted GPA: ' + str(tot_gpa_uw/index))
    print ('Average Weighted GPA: '+ str(tot_gpa_w/index))
    print ('Total Weighted Courses: ' + str(tot_weighted/index))
    print('Average AP Score: ' + str(tot_avg_ap/index))

    return render_template("resultsdata.html")