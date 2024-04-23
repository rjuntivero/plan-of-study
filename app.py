from flask import Flask, render_template, request, send_file, Blueprint, jsonify, Response, make_response, request, redirect
from flask_sqlalchemy import SQLAlchemy
from Database import Base, Course
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, createStringObject
import math, os, io
from datetime import datetime

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


@app.route('/reset-completed-attributes')
def reset_completed_attributes_route():
    reset_completed_attributes()  # Reset completed attributes
    return 'Completed attributes reset successfully.'
    
def reset_completed_attributes():
    # Open a new database session
    db_sesh = DBSession()
    try:
        # Reset all completed attributes to False in the database
        db_sesh.query(Course).update({Course.completed: False})
        db_sesh.commit()
        print("Completed attributes reset successfully.")
    except Exception as e:
        # Handle exceptions
        db_sesh.rollback()
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the session
        db_sesh.close()

#Required Courses List
@app.route('/get-required-courses')
def get_required_courses():
    department = request.args.get('department')
    if department:
        db_session = DBSession()
        if department == 'computer_science':
            courses = db_session.query(Course).filter(Course.comp_sci == True).all()
        elif department == 'data_science':
            courses = db_session.query(Course).filter(Course.data_sci == True).all()
        elif department == 'information_science':
            courses = db_session.query(Course).filter(Course.info_sci == True).all()
        elif department == 'information_technology':
            courses = db_session.query(Course).filter(Course.info_tech == True).all()
        elif department == 'information_systems':
            courses = db_session.query(Course).filter(Course.info_sys == True).all()
        else:
            db_session.close()
            return jsonify([])

        required_courses = [{'cname': course.cname, 'completed': course.completed} for course in courses]
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
@app.route('/search', methods=['GET','POST'])
def search():
    session = DBSession()
    default_message = "No Results Matching Search Criteria"

    print("Request Form Data: ", request.form)
    # Get the search query from the form data
    search_query = request.form.get('search_query', '')
    
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
    if filter3 and filter3.strip():
        print("Applying Filter 3:", filter3)
        query = query.filter(Course.class_id.contains(filter3))
    if search_query:
        # Prioritize course with matching names
        query = query.filter(Course.cname.ilike(f'%{search_query}%'))
    
    #debug statement
    #count_before_filter = query.count()
    #print("Count of courses before filter:", count_before_filter)

    courses = query.all()
    #debug statement
    #count_after_filter = len(courses)
    #print("Count of courses after filter:", count_after_filter)
    
    session.close()
    if not courses:
        return render_template('search_results.html', default_message=default_message)

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
            
            course_to_update.completed = True
            
            # Commit the changes to the database
            db_sesh.commit()
            
            # Close the session
            db_sesh.close()
            
            # Return a JSON response indicating success
            return redirect(request.referrer)
        
        except Exception as e:
            # Handle the exception, optionally log it
            return redirect(request.referrer)

#Remove Button for Completed Course Modal
@app.route('/remove-course', methods=['POST'])
def remove_course():
    if request.method == 'POST':
        try:
            course_id = request.form['course_id']
            
            db_sesh = DBSession()
            course_to_update = db_sesh.query(Course).filter_by(class_id=course_id).first()
            course_to_update.completed = False
            db_sesh.commit()
            db_sesh.close()
            
            # Redirect back to the previous page
            return redirect(request.referrer)
        
        except Exception as e:
            return redirect(request.referrer)

#PDF Generation (POS Generation) NOT YET IMPLEMENTED/WORKING
# Plan of Study PDF Generation
@app.route('/generate_pdf', methods=['GET','POST'])
def generatePlanOfStudy():
    # Retrieve form data
    name = request.form.get('NameField')  # Student name
    student_number = request.form.get('N-Number')  # Student number
    create_date = datetime.now().strftime("%Y-%m-%d")
    major = request.form.get('majorDropdown')

    print("Name:", name)
    print("Student Number:", student_number)
    print("Create Date:", create_date)
    print("Major:", major)

    try:
        # Define path to PDF template
        template_path = os.path.join(app.root_path, 'static', 'POS_Template.pdf')

        # Create a PdfWriter object to write to the output PDF
        writer = PdfWriter()

        # Open the preexisting PDF template
        with open(template_path, 'rb') as template_file:
            reader = PdfReader(template_file)

            # Fill in form fields with data
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                if '/Annots' in page:
                    for annot_num in range(len(page['/Annots'])):
                        annot = reader.get_object(page['/Annots'][annot_num])
                        if '/FT' in annot and annot['/FT'] == '/Btn':  # Check if it's a checkbox
                            checkbox_name = annot.get('/T')
                            if isinstance(checkbox_name, bytes):
                                checkbox_name = checkbox_name.decode('utf-8')
                            checkbox_name = checkbox_name.strip('(/)').strip()
                            checkbox_value = 'Yes' if checkbox_name in ['CSMajor', 'DSMajor', 'ISysMajor', 'ISciMajor', 'ITMajor'] and major == checkbox_name.lower() else 'Off'
                            updateCheckboxValues(page, annot, major)
                        elif '/T' in annot:
                            field_name = annot['/T']
                            if isinstance(field_name, bytes):
                                field_name = field_name.decode('utf-8')
                            field_name = field_name.strip('(/)').strip()

                            # Fill out other fields
                            if field_name == 'StudentName':
                                annot.update({NameObject("/V"): createStringObject(name)})
                            elif field_name == 'StudentNumber':
                                annot.update({NameObject("/V"): createStringObject(student_number)})
                            elif field_name == 'CreateDate_af_date':
                                current_date = datetime.now().strftime('%Y-%m-%d')  # Format as desired
                                annot.update({NameObject("/V"): createStringObject(current_date)})
                writer.add_page(page)

            # Define path for output filled PDF
            output_pdf = io.BytesIO()
            writer.write(output_pdf)
            output_pdf.seek(0)
        
        # Return the PDF data as a response
        response = make_response(output_pdf.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=filled_plan_of_study.pdf'

        return response

    except Exception as e:
        # Handle exceptions
        print("Error:", str(e))
        return jsonify(success=False, error=str(e))


def updateCheckboxValues(page, annot, major_value):
    # Map each major to its corresponding checkbox
    checkbox_map = {
        'computer_science': 'CSMajor',
        'data_science': 'DSMajor',
        'information_systems': 'ISysMajor',
        'information_science': 'ISciMajor',
        'information_technology': 'ITMajor'
    }
    # Get the corresponding checkbox name for the selected major
    checkbox_name = checkbox_map.get(major_value)
    if checkbox_name:
        # Loop through each annotation on the page
        for j in range(0, len(page['/Annots'])):
            writer_annot = annot.get_object()
            # Check if the annotation is the checkbox corresponding to the selected major
            if writer_annot.get('/T') == checkbox_name:
                # Update the checkbox value if it matches the major value
                if checkbox_name.lower() == major_value:
                    writer_annot.update({
                        NameObject("/V"): NameObject("/Yes"),
                        NameObject("/AS"): NameObject("/Yes")
                    })
                else:
                    writer_annot.update({
                        NameObject("/V"): NameObject("/Off"),
                        NameObject("/AS"): NameObject("/Off")
                    })


if __name__ == '__main__':
    app.run(debug=True)
