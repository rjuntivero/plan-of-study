from Database import Base, Course
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
