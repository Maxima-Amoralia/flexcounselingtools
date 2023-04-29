from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .models import StudentDatabase
from .models import SelectedCollege
from .models import CollegeDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


load_data = Blueprint('load_data', __name__)

@load_data.route("/load_data/college_data", methods=["POST","GET"])
@login_required
def load_college_data():

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

    DATA_SHEET_ID = '1CiqETRaSK1DMuvH73UrNuUG6LvFZOLTw5-u4vCJbqIY'

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = DATA_SHEET_ID, range = "'College List'!A1:A").execute()

    values = result.get('values', [])

    for x in values:
        college = CollegeDatabase.query.filter_by(college_name=x[0]).first()

        if not college:
            new_college = CollegeDatabase(college_name=x[0])
            db.session.add(new_college)
            db.session.commit()
        else:
            db.session.commit()

    return '0'