# pip install Flask-CKEditor

from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)
app.config["SECRET_KEY"] = "My secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
ckeditor = CKEditor(app)    # CREATING instance of CKEditor with out app
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    note = db.Column(db.String(), nullable = False, unique=True)
    
class NoteForm(FlaskForm):
    username = StringField("Enter your username: ", validators=[DataRequired()])
    note = CKEditorField("Your notes here", validators=[DataRequired()])
    submit = SubmitField()

@app.route("/", methods=["GET", "POST"])
def index():
    form = NoteForm()
    if form.validate_on_submit():
        note = Notes.query.filter_by(note = form.note.data).first()
        if note is None:
            note = Notes(username = form.username.data, 
                         note = form.note.data) 
            db.session.add(note)
            db.session.commit()
            flash("Note added successfully!!")
        else:
            flash("Note already exists!!")
        form.username.data = ""
        form.note.data = ""
    all_notes = Notes.query.all()
    return render_template("index.html", form=form, all_notes = all_notes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')    
    # hosting at 0.0.0.0 for public otherwise will be localhost 
    # and debugginf set to False
