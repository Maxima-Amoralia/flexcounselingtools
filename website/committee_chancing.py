from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .models import StudentDatabase
from .models import SelectedCollege
from .models import CollegeDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


committee_chancing = Blueprint('committee_chancing', __name__)

@committee_chancing.route("/committee_chancing", methods=["POST","GET"])
@login_required
def loadStudentDatabase():
    studentData = StudentDatabase.query.order_by(StudentDatabase.student_name).all()

    collegeData = CollegeDatabase.query.order_by(CollegeDatabase.college_name).all()
    return render_template("committee_chancing.html", student_data=studentData, college_data=collegeData)


@committee_chancing.route("/committee_chancing/update_chancing", methods=["POST","GET"])
@login_required
def updateChancing():
    
    input = json.loads(request.data)
    
    collegeName = input['college_name'].replace('_', ' ')

    college = SelectedCollege.query.filter_by(student_id=input['student_id']).all();

    for x in college:
        print(x.college_name)

    college = SelectedCollege.query.filter_by(student_id=input['student_id'], college_name=collegeName).first()


    if college:
        college.committee_chancing=input['chancing'];
        db.session.commit()
    else:
        new_college = SelectedCollege(college_name=collegeName, student_id=input['student_id'], committee_chancing=input['chancing'])
        db.session.add(new_college)
        db.session.commit()


    student = StudentDatabase.query.filter_by(id=input['student_id']).first();
    student.committee_chancing = True
    db.session.commit()

    print('Chancing Updated')

    return '0'


@committee_chancing.route("/committee_chancing/load_student_data", methods=["POST","GET"])
@login_required
def studentdata():

    input = json.loads(request.data)    

    student = StudentDatabase.query.filter_by(id=input['id']).first()

    if student.counselor == "":
        setCounselor = "None Assigned"
    else:
        setCounselor = student.counselor

    output = {
        'id' : student.id,
        'student_name' : student.student_name,
        'start_date' : student.start_date,
        'google_folder': student.google_folder,
        'ace_portal' : student.ace_portal,
        'student_email' : student.student_email,
        'gpa_w' : student.gpa_w,
        'eca_rating' : student.eca_rating,
        'counselor' : setCounselor,
        'high_school' : student.high_school,
        'package' : student.package,
        'major_group' : student.major_group
    }

    return output



@committee_chancing.route("/committee_chancing/load_student_colleges", methods=["POST","GET"])
@login_required
def loadStudentColleges():

    temp = json.loads(request.data)
    student = StudentDatabase.query.filter_by(id=temp['id']).first()
    studentName = student.student_name

    collegeList = [];

    colleges = SelectedCollege.query.filter_by(student_id=temp['id']).all()

    if colleges:     
        for college in colleges: 
            collegeList.append([college.college_name, college.student_chancing, college.ml_chancing, college.committee_chancing])

    else:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        from google.oauth2 import service_account

        SERVICE_ACCOUNT_FILE = 'keys.json'
        
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/spreadsheets']

        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('drive', 'v3', credentials=creds)
                
        results = service.files().list(q = "mimeType = 'application/vnd.google-apps.spreadsheet' and name contains 'College Research Worksheet' and name contains '"+studentName+"'",
            pageSize=10, fields="nextPageToken, files(id, name, modifiedTime)").execute()

        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
        
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()            

        import pickle

        file_name = 'chancing_models.pkl'
        models = []

        with open(file_name, 'rb') as f:
            while True:
                try:
                    models = pickle.load(f)
                except EOFError:
                    break

        addedColleges = []

        print(temp['major_group'])

        for item in items:
            result = sheet.values().get(spreadsheetId = item['id'], range = "'Part 1: College Selection'!A10:L90").execute()
            values = result.get('values', [])
            for x in values:
                if len(x)>10:
                    if(x[10]=='Maybe' or x[10]=='Yes') and (x[0] not in addedColleges):

                        addCollege = SelectedCollege.query.filter_by(college_name=x[0], student_id=temp['id']).first()

                        addedColleges.append(x[0])
                        mlChance = ['']
                        for i, model in enumerate(models):                               
                            if (model[0]==x[0]) and (model[1]==temp['major_group'] or model[1]=='all'):
                                clf = model[2]
                                mlChance = clf.predict([[temp['gpa_w'], temp['eca_rating']]])
                                print(mlChance[0])                            

                        if not addCollege:
                            collegeList.append([x[0], x[4], mlChance[0], mlChance[0]])
                            new_college = SelectedCollege(college_name=x[0], student_id=temp['id'], student_chancing=x[4], ml_chancing=mlChance[0], committee_chancing=mlChance[0])
                            db.session.add(new_college)
                            db.session.commit()
                        else:
                            collegeList.append([x[0], x[4], mlChance[0], addCollege.committee_chancing])
                    

    return collegeList


@committee_chancing.route("/committee_chancing/load", methods=["POST","GET"])
@login_required
def loaddata():

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient import errors
    from googleapiclient.discovery import build

    from google.oauth2 import service_account

    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None

    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    DATA_SHEET_ID = '1dAINP6SBOd5wXikFaN6Do0rtvmNyvBw5DkrR9FAhE1E'

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = DATA_SHEET_ID, range = "'All Students'!A2:L1000").execute()

    values = result.get('values', [])


    for x in values:
        student = StudentDatabase.query.filter_by(id=x[0]).first()

        if not student:
            new_student = StudentDatabase(id=x[0], student_name=x[1], counselor=x[2], start_date=x[3], package=x[4], high_school=x[5], google_folder=x[6], ace_portal=x[7], student_email=x[8], gpa_w=x[9], eca_rating=x[10], major_group=x[11])
            db.session.add(new_student)
            db.session.commit()
        else:
            student.student_name=x[1]
            student.counselor=x[2]
            student.start_date=x[3]
            student.package=x[4]
            student.high_school=x[5]
            student.google_folder=x[6]
            student.ace_portal=x[7]
            student.student_email=x[8]
            student.gpa_w=x[9]
            student.eca_rating=x[10]
            student.major_group=x[11]
            db.session.commit()

    query = StudentDatabase.query.order_by(StudentDatabase.student_name).all()
    return render_template('committee_chancing.html', student_data=query)

@committee_chancing.route("/committee_chancing/delete_college", methods=["POST","GET"])
@login_required
def deleteCollege():

    deleteInfo = json.loads(request.data)
    
    college = SelectedCollege.query.filter_by(college_name=deleteInfo['college_name'], student_id=deleteInfo['student_id']).first()

    if college:        
        db.session.delete(college)
        db.session.commit()
    
    return '0'


@committee_chancing.route("/committee_chancing/quick_ml_chancing", methods=["POST","GET"])
@login_required
def quickMLChance():

    chanceInfo = json.loads(request.data)
    
    import pickle

    file_name = 'chancing_models.pkl'
    models = []
    mlChance = ''
    chanced = False

    with open(file_name, 'rb') as f:
        while True:
            try:
                models = pickle.load(f)
            except EOFError:
                break

    for model in enumerate(models):
        if (model[1][0]==chanceInfo['college_name']) and (model[1][1]==chanceInfo['major_group'] or model[1][1]=='all'):
            clf = model[1][2]
            mlChance = clf.predict([[chanceInfo['gpa_weighted'], chanceInfo['eca_rating']]])
            chanced=True

    if chanced:
        mlChance = mlChance[0]
    else:
        mlChance = '-----'

    returnData = {'ml_chancing': mlChance}

    return returnData