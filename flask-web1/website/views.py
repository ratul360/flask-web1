from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os
from .models import Memo
from . import db, app
import json

views = Blueprint('views', __name__)

app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFIleForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = UploadFIleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.file.data
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            flash('File has been uploaded!', category='success')
        else: 
            memo = request.form.get('memo')
            if len(memo) >= 1:
                new_memo = Memo(data=memo, user_id=current_user.id)  
                db.session.add(new_memo) 
                db.session.commit()
                flash('Memo added!', category='success')

    return render_template("home.html", user=current_user, form=form)


@views.route('/delete-memo', methods=['POST'])
def delete_memo():  
    memo = json.loads(request.data)
    memoId = memo['memoId']
    memo = Memo.query.get(memoId)
    if memo:
        if memo.user_id == current_user.id:
            db.session.delete(memo)
            db.session.commit()

    return jsonify({})