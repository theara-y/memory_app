from flask import Blueprint, render_template, flash, redirect, request
from flask_login import current_user
from ..forms import NewMemoryForm
from ..api import memories
from ..models import Memory
from src import db
from src.models import Memory
from datetime import datetime, timedelta
from sqlalchemy import func
import json

bp = Blueprint('memory_app', __name__, url_prefix='/memory_app')

@bp.route('/', methods=['GET'])
def index():
    return render_template('memory_app.html')


@bp.route('/create_memory', methods=['GET', 'POST'])
def new_memory():
    form = NewMemoryForm()

    if form.validate_on_submit():

        training_status = 'active'
        if not form.training_status.data:
            training_status = 'inactive'

        memory = Memory(
            prompt = form.prompt.data,
            answer = form.answer.data,
            training_status = training_status,
            user_id = current_user.id
        )

        db.session.add(memory)
        db.session.commit()

        flash('New memory created!')

        return redirect('/')

    return render_template('main/create_memory.html', form=form)


@bp.route('/test_memory', methods=['GET'])
def test_memory():
    current_timestamp = datetime.utcnow()

    memories = Memory.query.filter(func.date(Memory.next_recall_at) <= current_timestamp).all()

    return render_template('main/test_memory.html', memories=memories)


@bp.route('/report_recall_outcome', methods=['PATCH'])
def report_recall_outcome():
    memory_id = request.json['memory_id']
    recall_outcome = request.json['recall_outcome']

    memory = Memory.query.filter_by(id=memory_id).first()
    memory.total_recall_count += 1
    memory.last_recall_outcome = recall_outcome
    memory.last_recall_at = datetime.utcnow()
    memory.last_modified_at = datetime.utcnow()

    if recall_outcome == 'perfect':
        memory.perfect_recall_count += 1
        if memory.recall_duration_days == 0:
            memory.recall_duration_days = 1
        else:
            memory.recall_duration_days *= 2
    elif recall_outcome == 'partial':
        memory.partial_recall_count += 1
        memory.recall_duration_days = 1
        pass
    elif recall_outcome == 'failed':
        memory.failed_recall_count += 1
        memory.recall_duration_days = 1
        pass
    
    memory.next_recall_at = datetime.utcnow() + timedelta(days=memory.recall_duration_days)

    db.session.commit()
    
    return "Success", 200
    


@bp.route('/view_memory', methods=['GET'])
def view_memory():
    memories = Memory.query.filter_by(user_id = current_user.id).all()

    return render_template('main/view_memory.html', memories=memories)