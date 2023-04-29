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

##########################################################################################

@views.route('/dactivities', methods=['GET', 'POST'])
@login_required
def dactivities():
    
    if request.method == 'POST':
        activity_type = request.form.get('activity_type')
        position = request.form.get('position')
        organization = request.form.get('organization')
        description = request.form.get('description')

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

##########################################################################################

@views.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():

    if request.method == 'POST':
    
        action = request.form.get('action')

        print(request.form)

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

##########################################################################################

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

##########################################################################################

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

##########################################################################################
