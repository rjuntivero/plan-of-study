from flask import Flask, render_template, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from Database import Base, Course
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os 

app = Flask(__name__)

DB_PATH = 'sqlite:///my_database.db'
engine = create_engine(DB_PATH)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)



@app.route('/')
def index():
    return render_template('index.html')
       

@app.route('/add-box')
def add_box():
    return """
    <div class="smaller-box">
        THIS IS A SMALL BOX
    </div>
    """

@app.route('/email-form')
def email_form():
    return render_template('email_form.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    return "Email sent successfully"

@app.route('/search', methods=['GET', 'POST'])

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
