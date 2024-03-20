from Database import Base, Course
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configure SQLAlchemy engine and session
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()

@app.route('/')
def index():
    # Query courses from the database
    courses = session.query(Course).all()
    return render_template('index.html', courses=courses)

@app.route('/search', methods = ['index.html'])
def search():
    #search courses by name 
    search_term = request.form.get('search_term')
    if search_term:
        courses = session.query(Course).filter(Course.cname.like(f%'%{search_term}%')).all()
        return render_template('results.html', courses = courses)
    else:
        return jsonify({'error': 'Search term is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
