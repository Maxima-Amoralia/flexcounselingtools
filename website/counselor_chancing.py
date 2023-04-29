from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .models import StudentDatabase
from .models import SelectedCollege
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


counselor_chancing = Blueprint('counselor_chancing', __name__)

@counselor_chancing.route("/counselor_chancing", methods=["POST","GET"])
@login_required
def loadStudentDatabase():
    
    counselor = request.args.get('counselor','')
    counselor = counselor.replace('_', ' ')

    print(counselor)

    if current_user.first_name == 'Alex' and current_user.last_name == 'Chang' and counselor=='':
        counselor='Alexander Chang'
    
    if counselor == '' or counselor == 'All':
        janStart = StudentDatabase.query.filter_by(start_date='01 Jan Start').order_by(StudentDatabase.student_name).all()
        marStart = StudentDatabase.query.filter_by(start_date='03 Mar Start').order_by(StudentDatabase.student_name).all()
        junStart = StudentDatabase.query.filter_by(start_date='06 Jun Start').order_by(StudentDatabase.student_name).all()
    else:
        janStart = StudentDatabase.query.filter_by(counselor=counselor, start_date='01 Jan Start').order_by(StudentDatabase.student_name).all()
        marStart = StudentDatabase.query.filter_by(counselor=counselor, start_date='03 Mar Start').order_by(StudentDatabase.student_name).all()
        junStart = StudentDatabase.query.filter_by(counselor=counselor, start_date='06 Jun Start').order_by(StudentDatabase.student_name).all()

    return render_template("counselor_chancing.html", jan_start=janStart, mar_start=marStart, jun_start=junStart)


@counselor_chancing.route("/counselor_chancing/update_chancing", methods=["POST","GET"])
@login_required
def updateChancing():

    input = json.loads(request.data)
    collegeName = input['college_name'].replace('_', ' ')

    college = SelectedCollege.query.filter_by(student_id=input['student_id'], college_name=collegeName).first()
    college.counselor_chancing=input['chancing'];
    db.session.commit()

    student = StudentDatabase.query.filter_by(id=input['student_id']).first();
    student.counselor_chancing = True
    db.session.commit()

    print('Chancing Updated')

    return '0'


@counselor_chancing.route("/counselor_chancing/load_student_data", methods=["POST","GET"])
@login_required
def studentdata():

    input = json.loads(request.data)    

    student = StudentDatabase.query.filter_by(id=input['id']).first()

    if student.counselor == "":
        setCounselor = "None Assigned"
    else:
        setCounselor = student.counselor


    collegeList = []

    colleges = SelectedCollege.query.filter_by(student_id=input['id']).all()

    for college in colleges:
        collegeList.append([college.college_name, college.student_chancing, college.ml_chancing, college.committee_chancing, college.committee_chancing])
        college.counselor_chancing = college.committee_chancing
    db.session.commit()
    
    print(collegeList)

    import pickle

    file_name = 'chancing_models.pkl'
    models = []

    with open(file_name, 'rb') as f:
        while True:
            try:
                models = pickle.load(f)
            except EOFError:
                break

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
        'major_group' : student.major_group,
        'colleges': collegeList
    }

    return output


@counselor_chancing.route("/counselor_chancing/save_selectivity_map", methods=["POST","GET"])
@login_required
def saveMap():

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.oauth2 import service_account
    
    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/documents',
              'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive.metadata']

    creds = None

    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    docService = build('docs', 'v1', credentials=creds)

    driveService = build('drive', 'v3', credentials=creds)

    OUTPUT_FOLDER_ID = '1WTwY9noEWT9U1mgqsLyWDDmTgUjfLuLa'

    file_metadata = {
        'name': 'hello3',
        'mimeType': 'application/vnd.google-apps.document'
    }

    body = {
        'title': 'hello'        
    }


    file = driveService.files().create(body=file_metadata, media_body='', supportsAllDrives=True, fields='id').execute()
    file_id = file.get('id')

    file = driveService.files().update(fileId=file_id, addParents=OUTPUT_FOLDER_ID, supportsAllDrives = True, fields='id, parents').execute()
    

    return '0'