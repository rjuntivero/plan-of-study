from flask import Flask, render_template, request, send_file, Blueprint, jsonify, Response, make_response, request, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
from Database import Base, Course, association_table
from sqlalchemy import create_engine, collate
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, createStringObject
import math, os, io, random
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
    sender_email = request.form.get('from')
    recipient_email = request.form.get('to')
    subject = request.form.get('subject')
    message_content = request.form.get('message')
    attachment_file = request.files.get('attachment')
    cc_email = request.form.get('cc')

    print("Recipient Email:", recipient_email)
    print("Subject:", subject)
    print("Message Content:", message_content)
    if attachment_file:
        print("Attachment File Detected:", attachment_file.filename)
    else:
        print("No Attachment File Detected")

    message = Message(
        subject=subject,
        recipients=[recipient_email],
        cc=[cc_email] if cc_email else None,
        sender=(sender_email, sender_email), 
        #sender=('RJ from Mailtrap', 'mailtrap@demomailtrap.com'),
    )
    message.html = f"<b>{message_content}</b>"

    if attachment_file:
        with attachment_file.stream as fp:  
            attachment_data = fp.read()
            print("Attachment Content Length:", len(attachment_data))
            message.attach(attachment_file.filename, attachment_file.content_type, fp.read())

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

    query = query.order_by(collate(Course.cname, 'NOCASE'))

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
@app.route('/generate_pdf', methods=['POST'])
def generatePlanOfStudy():
    try:
        # Retrieve form data
        name = request.form.get('NameField')  # Student name
        student_number = request.form.get('N-Number')  # Student number
        create_date = datetime.now().strftime("%Y-%m-%d") # Curr Date

        #Find The Department (major = department)
        major = request.form.get('majorDropdown')

        # Hardcoded class data for each semester
        class_data = {
            'Semester 1': ['Legal & Ethical Issues in Computing', 'Computer Organization and Architecture', 'Programming II'],
            'Semester 2': ['Computational Structures', 'Intro to Databases', 'Computer Networks'],
            'Semester 3': ['Theory of Computation', 'Data Structures', 'Systems Programming'],
            'Semester 4': ['Constr of Lang Translators', 'Operating Systems', 'Software Engineering'],
            'Semester 5': ['Linear Algebra', 'Prob and Stats for Eng'],
            'Semester 6': ['Design & Analysis of Algorithms'],
            'Semester 7': ['Intro to Artificial Intelligence']
        }

        session = DBSession()
        # Define path to PDF template
        template_path = os.path.join(app.root_path, 'static', 'POS_Template.pdf')

        # Create a PdfWriter object to write to the output PDF
        writer = PdfWriter()

        #Generate Logic ------------------------------------------------------------------
        total_hrs = 0
        comm_hrs = 0
        humanities_hrs = 0
        social_hrs = 0
        math_stat_hrs = 0
        science_hrs = 0
        to_schedule = []

        if (major == 'computer_science'):
        #--------------if computer science major
            major_compsci = session.query(Course).filter(Course.comp_sci == True).filter(Course.completed == False)
            for m in major_compsci:
                to_schedule.append(m)
                if (m.communication == True):
                    comm_hrs += m.credit_hrs
                if (m.humanities == True):
                    humanities_hrs += m.credit_hrs
                if (m.social_sci == True):
                    social_hrs += m.credit_hrs
                if (m.math_stats == True):
                    math_stat_hrs += m.credit_hrs
                if (m.science == True):
                    science_hrs += m.credit_hrs
                total_hrs += m.credit_hrs

        elif (major == 'data_science'):
        #---------------if data science major
            major_datasci = session.query(Course).filter(Course.data_sci == True).filter(Course.completed == False)
            for m in major_datasci:
                to_schedule.append(m)
                if (m.communication == True):
                    comm_hrs += m.credit_hrs
                if (m.humanities == True):
                    humanities_hrs += m.credit_hrs
                if (m.social_sci == True):
                    social_hrs += m.credit_hrs
                if (m.math_stats == True):
                    math_stat_hrs += m.credit_hrs
                if (m.science == True):
                    science_hrs += m.credit_hrs
                total_hrs += m.credit_hrs

        elif (major == 'information_science'):
        #--------------if information science major
            major_infosci = session.query(Course).filter(Course.info_sci == True).filter(Course.completed == False)
            for m in major_infosci:
                to_schedule.append(m)
                if (m.communication == True):
                    comm_hrs += m.credit_hrs
                if (m.humanities == True):
                    humanities_hrs += m.credit_hrs
                if (m.social_sci == True):
                    social_hrs += m.credit_hrs
                if (m.math_stats == True):
                    math_stat_hrs += m.credit_hrs
                if (m.science == True):
                    science_hrs += m.credit_hrs
                total_hrs += m.credit_hrs

        elif (major == 'information_systems'):
        #-------------if information systems major
            major_infosys = session.query(Course).filter(Course.info_sys == True).filter(Course.completed == False)
            for m in major_infosys:
                to_schedule.append(m)
                if (m.communication == True):
                    comm_hrs += m.credit_hrs
                if (m.humanities == True):
                    humanities_hrs += m.credit_hrs
                if (m.social_sci == True):
                    social_hrs += m.credit_hrs
                if (m.math_stats == True):
                    math_stat_hrs += m.credit_hrs
                if (m.science == True):
                    science_hrs += m.credit_hrs
                total_hrs += m.credit_hrs

        elif (major == 'information_technology'):
        #------------if information technology major
            major_infotech = session.query(Course).filter(Course.info_tech == True).filter(Course.completed == False)
            for m in major_infotech:
                to_schedule.append(m)
                if (m.communication == True):
                    comm_hrs += m.credit_hrs
                if (m.humanities == True):
                    humanities_hrs += m.credit_hrs
                if (m.social_sci == True):
                    social_hrs += m.credit_hrs
                if (m.math_stats == True):
                    math_stat_hrs += m.credit_hrs
                if (m.science == True):
                    science_hrs += m.credit_hrs
                total_hrs += m.credit_hrs

        done = session.query(Course).filter(Course.completed == True).all()


        # ---------------------------------------------------General Education 
        for d in done:
            if (d.communication == True):
                comm_hrs += d.credit_hrs
            if (d.humanities == True):
                humanities_hrs += d.credit_hrs
            if (d.social_sci == True):
                social_hrs += d.credit_hrs
            if (d.math_stats == True):
                math_stat_hrs += d.credit_hrs
            if (d.science == True):
                science_hrs += d.credit_hrs
            
        scheduled_class_ids = [course.class_id for course in to_schedule]

        #querying !completed removes possible duplicates

        #----------------communications needed
        must_take = session.query(Course).filter( Course.class_id == 'ENC 1101' ).first()
        if (must_take.completed == False):
            to_schedule.append(must_take)
            comm_hrs += int(must_take.credit_hrs) 
        all_comm_classes = session.query(Course).filter(Course.communication == True).filter(Course.completed == False).filter(Course.class_id != 'ENC 1101').filter(~Course.class_id.in_(scheduled_class_ids)).all()
        while comm_hrs < 9:
            #random.sample() is remvoing the result from the list so no duplicates will be produced
            comm_picked = random.sample(all_comm_classes, 1)
            to_schedule.append(comm_picked[0])
            comm_hrs += int(comm_picked[0].credit_hrs)

        #----------------humanities needed
        all_hum_classes = session.query(Course).filter(Course.humanities == True).filter(Course.completed == False).filter(~Course.class_id.in_(scheduled_class_ids)).all()
        while humanities_hrs < 9:
            hum_picked = random.sample(all_hum_classes, 1)
            to_schedule.append(hum_picked[0])
            humanities_hrs += int(hum_picked[0].credit_hrs)

        #----------------social sciences needed 
        all_social_classes = session.query(Course).filter(Course.social_sci == True).filter(Course.completed == False).filter(~Course.class_id.in_(scheduled_class_ids)).all()
        while social_hrs < 6:
            social_picked = random.sample(all_social_classes, 1)
            to_schedule.append(social_picked[0])
            social_hrs += int(social_picked[0].credit_hrs)

        all_mathstat_classes = session.query(Course).filter(Course.math_stats == True).filter(Course.completed == False).filter(~Course.class_id.in_(scheduled_class_ids)).all()
        if math_stat_hrs < 3:
            mathstat_picked = random.sample(all_mathstat_classes, 1)
            to_schedule.append(mathstat_picked[0])
            math_stat_hrs += int(mathstat_picked[0].credit_hrs)
            
        all_science_classes = session.query(Course).filter(Course.science == True).filter(Course.completed == False).filter(~Course.class_id.in_(scheduled_class_ids)).all()
        if science_hrs < 3:
            science_picked = random.sample(all_science_classes, 1)
            to_schedule.append(science_picked[0])
            science_hrs += int(science_picked[0].credit_hrs)

        all_either_classes = session.query(Course).filter( (Course.science == True) | (Course.math_stats == True) ).filter(Course.completed == False).filter(~Course.class_id.in_(scheduled_class_ids)).all()
        while (math_stat_hrs + science_hrs) < 12:
            chosen = random.sample(all_either_classes, 1)
            if (chosen[0].math_stats == True):
                math_stat_hrs += int(chosen[0].credit_hrs)
            else:
                science_hrs += int(chosen[0].credit_hrs)

        total_hrs += (comm_hrs + humanities_hrs + social_hrs + math_stat_hrs + science_hrs)
        
        #----------------------------------------------------------------------------Genrerate plan

        '''for sched in to_schedule:
            course_id_to_check = sched.class_id
            has_prerequisite = session.query(association_table).\
            filter(association_table.c.course_id == course_id_to_check).\
            count() > 0

            if has_prerequisite:
                print(f"The course with ID '{course_id_to_check}' has prerequisites.")
            else:
                print(f"The course with ID '{course_id_to_check}' does not have prerequisites.")'''

        to_schedule.sort(key=lambda sched: session.query(association_table).filter(association_table.c.course_id == sched.class_id).count() > 0)
        '''semesters = []
        current_semester = []
        current_credits = 0
        index = 0
        to_revisit = []

        for course in to_schedule:
            # Handle labs by pairing them with their corresponding lecture course
            if 'Lab' in course.cname:
                lecture_id = course.class_id.rstrip('L')
                lecture_course = session.query(Course).filter(lecture_id == Course.class_id).first()
                if lecture_course:
                    if lecture_course not in current_semester:
                        current_semester.append(lecture_course)
                        #lecture_course.completed = True
                        current_credits += lecture_course.credit_hrs
                    to_schedule.remove(lecture_course)
                    current_semester.append(course)
                    #course.completed = True
                    current_credits += course.credit_hrs
            #class is not a lab
            else:
                current_semester.append(course)
                current_credits += course.credit_hrs

            if current_credits >= 12:
                semesters.append(current_semester)
                current_semester = []
                current_credits = 0

    
        for index, semester in enumerate(semesters, start=1):
            print(f"Semester {index}:")
            for course in semester:
                print(f"- {course.cname} ({course.class_id})")
            print()'''
        

        for cla in to_schedule:
            print(cla.class_id, cla.cname, "has the following prerequisites: ")
            prerequisites = session.query(association_table).\
                    filter(association_table.c.course_id == cla.class_id).\
                    all()

            
            if prerequisites:
                for p in prerequisites:
                    prereq_course = session.query(Course).filter(Course.class_id == p.prerequisite_id).first()
                    print(prereq_course.class_id, prereq_course.cname)
            else:
                print("None")
            
            print()



        print("Total: ", total_hrs)

        print()



        # Open the preexisting PDF template
        with open(template_path, 'rb') as template_file:
            reader = PdfReader(template_file)

            # Fill in form fields with data
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num] # pdf render
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
                    # Fill out text fields for each semester
                    for semester, classes in class_data.items():
                        for idx, class_name in enumerate(classes):
                            field_name = f'{semester}Row{idx+1}'
                            annot = find_text_field(reader, field_name)
                            if annot:
                                print(f"Updating text field '{field_name}' with class name '{class_name}'")
                                annot.update({NameObject("/V"): createStringObject(class_name)})
                            else:
                                print(f"Text field '{field_name}' not found")

                writer.add_page(page)

        # Define path for output filled PDF
        output_pdf = io.BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)

        # Return the PDF data as a response
        response = make_response(output_pdf.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=filled_plan_of_study.pdf'

        session.close()
        return response

    except Exception as e:
        # Handle exceptions
        print("Error:", str(e))
        return jsonify(success=False, error=str(e))


def find_text_field(reader, field_name):
    for page in reader.pages:
        if '/Annots' in page:
            for annot_num in range(len(page['/Annots'])):
                annot = reader.get_object(page['/Annots'][annot_num])
                if '/T' in annot:
                    annot_field_name = annot['/T']
                    if isinstance(annot_field_name, bytes):
                        annot_field_name = annot_field_name.decode('utf-8')
                    annot_field_name = annot_field_name.strip('(/)').strip()
                    if annot_field_name == field_name:
                        print(f"Found text field '{field_name}'")
                        return annot
    print(f"Text field '{field_name}' not found")
    return None



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

    
