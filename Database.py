from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
Base = declarative_base()

association_table = Table('prerequisite_association', Base.metadata,
    Column('course_id', String, ForeignKey('Course.class_id'), primary_key=True),
    Column('prerequisite_id', String, ForeignKey('Course.class_id'), primary_key=True)
)

class Course(Base):
    __tablename__ = 'Course'
    class_id = Column(String, primary_key = True) 
    cname = Column(String, nullable = False, unique = True)
    fall = Column(Boolean)
    spring = Column(Boolean)
    summer = Column(Boolean)
    completed = Column(Boolean, nullable = False)
    credit_hrs = Column(Integer, nullable = False)
    description = Column(Text)
    prerequisites = relationship('Course', secondary=association_table,
                                 primaryjoin=class_id == association_table.c.course_id,
                                 secondaryjoin=class_id == association_table.c.prerequisite_id,
                                 backref='prerequisite_of')

    def __repr__(self):
        return f"Course: {self.class_id} Course Name: {self.cname}"


Base.metadata.create_all(engine)
session = Session()

course_details = [
    #Computer Science specific courses
    {'class_id': 'COP 2220', 'cname': 'Programming I', 'fall': True, 'spring': True, 'summer': True, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COT 3100', 'cname': 'Computational Structures', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'CIS 3253', 'cname': 'Legal and Ethical Issues in Computing', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COP 3503', 'cname': 'Programming II', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'CDA 3100', 'cname': 'Computer Organization and Architecture', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 4, 'description': 'Description'},
    {'class_id': 'COT 3210', 'cname': 'Theory of Computation', 'fall': 1, 'spring': 0, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COP 3530', 'cname': 'Data Structures', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'CNT 4504', 'cname': 'Computer Networks', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COP 3703', 'cname': 'Introduction to Databases', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COP 3404', 'cname': 'Systems Programming', 'fall': 1, 'spring': 0, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COP 4620', 'cname': 'Construction of Language Translators', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'CEN 4010', 'cname': 'Software Engineering', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COT 4400', 'cname': 'Design and Analysis of Algorithms', 'fall': 1, 'spring': 0, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'CAP 4630', 'cname': 'Introduction to Artificial Intelligence', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Description'},
    {'class_id': 'COP 4610', 'cname': 'Operating Systems', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Description'}]

prereq_details = [
    #Compuer Science specific prerequisites, read as "Course (course_id) has the prequisite (prerequisite_id) 
    {'course_id': 'CIS 3253', 'prerequisite_id': 'COP 2220'},
    {'course_id': 'COP 3503', 'prerequisite_id': 'COP 2220'},
    {'course_id': 'CDA 3100', 'prerequisite_id': 'COP 2220'},
    {'course_id': 'COT 3210', 'prerequisite_id': 'COT 3100'},
    {'course_id': 'COP 3530', 'prerequisite_id': 'COT 3100'},
    {'course_id': 'COP 3530', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'CNT 4504', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'COP 3703', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'COP 3404', 'prerequisite_id': 'COP 3503'},
    {'course_id': 'COP 3404', 'prerequisite_id': 'CDA 3100'},
    {'course_id': 'COP 4620', 'prerequisite_id': 'COT 3210'},
    {'course_id': 'COP 4620', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'CEN 4010', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'COT 4400', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'CAP 4630', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'COP 4610', 'prerequisite_id': 'COP 3530'},
    {'course_id': 'COP 4610', 'prerequisite_id': 'COP 3404'},
    {'course_id': 'CEN 4010', 'prerequisite_id': 'COP 3703'}
    ]

for course_detail in course_details:
    c = Course(**course_detail)
    session.add(c)

for p in prereq_details:
    p = association_table.insert().values(**p)
    session.execute(p)

session.commit()

courses = session.query(Course).all()
for course in courses:
    print(course)
    prerequisites = course.prerequisites
    if prerequisites:
        print("Prerequisites:")
        for prereq in prerequisites:
            print(f"- {prereq.class_id}")
    else:
        print("No Prerequisites")
    print()