from flask import Blueprint, render_template, flash, redirect, jsonify
from flask_login import current_user
from ..forms import NewMemoryForm
from ..api import memories
from ..models import Memory
from src import db
from src.models import Memory
from datetime import datetime
from sqlalchemy import func

bp = Blueprint('memory', __name__, url_prefix='/memory')

@bp.route('/', methods=['GET'])
def get_memories():
    memories = Memory.query.filter_by(user_id = current_user.id).all()
    result = []
    for memory in memories:
        result.append(memory.serialize())
    return jsonify(result)

@bp.route('/test', methods=['GET'])
def test_memory():
    current_timestamp = datetime.utcnow()
    memories = Memory.query.filter(func.date(Memory.next_recall_at) <= current_timestamp).all()

    result = []
    for memory in memories:
        result.append(memory.serialize())
    return jsonify(result)



@bp.route('/new_memory', methods=['GET', 'POST'])
def new_memory():
    form = NewMemoryForm()

    if form.validate_on_submit():
        memory = Memory(
            signal = form.signal.data,
            memory = form.memory.data,
            user_id = current_user.id
        )

        db.session.add(memory)
        db.session.commit()

        flash('New memory created!')

        return redirect('/')

    return render_template('main/new_memory.html', form=form)