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
    {'class_id': 'COP 2220', 'cname': 'Programming I', 'fall': True, 'spring': True, 'summer': True, 'completed': False, 'credit_hrs': 3, 'description': 'This course provides an introduction to problem solving techniques and the computer programming process. Topics in the course include data types, operations, expressions, flow control, I/O, functions, program structure, software design techniques, and memory allocation. Course concepts are reinforced with many programming projects throughout the course.'},
    {'class_id': 'COT 3100', 'cname': 'Computational Structures', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'This course will cover the mathematical and logical fundamentals required in computer science, information systems, information science, and information technology. The course develops concepts in discrete mathematical structures as applied to computing in general through the topics of sets; logic; proof techniques; Boolean algebra; algorithms and problem solving; number systems; number theory; counting and discrete probability; and relations and graphs.'},
    {'class_id': 'CIS 3253', 'cname': 'Legal and Ethical Issues in Computing', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'This course provides an opportunity to discuss and analyze the legal and ethical issues facing today’s computing professionals, as well as the legal and ethical issues computing professionals may face in the future. Legal and ethical issues are considered from local, as well as global perspectives.'},
    {'class_id': 'COP 3503', 'cname': 'Programming II', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'This course serves as a continuation to the Programming I course. Students are shown additional fundamental concepts of problem solving using the object-oriented paradigm and data structures. The topics in this course include classes, interfaces, objects, class types, events, exceptions, control structures, polymorphism, inheritance, linked lists, arrays, stacks, queues, and deques. Students are expected to apply these concepts through the construction of numerous small software systems using both integrated development environments and command-line- driven tools that support editing, testing, and debugging.'},
    {'class_id': 'CDA 3100', 'cname': 'Computer Organization and Architecture', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 4, 'description': 'This course will cover the fundamental ideas in computer architecture and organization. Topics include machine-level data representation; digital logic; computer arithmetic; processor design; system components and inter-communication; memory hierarchy; multi-core processors; GPU; and modern technological advancements.'},
    {'class_id': 'COT 3210', 'cname': 'Theory of Computation', 'fall': 1, 'spring': 0, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'This course will cover the theory of computation using formal methods for describing and analyzing programming languages and algorithms. Topics include finite automata and regular expressions; formal languages and syntactic analysis; pushdown automata and Turing machines; and computational complexity.'},
    {'class_id': 'COP 3530', 'cname': 'Data Structures', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'Students in this course will study various data structures including binary trees, balanced trees, B-trees, hashing, and heaps. Additional topics include advanced data structures such as splay trees, tree representations, graphs, dynamic memory, and algorithms for sorting and searching. Students are expected to complete projects using object-oriented programming.'},
    {'class_id': 'CNT 4504', 'cname': 'Computer Networks', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'In this course, students will study architectures, protocols, and layers in computer networks and develop client-server applications. Topics include the OSI and TCP/IP models, transmission fundamentals, flow and error control, switching and routing, network and transport layer protocols, local and wide-area networks, wireless networks, client-server models, and network security. Students will extend course topics via programming assignments, library assignments and other requirements.'},
    {'class_id': 'COP 3703', 'cname': 'Introduction to Databases', 'fall': 1, 'spring': 1, 'summer': 1, 'completed': False, 'credit_hrs': 3, 'description': 'This course covers database modeling with emphasis on the relational data model. Principles of relational database design, normal forms, constraints, and SQL programming will be discussed extensively. Additionally, topics related to indexing, views, transactions, XML and No-SQL databases will also be discussed. The course will cover aspects of information security and assurance as they relate to data management. Concepts covered in the course will be reinforced through the use of open source and/or commercial database management systems.'},
    {'class_id': 'COP 3404', 'cname': 'Systems Programming', 'fall': 1, 'spring': 0, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Students will learn the design and role of systems software including assemblers, loaders and linkers; assembly programming; system libraries; utility programs; concurrent programming including threads, semaphores, and synchronization; event-driven programming; memory management; and machine-dependent code optimization techniques.'},
    {'class_id': 'COP 4620', 'cname': 'Construction of Language Translators', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'This course introduces students to the theoretical foundations and practical issues of designing language translators. Students will learn how to use compiler construction tools such as generators of scanners and parsers. Grammars, parsing, lexical analysis, syntax analysis, code generation, and optimization will also be discussed.'},
    {'class_id': 'CEN 4010', 'cname': 'Software Engineering', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'This course introduces students to fundamental Software Engineering concepts and current practices. Topics covered include: software process models; agile software development; requirements engineering; domain modeling; model-driven development; software architectures; design paradigms and patterns; project management, tracking, and release planning; collaborative development, testing, deployment, maintenance and evolution.'},
    {'class_id': 'COT 4400', 'cname': 'Design and Analysis of Algorithms', 'fall': 1, 'spring': 0, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'This course will introduce fundamental techniques for designing and analyzing algorithms, including asymptotic analysis; divide-and-conquer algorithms and recurrences; greedy algorithms; dynamic programming; and graph algorithms.'},
    {'class_id': 'CAP 4630', 'cname': 'Introduction to Artificial Intelligence', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Course topics include heuristic techniques for problem-solving and decision making, control and search strategies, knowledge representation, logic, AI languages, and tools. Applications such as machine learning, natural language understanding, planning, and robotics will be included.'},
    {'class_id': 'COP 4610', 'cname': 'Operating Systems', 'fall': 0, 'spring': 1, 'summer': 0, 'completed': False, 'credit_hrs': 3, 'description': 'Topics in this course include process management, memory management, file management, and I/O device management.'}]

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
