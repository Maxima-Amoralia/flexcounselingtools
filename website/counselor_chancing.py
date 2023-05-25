from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
from .models import StudentDatabase
from .models import SelectedCollege
from .models import CollegeDatabase
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

    collegeData = CollegeDatabase.query.order_by(CollegeDatabase.college_name).all()

    return render_template("counselor_chancing.html", jan_start=janStart, mar_start=marStart, jun_start=junStart, college_data=collegeData)


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

    return '0'



@counselor_chancing.route("/counselor_chancing/update_rec", methods=["POST","GET"])
@login_required
def updateRec():

    input = json.loads(request.data)        
    collegeName = input['college_name'].replace('_', ' ')

    college = SelectedCollege.query.filter_by(student_id=input['student_id'], college_name=collegeName).first()
    
    college.counselor_rec=input['counselor_rec']
    db.session.commit()    

    student = StudentDatabase.query.filter_by(id=input['student_id']).first();
    student.counselor_chancing = True
    db.session.commit()

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
        collegeList.append([college.college_name, college.student_chancing, college.ml_chancing, college.committee_chancing, college.counselor_chancing, college.counselor_rec])        
    
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

    templateId = '1wW--iQ3J_wtR6gAMMGOWUvk45REvXaDA1Sj9DkL8QNc'

    input = json.loads(request.data)    
    colleges = SelectedCollege.query.filter_by(student_id=input['id']).all()
    student = StudentDatabase.query.filter_by(id = input['id']).first()

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
    
    template =  docService.documents().get(documentId=templateId).execute()
    lastContentIndex = len(template.get('body').get('content'))-1

    file_name = 'Selectivity Map - '+student.student_name

    file = driveService.files().copy(fileId=templateId, supportsAllDrives=True, body={'parents': [student.google_folder.replace('https://drive.google.com/drive/folders/', '')], 'name': file_name}).execute()
    file_id = file.get('id')

    requests = []
    
    tableStartIndex = template.get('body').get('content')[lastContentIndex].get('endIndex')
    tableLocations = []

    tableLocations.insert(0, tableStartIndex)

    for x, college in enumerate(colleges):
        addRequest = {'insertTable':
                        {
                            'rows':1,
                            'columns':2,
                            'endOfSegmentLocation': {'segmentId':''},
                        }
                    }

        requests.append(addRequest)

        tableLocation = 8*x+tableStartIndex

        tableLocations.insert(0, tableLocation)

        updateCellStyle = {
            "updateTableCellStyle": {
                "tableCellStyle": {
                    "borderTop": {
                        "color": {"color": {"rgbColor": {}}},
                        "width": {"magnitude": 0, "unit": "PT"},
                        "dashStyle": "SOLID"
                    },
                    "borderBottom": {
                        "color": {"color": {"rgbColor": {}}},
                        "width": {"magnitude": 0, "unit": "PT"},
                        "dashStyle": "SOLID"
                    },
                    "borderLeft": {
                        "color": {"color": {"rgbColor": {}}},
                        "width": {"magnitude": 0, "unit": "PT"},
                        "dashStyle": "SOLID"
                    },
                    "borderRight": {
                        "color": {"color": {"rgbColor": {}}},
                        "width": {"magnitude": 0, "unit": "PT"},
                        "dashStyle": "SOLID"
                    },
                    "paddingTop": {"magnitude": 3, "unit": "PT"},
                    "paddingBottom": {"magnitude": 3, "unit": "PT"},
                    "paddingLeft": {"magnitude": 3, "unit": "PT"},
                    "paddingRight": {"magnitude": 3, "unit": "PT"},
                },
                "fields": "*",
                "tableRange": {
                    "columnSpan": 2,
                    "rowSpan": 1,
                    "tableCellLocation": {
                        "columnIndex": 0,
                        "rowIndex": 0,
                        "tableStartLocation": {
                        "index": tableLocation
                        }
                    }
                }
            }
        }
        requests.append(updateCellStyle)

    reversedList = []

    for college in colleges:
        reversedList.insert(0, college)

   
    for x, college in enumerate(reversedList):

        insertIndex = tableLocations[x]+3

        uWidth=140

        if college.counselor_chancing == "Far Reach":
            targetColumn = 0
            insertIndexIncrement = 0
            c0Width = uWidth
        elif college.counselor_chancing =="Reach": 
            targetColumn = 1
            insertIndexIncrement = 2
            c0Width = 141-uWidth/2
            c1Width = uWidth
        elif college.counselor_chancing =="Target": 
            targetColumn = 1
            insertIndexIncrement = 2
            c0Width = (468-uWidth)/2
            c1Width = uWidth
        elif college.counselor_chancing =="Likely": 
            targetColumn = 1
            insertIndexIncrement = 2
            c0Width = 327-uWidth/2
            c1Width = uWidth
        elif college.counselor_chancing =="Very Likely": 
            targetColumn = 1
            insertIndexIncrement = 2
            c0Width = 468-uWidth
            c1Width = uWidth

        red = 0;
        green = 0;
        blue = 0;

        if(college.counselor_rec=='Alternate Major'):
            red = .902
            green = .569
            blue = .220
        elif(college.counselor_rec=='Not Recommended'):
            red = 1
            green = 0
            blue = 0
        elif(college.counselor_rec=='Early Action'):
            red = .416
            green = .659
            blue = .310
        elif(college.counselor_rec=='Early Decision'):
            red = .220
            green = .463
            blue = .114
        else:
            red = .404
            green=.529
            blue=.718


        updateStyle = {
            "updateTableCellStyle": {
                "tableCellStyle": {
                    "backgroundColor": {"color": {"rgbColor": {"red": red, "green": green, "blue": blue}}},
                },
                "fields": "backgroundColor",
                "tableRange": {
                "columnSpan": 1,
                "rowSpan": 1,
                "tableCellLocation": {
                    "columnIndex": targetColumn,
                    "rowIndex": 0,
                    "tableStartLocation": {
                    "index": tableLocations[x]
                    }
                }
                }
            }
        }
        requests.append(updateStyle)

        insertIndex = insertIndex + insertIndexIncrement

        insertText = {
            'insertText': {
                'location': {
                    'index': insertIndex,
                },
                'text': college.college_name
            }
        }
        requests.append(insertText)

        updateTextStyle = {
            'updateTextStyle': {
                'range': {
                    'startIndex': insertIndex-1,
                    'endIndex': insertIndex+len(college.college_name)
                },
                'textStyle': {
                    "bold": False,
                    "italic": False,
                    "foregroundColor": {"color": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}}, 
                    'fontSize': {
                        "magnitude": 10,
                        "unit": "PT"
                    }
                },
                'fields': 'fontSize, bold, italic, foregroundColor'                
            }
        }
        requests.append(updateTextStyle)

        updateParagraphStyle = {
            "updateParagraphStyle": {
                'range': {
                    'startIndex': insertIndex,
                    'endIndex': insertIndex+len(college.college_name)
                },
                "paragraphStyle": {
                    "alignment":"CENTER"
                },
                "fields": 'alignment'
            }
        }
        requests.append(updateParagraphStyle)


        updateColumns = [{'updateTableColumnProperties': {
            'tableStartLocation': {'index': tableLocations[x]},
            'columnIndices': [0],
            'tableColumnProperties': {
                'widthType': 'FIXED_WIDTH',
                'width': {
                'magnitude': c0Width,
                'unit': 'PT'
                }
            },
            'fields': '*'
            }},
            {'updateTableColumnProperties': {
            'tableStartLocation': {'index': tableLocations[x]},
            'columnIndices': [1],
            'tableColumnProperties': {
                'widthType': 'FIXED_WIDTH',
                'width': {
                'magnitude': c1Width,
                'unit': 'PT'
                }
            },
            'fields': '*'
            }}
            ]

        
        requests.append(updateColumns)

    docService.documents().batchUpdate(documentId=file_id, body={'requests': requests}).execute()

    requests = [];

    firstName = student.student_name[0: student.student_name.index(' ')]

    replaceText = [
            {
            'replaceAllText': {
                'containsText': {
                    'text': '<studentFullName>',
                    'matchCase':  'true'
                },
                'replaceText': student.student_name,
            }}, {
            'replaceAllText': {
                'containsText': {
                    'text': '<highSchool>',
                    'matchCase':  'true'
                },
                'replaceText': student.high_school,
            }}, {
            'replaceAllText': {
                'containsText': {
                    'text': '<studentId>',
                    'matchCase':  'true'
                },
                'replaceText': str(student.id),
            }},{
            'replaceAllText': {
                'containsText': {
                    'text': '<studentName>',
                    'matchCase':  'true'
                },
                'replaceText': str(firstName),
            }},
                     
            
        ]

    requests.append(replaceText)
    docService.documents().batchUpdate(documentId=file_id, body={'requests': requests}).execute()



    return '0'