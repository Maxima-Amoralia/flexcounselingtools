#===========================================

from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

from google.oauth2 import service_account

import pandas as pd
#===========================================




from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, CA_Activity
from . import db
import json






views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)



@views.route('/dactivities', methods=['GET', 'POST'])
@login_required
def dactivities():
    
    if request.method == 'POST':
        activity_type = request.form.get('activity_type')
        position = request.form.get('position')
        organization = request.form.get('organization')
        description = request.form.get('description')

        print(request.data)

        if request.form.get('action') == 'update':
            activityId = request.form.get('activityId')
            activity = CA_Activity.query.get(activityId)
            
            if activity:
                if activity.user_id == current_user.id:
                    activity.activity_type = activity_type
                    activity.position = position
                    activity.organization = organization
                    activity.description = description
                    db.session.commit()

        else:
            new_ca_activity = CA_Activity(activity_type=activity_type, position=position, organization=organization, description=description, user_id=current_user.id)
            db.session.add(new_ca_activity)
            db.session.commit()

    return render_template("activities.html", user=current_user)


@views.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():
    if request.method == 'POST':

        action = request.form.get('action')
        
        if action == 'addnew':

            activity_type = request.form.get('activity_type')
            position = request.form.get('position')
            organization = request.form.get('organization')
            description = request.form.get('description')

            new_ca_activity = CA_Activity(activity_type=activity_type, position=position, organization=organization, description=description, user_id=current_user.id)
            db.session.add(new_ca_activity)
            db.session.commit()

        else: 
            activity = json.loads(request.data)

            activity_type = activity['activity_type']
            position = activity['position']
            organization = activity['organization']
            description = activity['description']
            activityId = activity['activityId']

            activity = CA_Activity.query.get(activityId)
                
            if activity:
                if activity.user_id == current_user.id:
                    activity.activity_type = activity_type
                    activity.position = position
                    activity.organization = organization
                    activity.description = description
                    db.session.commit()

    return render_template("activities.html", user=current_user)

@views.route('delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('delete-ca_activity', methods=['POST'])
def save_ca_activity():
    activity = json.loads(request.data)
    activityId = activity['activityId']
    activity = CA_Activity.query.get(activityId)
    if activity:
        if activity.user_id == current_user.id:
            db.session.delete(activity)
            db.session.commit()
    return jsonify({})

@views.route("/test", methods=["POST","GET"])
#@login_required
def test():
    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None

    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

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

    print(index)
    print ('Average Unweighted GPA: ' + str(tot_gpa_uw/index))
    print ('Average Weighted GPA: '+ str(tot_gpa_w/index))
    print ('Total Weighted Courses: ' + str(tot_weighted/index))
    print('Average AP Score: ' + str(tot_avg_ap/index))


    import numpy as np
    import matplotlib
    from matplotlib import pyplot as plt

    ys = 200 + np.random.randn(100)
    x = [x for x in range(len(ys))]

    plt.plot(x, ys, '-')
    plt.fill_between(x, ys, 195, where=(ys > 195), facecolor='g', alpha=0.6)

    plt.title("Sample Visualization")
    plt.show()
    # sheet.values()

    return render_template('test.html')