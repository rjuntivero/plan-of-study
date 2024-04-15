from flask import Flask, render_template, request, send_file, Blueprint, jsonify, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from Database import Base, Course
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, createStringObject
import os, io

app = Flask(__name__)

#Database configuration
DB_PATH = 'sqlite:///my_database.db'
engine = create_engine(DB_PATH)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

#Mail Configuration *Change to match live server/domain
app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '3f79243f5a1e151623852c1018bf9213'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

#Homepage Render
@app.route('/')
def index():
    return render_template('index.html')

#Required Courses List
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

#Email Button
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

#Search Bar with Filters
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # Get the search query from the form data
        search_query = request.form['search_query']
        session = DBSession()
        
        # Extract filter options from html (takes in 'name')
        filter1 = request.form.get('filter1')
        filter2 = request.form.get('filter2')
        filter3 = request.form.get('filter3')

        courses = []

        print("Search Query:", search_query)
        print("Filter 1:", filter1)
        print("Filter 2:", filter2)
        print("Filter 3:", filter3)
        # Base query
        query = session.query(Course)
        
        # Subject Filter
        if filter1 and filter1 != "Subject":
            print("Applying Filter 1:", filter1)
            query = query.filter(Course.class_id.startswith(filter1))
        if filter2 and filter2 not in ["", "Semester"]:
            # Semester Filter
            print("Applying Filter 2:", filter2)
            if filter2 == "Fall":
                query = query.filter(Course.fall == 1)
            elif filter2 == "Spring":
                query = query.filter(Course.spring == 1)
            elif filter2 == "Summer":
                query = query.filter(Course.summer == 1)
        if search_query:
            # Prioritize course with matching names
            query = query.filter(Course.cname.ilike(f'%{search_query}%'))
        
        #debug statement
        count_before_filter = query.count()
        print("Count of courses before filter:", count_before_filter)
        
        courses = query.all()
        
        #debug statement
        count_after_filter = len(courses)
        print("Count of courses after filter:", count_after_filter)
        
        session.close()
        
        return render_template('search_results.html', courses=courses, search_query=search_query)

#Add button for Course Catalog Results
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

#PDF Generation (POS Generation) NOT YET IMPLEMENTED/WORKING
@app.route('/generate_pdf', methods=['GET','POST'])
def generate_pdf():
    try:
        # Retrieve form data
        course_id = request.form.get('course_id', '')
        course_name = request.form.get('course_name', '')
        
        #debug statement
        print("Received form data:")
        print("Course ID:", course_id)
        print("Course Name:", course_name)

        # Define path to PDF template
        template_path = os.path.join(app.root_path, 'static', 'POS_Template.pdf')

        # Open the preexisting PDF template
        with open(template_path, 'rb') as template_file:
            reader = PdfReader(template_file)
            writer = PdfWriter()

            # Fill in form fields with data
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                if '/Annots' in page:
                    for annot_num in range(len(page['/Annots'])):
                        annot = reader.get_object(page['/Annots'][annot_num])
                        if '/T' in annot:
                            field_name = annot['/T']
                            if isinstance(field_name, bytes):
                                field_name = field_name.decode('utf-8')
                            # Remove leading and trailing slash and parenthesis
                            field_name = field_name.strip('(/)').strip()
                            print("Field name:", field_name)
                            field_value = None
                            if annot.get('/V') is not None:
                                # Extract field value
                                field_value_obj = annot['/V'].get_object()
                                if '/AS' in field_value_obj:
                                    field_value = field_value_obj['/AS']
                                else:
                                    field_value = field_value_obj
                                print("Field value:", field_value)
                            if field_value is not None:
                                if 'Semester' in field_name and 'Row' in field_name:
                                    # Fill in Semester fields
                                    annot.update({
                                        NameObject("/V"): createStringObject("random fill in the spots")
                                    })
                                    print("Semester field filled.")
                                elif 'CreditsRow' in field_name:
                                    # Fill in CreditsRow fields
                                    annot.update({
                                        NameObject("/V"): createStringObject("random fill in the spots")
                                    })
                                    print("CreditsRow field filled.")
                writer.add_page(page)

            # Define path for output filled PDF
            output_pdf = "filled_plan_of_study.pdf"  

            # Write filled PDF to disk
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)

        # Return the filled PDF as a response
        response = make_response(send_file(output_pdf, as_attachment=True))
        return response

    except Exception as e:
        #exception debugging
        print("Error:", str(e))
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)


