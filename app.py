from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Event Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade="all, delete-orphan")

# Define Registration Model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_email = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

# Create database tables automatically
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    events = Event.query.all()
    return render_template("index.html", events=events)

@app.route("/add_event", methods=["POST"])
def add_event():
    title = request.form.get("title")
    date = request.form.get("date")
    venue = request.form.get("venue")

    if title and date and venue:
        new_event = Event(title=title, date=date, venue=venue)
        db.session.add(new_event)
        db.session.commit()

    return redirect(url_for("home"))

@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    name = request.form.get("student_name")
    email = request.form.get("student_email")

    if name and email:
        new_reg = Registration(student_name=name, student_email=email, event_id=event_id)
        db.session.add(new_reg)
        db.session.commit()

    return redirect(url_for("home"))

@app.route("/event/<int:event_id>")
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_details.html", event=event)

@app.route("/delete/<int:event_id>")
def delete_event(event_id):
    event_to_delete = Event.query.get_or_404(event_id)
    db.session.delete(event_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)