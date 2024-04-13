from flask import Flask, render_template, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from Database import Base, Course
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
import os 

app = Flask(__name__)

DB_PATH = 'sqlite:///my_database.db'
engine = create_engine(DB_PATH)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '3f79243f5a1e151623852c1018bf9213'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')
       
@app.route('/get-required-courses')
def get_required_courses():
    department = request.args.get('department')
    if department == 'computer_science':
        db_session = DBSession()
        computer_science_courses = db_session.query(Course).all()
        required_courses = [{'cname': course.cname, 'completed': course.completed} for course in computer_science_courses]
        db_session.close()
        return jsonify(required_courses)
    else:
        return jsonify([])


@app.route('/add-course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        try:
            course_id = request.form['course_id']
            course_name = request.form['course_name']
            
            db_sesh = DBSession()
            
            # Fetch the course to be updated
            course_to_update = db_sesh.query(Course).filter_by(class_id=course_id).first()
            
            # Update the completed attribute to True
            course_to_update.completed = True
            
            # Commit the changes to the database
            db_sesh.commit()
            
            # Close the session
            db_sesh.close()
            
            # Redirect back to the same page
            return redirect(request.referrer)
        
        except Exception as e:
            # Handle the exception, optionally log it
            return redirect(request.referrer)


@app.route('/send-email', methods=['GET','POST'])
def send_email():
    message = Message(
        subject='Hello',
        recipients=['jirokuntivero@gmail.com'],
        sender=('RJ from Mailtrap', 'mailtrap@demomailtrap.com'),
    )
    message.html = "<b> Hello UNF<\b>, sending you this email for my plan of study from <a href='https://google.com'>Flask app</a>, yuh"
    mail.send(message)

    return "Message sent!"

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # Get the search query from the form data
        search_query = request.form['search_query']
        session = DBSession()
        
        # Fetch courses that match the search query
        courses = session.query(Course).filter(Course.cname.ilike(f'%{search_query}%')).all()
        
        session.close()

        # Render a template with the search results
        return render_template('search_results.html', courses=courses, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
